#
# Name : Kim Kyeong Hwan
# Student ID : 20133316
# MultiThreadTCPServer.py
#

from socket import *
from threading import *
import time
import sys

serverPort = 23316
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
connectionSocket = socket()

clientName = 0          #client's number ex)Client 2
clientNumber = 0        #the number of clients
inputOption = '0'       # initialize inputOption

print("The server is ready to receive on port", serverPort)

def handler(connectionSocket, clientAddress, inputOption, clientName):                      #handle the connection socket's request
    while inputOption[0] != '5':  # if inputOption[0] is not 5, continue
        inputOption = connectionSocket.recv(2048)
        inputOption = inputOption.decode()

        if inputOption[0] == '1':
            modifiedMessage = inputOption[1:].upper()  # inputOption[1:] is a input message except inputOption
            connectionSocket.send(modifiedMessage.encode())

        elif inputOption[0] == '2':
            modifiedMessage = inputOption[1:].lower()  # inputOption[1:] is a input message except inputOption
            connectionSocket.send(modifiedMessage.encode())

        elif inputOption[0] == '3':
            ipAddress = clientAddress[0]
            portNumber = clientAddress[1]
            ipPortMessage = 'IP = ' + ipAddress + ' port = ' + str(portNumber)  # ip address and port number
            connectionSocket.send(ipPortMessage.encode())

        elif inputOption[0] == '4':
            temp = time.localtime()  # server current time
            serverCurrentTime = time.strftime('%Y-%m-%d %H:%M:%S', temp)
            connectionSocket.send(serverCurrentTime.encode())

        elif inputOption[0] == '5':  # if inputOption[0] is 5, close the connection
            global clientNumber
            clientNumber -= 1               #if connection socket is close, then clientNumber minus 1
            print('Client '+str(clientName)+' disconnected. Number of connected clients = '+str(clientNumber))
            connectionSocket.close()

while True:
    try:
        (connectionSocket, clientAddress) = serverSocket.accept()
        print('Connection requested from', clientAddress)
        clientName = clientName + 1
        clientNumber = clientNumber + 1
        print('Client '+str(clientName)+' connected. Number of connected clients = '+str(clientNumber))
        inputOption = '0'  # initialize inputOption
        Thread(target=handler,args=(connectionSocket, clientAddress, inputOption, clientName)).start()                  #multi threading start

    except KeyboardInterrupt:                                           #if user enters 'ctrl+c', close the connection and server socket, and then system exit
        print()
        print('Bye bye~')
        connectionSocket.close()
        serverSocket.close()
        sys.exit()

