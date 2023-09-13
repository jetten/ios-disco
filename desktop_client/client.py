import sys
import socket
import threading
from PyQt5 import QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal
import traceback
import ui

class MainWindow(QtWidgets.QMainWindow, ui.Ui_MainWindow):

    connectedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.strobespeed = 0

        self.connectedSignal.connect(self.connectedTrigger)

        #threading.Thread(target=self.connectionCheck).start()

        self.strobeslider.setRange(0,63)
        self.cd = QtWidgets.QColorDialog()

        self.btn2.setStyleSheet("background-color: orange;")

        self.btn.clicked.connect(self.btnstate)
        self.btn2.clicked.connect(self.btnstate)
        self.colorbtn.clicked.connect(self.colorDialog)
        self.power.clicked.connect(self.powerstate)
        self.strobeslider.valueChanged.connect(self.strobespeedChanged)
        self.strobeOffBtn.clicked.connect(self.strobespeedChanged)
        self.strobeOnBtn.clicked.connect(self.strobespeedChanged)
        self.strobePulseBtn.clicked.connect(self.strobespeedChanged)
        self.strobeRandomBtn.clicked.connect(self.strobespeedChanged)
        self.floodlightOff.clicked.connect(self.floodlight)
        self.floodlightOn.clicked.connect(self.floodlight)
        self.floodlightSlow.clicked.connect(self.floodlight)
        self.floodlightFast.clicked.connect(self.floodlight)
        self.floodlightUltra.clicked.connect(self.floodlight)


    def connectionCheck(self):
        global sock, connectionStatus
        try:
            sock.send(b"PING\n")
            while True:
                response = sock.recv(1024)

                if b"UP" in response:
                    connectionStatus = "connected"
                    self.power.setEnabled(True)
                    self.power.setChecked(True)
                    break
                elif b"DOWN" in response:
                    self.power.setEnabled(True)
                    connectionStatus = "connected"
                    break
                elif b"LOCK" in response:
                    connectionStatus = "locked"
                    self.power.setEnabled(False)
                    break
                elif len(response)==0: # Socket is closed
                    connectionStatus = "failed"
                    break

        except: # Socket is not connected yet
            pass

        self.connectedSignal.emit()

    def colorDialog(self):
        self.color = self.cd.getColor()
        if self.color.isValid():
            #self.setStyleSheet("background-color: "+self.color.name()+";")
            self.colorbtn.setStyleSheet("background-color: "+self.color.name()+";")
            smoke.setRgb(self.color.red(), self.color.green(), self.color.blue())


    def connectedTrigger(self):
        global connectionStatus, connectionchecktimer
        try: connectionStatus
        except NameError: connectionStatus=None

        if connectionStatus=="failed":
            self.b.setText("Anslutning misslyckades")
            self.b.setStyleSheet("color: red;")
            self.power.setEnabled(False)
        elif connectionStatus=="connected":
            self.b.setText("Ansluten")
            self.b.setStyleSheet("")
            connectionchecktimer = threading.Timer(1800, self.connectionCheck)
            connectionchecktimer.start()
        elif connectionStatus=="locked":
            self.b.setText("Ansluten, strömkontroll avstängd och låst")
            self.b.setStyleSheet("")
        else:
            self.b.setText("Ansluter...")
            self.b.setStyleSheet("color: red;")
            connectionchecktimer = threading.Timer(1, self.connectionCheck)
            connectionchecktimer.start()
        self.b.adjustSize()


    def btnstate(self):
        global sock

        if (self.sender()== self.btn and self.btn.isChecked()):
            self.btn2.setChecked(False)
        elif (self.sender()== self.btn2 and self.btn2.isChecked()):
            self.btn.setChecked(False)

        if self.btn.isChecked():
            try: smoke.setRgb(self.color.red(), self.color.green(), self.color.blue())
            except: pass
            smoke.setMode(255)
            #self.btn.setText("RUNNING")
            #self.btn.setStyleSheet("background-color: green")
        elif self.btn2.isChecked():
            smoke.setRgba(0, 0, 0, 255)
            smoke.setMode(255)

        else:
            smoke.setMode(0)
            #self.btn.setText("GO")
            #self.btn.setStyleSheet("background-color: initial")

    def powerstate(self):
        smoke.setPower(self.power.isChecked())

    def strobespeedChanged(self):
        if self.strobeOffBtn.isChecked():
            smoke.setStrobe(0)
        elif self.strobeOnBtn.isChecked():
            smoke.setStrobe(self.strobeslider.value()+32)
        elif self.strobePulseBtn.isChecked():
            smoke.setStrobe(self.strobeslider.value()+96)
        elif self.strobeRandomBtn.isChecked():
            smoke.setStrobe(self.strobeslider.value()+160)

    def floodlight(self):
        if self.floodlightOn.isChecked():
            smoke.setFloodlight(255,0)
        elif self.floodlightOff.isChecked():
            smoke.setFloodlight(0,255)
        elif self.floodlightSlow.isChecked():
            smoke.setFloodlight(5,25)
        elif self.floodlightFast.isChecked():
            smoke.setFloodlight(8,8)
        elif self.floodlightUltra.isChecked():
            smoke.setFloodlight(2,4)


class SmokeControl():
    def __init__(self):
        self.mode = 0
        self.red = 255
        self.green = 255
        self.blue = 255
        self.amber = 0
        self.strobe = 0
        self.dimmer = 255

    def setPower(self, s):
        if s:
            self.send("1\n")
        else:
            self.send("0\n")

    def setMode(self, m):
            self.mode = m
            self.flush()

    def setRgba(self, r, g, b, a):
            self.red = r
            self.green = g
            self.blue = b
            self.amber = a
            self.flush()

    def setRgb(self, r, g, b):
            self.setRgba(r, g, b, 0)

    def setStrobe(self, s):
            self.strobe = s
            self.send("6 "+str(self.strobe) +"\n")

    def flush(self):
        command  = "1 "+str(self.mode)   +"\n"
        command += "2 "+str(self.red)    +"\n"
        command += "3 "+str(self.green)  +"\n"
        command += "4 "+str(self.blue)   +"\n"
        command += "5 "+str(self.amber)  +"\n"
        command += "6 "+str(self.strobe) +"\n"
        command += "7 "+str(self.dimmer) +"\n"
        self.send(command)

    def setFloodlight(self, ontime, offtime):
        command  = "8 "+str(ontime)      +"\n"
        command += "9 "+str(offtime)     +"\n"
        self.send(command)

    def send(self, command):
        global sock
        sock.sendall(command.encode())
        #print(str.replace(sock.recv(1024).decode(), "\n", ""), end=' ', flush=True)

def exitHandler():
    global connectionchecktimer, smoke
    smoke.setMode(0)
    try: connectionchecktimer.cancel()
    except: pass

if __name__ == '__main__':
    sock = None
    connectionchecktimer = None

    smoke = SmokeControl()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:
        sock = socket.create_connection(("jiihon.com", 9998))
        sock.send(b"LZ6T4DUq\n")
        sock.recv(1024)
    except:
        print("Connection to control server failed")
        connectionStatus = "failed"
        window.connectedSignal.emit()
        print(traceback.format_exc())

    threading.Thread(target=window.connectionCheck).start()

    app.aboutToQuit.connect(exitHandler)
    sys.exit(app.exec_())
