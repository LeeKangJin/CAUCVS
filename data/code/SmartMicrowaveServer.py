from socket import *
import sys
import predict
from time import sleep

serverPort = 5163
serverSocket = socket(AF_INET, SOCK_STREAM)
fileName = 'image.jpg'
foodCategory = ''
operationTime = ''

def serverOpen(serverPort):
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port", serverPort)

def receiveData(fileName):
    data = connectionSocket.recv(1024)
    f = open(fileName, 'wb')
    while data:
        if data == b'\x00\x00' :
            break
        f.write(data)
        data = connectionSocket.recv(1024)
    f.close()
    print("receive Done")

def imageRecognition(fileName):
    return predict.predict(fileName)

def matchDB(foodCategory):
    #todo match the image to db in order to get operation time
    return operationTime

def sendData(operationTime):
    connectionSocket.send(operationTime.encode())

serverOpen(serverPort)

while True: 
    (connectionSocket, clientAddress) = serverSocket.accept()
    print('Connection requested from', clientAddress)
    while connectionSocket.fileno() != -1:
        try:
            receiveData(fileName)
            result = imageRecognition(fileName)
            sendData(result)

        except KeyboardInterrupt:
            print('Keyboard Interrupt occurs')
            connectionSocket.close()
            serverSocket.close()
            sys.exit(0)

    connectionSocket.close()


