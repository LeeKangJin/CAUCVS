from socket import *
import sys
import time
import picamera
from time import sleep
import RPi.GPIO as GPIO

serverName = '165.194.17.15'
serverPort = 5163
clientSocket = socket(AF_INET, SOCK_STREAM)
fileName = 'image.jpg'
buttonLeft = 5
buttonRight = 6
myWatt = '700'
#myWatt = '1000'

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def connect(serverName, serverPort):
    clientSocket.connect((serverName, serverPort))
    print("The client is running on port", clientSocket.getsockname()[1])

def capture(fileName):
    while True:
        if GPIO.input(buttonLeft) == False:
            print("capture")
            with picamera.PiCamera() as camera:
                camera.capture(fileName)
            break

def sendData(fileName):
    f = open(fileName, 'rb')
    data = f.read(1024)
    myWattEncoded = myWatt[0].encode()
    clientSocket.send(myWattEncoded)
    while data:
        clientSocket.send(data)
        data = f.read(1024)
    sleep(1)
    clientSocket.send(b'\x00\x00')
    f.close()
    print("Image transfer complete.")
    

def receiveData():
    operationTime = clientSocket.recv(2048)
    return operationTime.decode()

def dispalyOperationTime(operationTime):
    #todo display the Operation Time on the LCD Module
    print(operationTime)

def printResult(result):
    print("The Image is %s." % result)

initialize()
connect(serverName, serverPort)

while True:
    try:
        capture(fileName)
        sendData(fileName)
        result = receiveData()
        printResult(result)
        #displayOperationTime(operationTime)

    except KeyboardInterrupt:
        print('Keyboard Interrupt occurs')
        clientSocket.close()
        sys.exit(0)


