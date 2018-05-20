from socket import *
from threading import *
import sys
import sqlite3
import predict
from time import sleep

serverPort = 5163
serverSocket = socket(AF_INET, SOCK_STREAM)
connectionSocket = socket()
fileName = 'image.jpg'

def serverOpen(serverPort):
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port", serverPort)

def receiveData(fileName, connectionSocket):
    wattCheck = connectionSocket.recv(1).decode()
    if wattCheck == '7':
        print('Power consumption : 700watt')
    elif wattCheck == '1':
        print('Power consumption : 1000watt')
    data = connectionSocket.recv(1024)
    f = open(fileName, 'wb')
    while data:
        if data == b'\x00\x00' :
            break
        f.write(data)
        data = connectionSocket.recv(1024)
    f.close()
    print("Image file received done")
    return wattCheck

def imageRecognition(fileName):
    foodCategory = predict.predict(fileName)
    print("foodCategory : %s" % foodCategory )
    return foodCategory

def matchDB(foodCategory, wattCheck):
    conn = sqlite3.connect('SmartMicrowave.db')
    cur = conn.cursor()
    if wattCheck == '7':
        sql = "select OperationTime700 from CVSFood where FoodCategory = ?"
    elif wattCheck == '1':
        sql = "select OperationTime1000 from CVSFood where FoodCategory = ?"
    cur.execute(sql, (foodCategory,))
    operationTime = cur.fetchone()
    return operationTime[0]

def sendData(operationTime, connectionSocket):
    connectionSocket.send(operationTime.encode())

def handler(connectionSocket):
    while connectionSocket.fileno() != -1:
        wattCheck = receiveData(fileName, connectionSocket)
        foodCategory = imageRecognition(fileName)
        operationTime = matchDB(foodCategory, wattCheck)
        message = foodCategory + ' ' + operationTime
        sendData(message, connectionSocket)

serverOpen(serverPort)

while True:

    try:
        (connectionSocket, clientAddress) = serverSocket.accept()
        print('Connection requested from', clientAddress)
        Thread(target=handler, args=(connectionSocket,)).start()

    except KeyboardInterrupt:
        print('Keyboard Interrupt occurs')
        connectionSocket.close()
        serverSocket.close()
        sys.exit(0)

    #connectionSocket.close()
