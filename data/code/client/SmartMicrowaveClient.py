from socket import *
import sys
import time
import picamera
from time import sleep
import RPi.GPIO as GPIO
import lcd_i2c as lcd
import serial

serverName = '165.194.17.15'
serverPort = 5163
clientSocket = socket(AF_INET, SOCK_STREAM)
fileName = 'image.jpg'
buttonLeft = 5
buttonRight = 6
myWatt = '700'
#myWatt = '1000'
ser = serial.Serial("/dev/ttyACM0", 9600)

def initialize():
    global ser
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    lcd.lcd_init()
    ser.baudrate = 9600

def connect(serverName, serverPort):
    clientSocket.connect((serverName, serverPort))
    print("The client is running on port", clientSocket.getsockname()[1])

def capture(fileName):
    while True:
        if GPIO.input(buttonLeft) == False:
            lcd.lcd_string("Do you want", lcd.LCD_LINE_1)
            lcd.lcd_string("check?", lcd.LCD_LINE_2)
            sleep(0.3)
			
            while True:
                if GPIO.input(5) == False:
                    lcd.lcd_string("Checking", lcd.LCD_LINE_1)
                    lcd.lcd_string("operation time", lcd.LCD_LINE_2)
                    print("capture")
                    with picamera.PiCamera() as camera:
                        camera.capture(fileName)
                    return

                elif GPIO.input(6) == False:
                    lcd.lcd_string("Back to the", lcd.LCD_LINE_1)
                    lcd.lcd_string("First", lcd.LCD_LINE_2)
                    sleep(2)
                    printFirstScreen()
                    break
            
def getTemperature():
    ser.write("GET".encode());
    temperature_read = ser.readline().decode()
    temperature = int(temperature_read)
    print('Temperature : %d degree' % temperature)
    if temperature > 0:
        temperature_str = '+' + '%.2d' % temperature
    elif temperature == 0:
        temperature_str = '+00'
    else:
        temperature_str = '-' + '%.2d' % temperature
    return temperature_str


def sendData(fileName, temperature):
    f = open(fileName, 'rb')
    print("Transferring Image...")
    data = f.read(1024)
    myWattEncoded = myWatt[0].encode()
    temperatureEncoded = temperature.encode()
    clientSocket.send(myWattEncoded)
    clientSocket.send(temperatureEncoded)
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

def displayOperationTime(operationTime):
    #todo display the Operation Time on the LCD Module
    print(operationTime)
    lcd.lcd_string(operationTime, lcd.LCD_LINE_1)
    lcd.lcd_string("Operate?", lcd.LCD_LINE_2)
    sleep(0.3)
    while True:
        if GPIO.input(5) == False:
            lcd.lcd_string("Operating...", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            sleep(3)
            break
        elif GPIO.input(6) == False:
            lcd.lcd_string("Back to the", lcd.LCD_LINE_1)
            lcd.lcd_string("First", lcd.LCD_LINE_2)
            sleep(2)
            break

def printResult(result):
    print("The Image is %s." % result)
	
def printFirstScreen():
    lcd.lcd_string("SMART MICROWAVE ", lcd.LCD_LINE_1)
    lcd.lcd_string("", lcd.LCD_LINE_2)

initialize()
connect(serverName, serverPort)

while True:
    try:
        printFirstScreen()
        capture(fileName)
        temperature = getTemperature()
        sendData(fileName, temperature)
        result = receiveData()
        displayOperationTime(result)

    except KeyboardInterrupt:
        print('Keyboard Interrupt occurs')
        clientSocket.close()
        sys.exit(0)


