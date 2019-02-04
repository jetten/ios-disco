#!/usr/bin/python3

import socketserver
import websockets
import socket
import threading
import asyncio
import queue
import time
import sys
import signal
import logging
import traceback

logging.basicConfig(filename="test.py.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
#logging.getLogger('asyncio').setLevel(logging.DEBUG)

commandqueues = []
responsequeues = []
lockdown = False

class IotServerHandler(socketserver.BaseRequestHandler): #9999
    def handle(self):
        global commandqueues, statusupdate

        logging.warning("IOT connect from "+str(self.client_address[0])+", waiting for authentication...")

        # Authentication
        try: self.data = self.request.recv(1024)
        except: return
        if self.data==b"cbsZ\n":
            pass
        else:
            return

        self.q = queue.Queue()
        commandqueues += [self.q]

        logging.warning("IOT from "+str(self.client_address[0])+" authenticated successfully")

        # Watch for responses and add it to response queue
        responsethread = threading.Thread(target=responseListener, args=[self])
        responsethread.start()

        while True:
            #logging.debug("While iteration: IotServerHandler")
            qdata = self.q.get()
            try:
                self.request.sendall(qdata)
            except:
                commandqueues.remove(self.q)
                logging.warning("IOT disconnect")
                return


def responseListener(self):
    while True:
        #logging.debug("While iteration: responseListener")
        try:
            data = self.request.recv(1024)
            if(len(data)==0): return
        except:
            return

        for q in responsequeues:
            q.put(data)


class CtrlServerHandler(socketserver.BaseRequestHandler): #9998

    def handle(self):
        global responsequeues

        # Authentication
        while True:
            #logging.debug("While iteration: CtrlServerHandler Authentication")
            try: self.data = self.request.recv(1024)
            except: return
            if self.data==b"LZ6T4DUq\n":
                self.request.sendall(b"OK\n")
                break
            else:
                try:
                    self.request.sendall(b"NOK\n")
                except:
                    logging.warning("CtrlServer user disconnected before auth")
                    return

        # Add this thread as target for receiving responses
        self.q = queue.Queue()
        responsequeues += [self.q]

        # Watch response queue and send response
        responsethread = threading.Thread(target=responseSender, args=[self])
        responsethread.start()

        # Read command
        while True:
            #logging.debug("While iteration: CtrlServerHandler")
            try:
                self.data = b""
                while (len(self.data)==0 or (self.data.decode()[-1] != "\n")): #Ensure we get a complete command
                    newdata = self.request.recv(1024)
                    self.data += newdata
                    if len(newdata)==0: break
            except:
                responsequeues.remove(self.q)
                return

            response = b""
            for q in commandqueues:
                try:
                    q.put(asciiToBin(self.data))
                    if not lockdown:
                        response=b"OK"
                    else:
                        response=b"LOCK"
                except:
                    response=b"NOK"
                    #logging.debug("NOK: "+sys.exc_info()[1])
                    #print(traceback.format_exc())

            try:
                self.request.sendall(response + str(len(commandqueues)).encode() + b"\n")
            except:
                responsequeues.remove(self.q)
                return

def responseSender(self):
    while True:
        #logging.debug("While iteration: responseSender")
        rdata = self.q.get()
        try: self.request.sendall(rdata)
        except: return


async def websocketHandler(websocket, path):
    global responsequeues

    # Authentication
    while True:
        logging.debug("While iteration: websocketHandler Authentication")
        try:
            data = await websocket.recv()
        except:
            logging.warning("websocketHandler user disconnected before sending password")
            return

        if data=="LZ6T4DUq\n":
            await websocket.send("OK\n")
            break
        else:
            try:
                await websocket.send("NOK\n")
            except:
                logging.warning("websocketHandler user disconnected before auth")
                return


    # Add this thread as target for receiving responses
    q = queue.Queue()
    responsequeues += [q]

    commandtask = asyncio.ensure_future(websocketCommandReceiver(websocket, q, commandqueues, responsequeues))
    responsetask = asyncio.ensure_future(websocketResponseSender(websocket, q))
    await asyncio.wait([commandtask, responsetask], return_when=asyncio.FIRST_COMPLETED)

async def websocketCommandReceiver(websocket, q, commandqueues, responsequeues):
    while True:
        #logging.debug("While iteration: websocketCommandReceiver")
        try:
            #print("waiting for data")
            data = await websocket.recv()
            #print("got data!")
        except:
            try: responsequeues.remove(q)
            except: logging.error("Failed to remove from responsequeue on websocket disconnect")
            #print("Websocket disconnect")
            return

        response = ""
        for qq in commandqueues:
            try:
                qq.put(asciiToBin(data.encode()))
                if not lockdown:
                    response="OK"
                else:
                    response="LOCK"
            except:
                response="NOK"
                logging.debug("NOK: "+sys.exc_info()[1])

        try:
            await websocket.send(response + str(len(commandqueues)) +" \n")
        except:
            try: responsequeues.remove(q)
            except: logging.error("Failed to remove from responsequeue on websocket disconnect")
            #print("Websocket disconnect")
            return

async def websocketResponseSender(websocket, q):
    while True:
        logging.debug("While iteration: websocketResponseSender")
        try:
            rdata = await asyncio.get_event_loop().run_in_executor(None, q_get, q)
            await websocket.send(rdata)
        except:
            logging.error("websocketResponseSender caused exception: "+sys.exc_info()[1])
            logging.error("websocketResponseSender returning now")
            return

def q_get(q):
    return q.get().decode()

def asciiToBin(cmd):
    global lockdown

    cmds = cmd.split(b"\n")
    output = bytearray(b"")

    for s in cmds[:-1]:
        if(s==b'PING'  or s==b'P'):
            if not lockdown:
                output += b'P'
        elif(s==b'0' or s==b'1'):
            if not lockdown:
                output += s
        elif(s==b'L1'):
            lockdown=True
        elif(s==b'L0'):
            lockdown=False
        elif(s==b'L'):
            output += s
        else:
            dmxchannel = int(s.split(b" ")[0])
            dmxvalue   = int(s.split(b" ")[1])
            if (dmxchannel not in range(0,512) or dmxvalue not in range(0,256)):
                raise ValueError("Values outside DMX range")

            output += b'D'
            output [-1] = output[-1] | ((dmxchannel>>1)&128)
            output += (dmxchannel&127).to_bytes(1, byteorder='big')
            output += dmxvalue.to_bytes(1, byteorder='big')

    return bytes(output)


class V6Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

def signal_handler(signal, frame):
    global iotserver, ctrlserver
    iotserver.server_close()
    ctrlserver.server_close()
    logging.warning("quitting")
    sys.exit(0)

if __name__ == "__main__":
    socketserver.allow_reuse_address = True

    iotserver = V6Server(("", 9999), IotServerHandler)
    iotthread = threading.Thread(target=iotserver.serve_forever)
    iotthread.start()

    ctrlserver = V6Server(("", 9998), CtrlServerHandler)
    ctrlthread = threading.Thread(target=ctrlserver.serve_forever)
    ctrlthread.start()

    websocketserver = websockets.serve(websocketHandler, '', 9997)
    asyncio.get_event_loop().run_until_complete(websocketserver)
    asyncio.get_event_loop().run_forever()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
