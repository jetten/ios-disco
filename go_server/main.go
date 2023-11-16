package main

import (
	"bufio"
	"errors"
	"fmt"
	"net"
	"net/http"
	"strconv"
	"strings"

	"golang.org/x/net/websocket"
)

const REQUIRE_AUTH = true

type client chan<- string

var (
	ctrlmessages = make(chan string)
	iotmessages  = make(chan string)
	iotentering  = make(chan client)
	iotleaving   = make(chan client)
	ctrlentering = make(chan client)
	ctrlleaving  = make(chan client)
	wsentering   = make(chan client)
	wsleaving    = make(chan client)

	iotClients  = make(map[client]bool)
	ctrlClients = make(map[client]bool)
	wsClients   = make(map[client]bool)

	lockdown = false
)

func main() {
	go IotListener()
	go CtrlListener()
	go WebsocketListener()
	broadcaster()
}

func broadcaster() {
	for {
		select {
		case msg := <-ctrlmessages:
			for client := range iotClients {
				select {
				case client <- msg:
				default:
					fmt.Println("Send to iotClient blocked")
				}
			}
		case msg := <-iotmessages:
			for client := range ctrlClients {
				select {
				case client <- msg:
				default:
					fmt.Println("Send to ctrlClient blocked")
				}
			}
			for client := range wsClients {
				select {
				case client <- msg:
				default:
					fmt.Println("Send to wsClient blocked")
				}
			}
		case client := <-iotentering:
			iotClients[client] = true
		case client := <-iotleaving:
			delete(iotClients, client)
			close(client)
		case client := <-ctrlentering:
			ctrlClients[client] = true
		case client := <-ctrlleaving:
			delete(ctrlClients, client)
		case client := <-wsentering:
			wsClients[client] = true
		case client := <-wsleaving:
			delete(wsClients, client)
			close(client)
		}
	}
}

func IotListener() {
	listener, err := net.Listen("tcp", ":9999")
	if err != nil {
		fmt.Println(err)
	}
	for {
		conn, err := listener.Accept()
		_ = err
		go handleIotConn(conn)
	}
}

func CtrlListener() {
	listener, err := net.Listen("tcp", ":9998")
	if err != nil {
		fmt.Println(err)
	}
	for {
		conn, err := listener.Accept()
		_ = err
		go handleCtrlConn(conn)
	}
}

func WebsocketServer(ws *websocket.Conn) {
	ch := make(chan string)
	defer func() {
		ws.Close()
		wsleaving <- ch
	}()

	reader := bufio.NewReader(ws)

	if REQUIRE_AUTH {
		data, _ := reader.ReadString('\n')
		if data == "LZ6T4DUq\n" {
			fmt.Fprintln(ws, "OK")
		} else {
			fmt.Fprintln(ws, "NOK")
			return
		}
	}

	fmt.Printf("Websocket client logged in on port 9997 from %s\n", ws.Request().RemoteAddr)
	wsentering <- ch

	go func() {
		for {
			bdata := make([]byte, 1024)
			_, err := reader.Read(bdata)
			if err != nil {
				return
			}
			data, err := asciiToBin(string(bdata))
			if err != nil {
				fmt.Fprintln(ws, "NOK")
				fmt.Printf("[%s] asciiToBin failed: %s\n", ws.Request().RemoteAddr, err)
			} else if lockdown {
				ctrlmessages <- data
				fmt.Fprintln(ws, "LOCK"+fmt.Sprint(len(iotClients)))
			} else {
				ctrlmessages <- data
				fmt.Fprintln(ws, "OK"+fmt.Sprint(len(iotClients)))
			}
		}
	}()

	for {
		message := <-ch
		_, err := fmt.Fprint(ws, message)
		if err != nil {
			return
		}
	}
}

func WebsocketListener() {
	//http.Handle("/", websocket.Handler(WebsocketServer))   # This line will give 403 if Origin is not set on request
	http.HandleFunc("/", func(w http.ResponseWriter, req *http.Request) {
		s := websocket.Server{Handler: websocket.Handler(WebsocketServer)}
		s.ServeHTTP(w, req)
	})
	err := http.ListenAndServe(":9997", nil)
	if err != nil {
		panic("ListenAndServe: " + err.Error())
	}
}

func handleIotConn(conn net.Conn) {
	ch := make(chan string)
	defer func() {
		conn.Close()
		iotleaving <- ch
	}()

	reader := bufio.NewReader(conn)

	// Read password
	if REQUIRE_AUTH {
		data, err := reader.ReadString('\n')
		_ = err
		if data != "cbsZ\n" {
			return
		}
	}

	fmt.Printf("Iot client logged in on port 9999 from %s\n", conn.RemoteAddr())
	iotentering <- ch

	go func() {
		for {
			bdata := make([]byte, 1024)
			_, err := reader.Read(bdata)
			if err != nil {
				return
			}
			iotmessages <- string(bdata)
		}
	}()

	for {
		message := <-ch
		_, err := fmt.Fprint(conn, message)
		if err != nil {
			return
		}
	}
}

func handleCtrlConn(conn net.Conn) {
	ch := make(chan string)
	defer func() {
		conn.Close()
		ctrlleaving <- ch
	}()

	reader := bufio.NewReader(conn)

	// Read password
	if REQUIRE_AUTH {
		data, _ := reader.ReadString('\n')
		if data == "LZ6T4DUq\n" {
			fmt.Fprintln(conn, "OK")
		} else {
			fmt.Fprintln(conn, "NOK")
			return
		}
	}

	fmt.Printf("Control client logged in on port 9998 from %s\n", conn.RemoteAddr())
	ctrlentering <- ch

	go func() {
		for {
			message := <-ch
			_, err := fmt.Fprint(conn, message)
			if err != nil {
				return
			}
		}
	}()

	for {
		bdata := make([]byte, 1024)
		_, err := reader.Read(bdata)
		if err != nil {
			return
		}
		data, err := asciiToBin(string(bdata))
		if err != nil {
			fmt.Fprintln(conn, "NOK")
		} else if lockdown {
			ctrlmessages <- data
			fmt.Fprintln(conn, "LOCK"+fmt.Sprint(len(iotClients)))
		} else {
			ctrlmessages <- data
			fmt.Fprintln(conn, "OK"+fmt.Sprint(len(iotClients)))
		}
	}
}

func asciiToBin(cmd string) (string, error) {
	cmds := strings.Split(cmd, "\n")
	cmds = cmds[:len(cmds)-1]
	output := ""
	for _, cmd = range cmds {
		if cmd == "PING" || cmd == "P" {
			return "P", nil
		} else if cmd == "0" || cmd == "1" {
			if lockdown == false {
				output += cmd
			}
		} else if cmd == "L1" {
			lockdown = true
		} else if cmd == "L0" {
			lockdown = false
		} else if cmd == "L" {
			output += cmd
		} else {
			values := strings.Split(cmd, " ")
			if len(values) != 2 {
				return "", errors.New("invalid number of arguments")
			}
			dmxchannel, dmxchannelerr := strconv.Atoi(values[0])
			dmxvalue, dmxvalueerr := strconv.Atoi(values[1])

			if dmxchannel < 0 || dmxchannel >= 512 || dmxvalue < 0 || dmxvalue >= 256 || dmxchannelerr != nil || dmxvalueerr != nil {
				return "", errors.New("invalid values")
			}

			result := []byte("   ")
			result[0] = 'D' | byte(dmxchannel>>1)&128
			result[1] = byte(dmxchannel) & 255
			result[2] = byte(dmxvalue)
			output += string(result)
		}
	}
	return output, nil
}
