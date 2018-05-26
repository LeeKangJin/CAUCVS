from socket import *
from threading import *
import sys
import sqlite3
import predict
from time import sleep

serverPort = 5163
serverSocket = socket(AF_INET, SOCK_STREAM)
connectionSocket = socket()
numOfClient = 1
rt = 10

def serverOpen(serverPort):
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port", serverPort)

def receiveData(fileName, connectionSocket):
    wattCheck = connectionSocket.recv(1).decode()
    ct = connectionSocket.recv(3).decode()
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
    return wattCheck, int(ct)

def imageRecognition(fileName):
    foodCategory = predict.predict(fileName)
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
    sql = "select TargetTemperature from CVSFood where FoodCategory = ?"
    cur.execute(sql, (foodCategory,))
    tt = cur.fetchone()
    return int(operationTime[0]), int(tt[0])

def changeTimeFormat(operationTime):
    min = int(operationTime / 60)
    sec = int(operationTime - min * 60)
    min = str(min)
    if sec == 0:
        sec = '00'
    else:
        sec = str(sec)
    changedOperationTime = min + ':' + sec
    return changedOperationTime

def sendData(operationTime, connectionSocket):
    connectionSocket.send(operationTime.encode())

def handler(connectionSocket):
    global numOfClient
    fileName = 'image'+  str(numOfClient) + '.jpg'
    numOfClient += 1
    while connectionSocket.fileno() != -1:
        (wattCheck, ct) = receiveData(fileName, connectionSocket)
        foodCategory = imageRecognition(fileName)
        (operationTime, tt) = matchDB(foodCategory, wattCheck)
        operationTime = operationTime * ((tt - ct)/(tt - rt))
        operationTime = changeTimeFormat(operationTime)
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


