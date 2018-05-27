import lcd_i2c as lcd
import RPi.GPIO as GPIO
import sys
from time import sleep
import picamera

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lcd.lcd_init()


while True:
    lcd.lcd_string("SMART MICROWAVE ", lcd.LCD_LINE_1)
    lcd.lcd_string("", lcd.LCD_LINE_2)
    while True:
        if GPIO.input(5) == False:
            lcd.lcd_string("Do you want", lcd.LCD_LINE_1)
            lcd.lcd_string("check?", lcd.LCD_LINE_2)
            sleep(0.3)

            while True:
                if GPIO.input(5) == False:
                    lcd.lcd_string("Checking", lcd.LCD_LINE_1)
                    lcd.lcd_string("operation time", lcd.LCD_LINE_2)
                    picamera.PiCamera().capture('image.jpg')
                    sleep(2)
                    lcd.lcd_string("Kimbap : 20 sec", lcd.LCD_LINE_1)
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
                    break
                elif GPIO.input(6) == False:
                    lcd.lcd_string("Back to the", lcd.LCD_LINE_1)
                    lcd.lcd_string("First", lcd.LCD_LINE_2)
                    sleep(2)
                    break
            break
