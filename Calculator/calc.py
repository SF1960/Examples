import math
import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD

# set GPIO board mode
GPIO.setmode(GPIO.BOARD)
a=[]
b=[]
# matrix button id 
# define LCD column and row size for 16x2 LCD
lcd_columns=16
lcd_rows=2
# initialize the LCD using the pins
lcd=LCD.Adafruit_CharLCDBackpack(address=0x21)
buttonIDs=[[1,2,3,4],[5,6,7,8],[9,0]]
# gpio input for rows
rowPins=[13,15,29,31]
# gpio outputs for columns
columnPins=[33,35,37,22]
# define four inputs with pull up resistor
for i in range(len(rowPins)):
    GPIO.setup(rowPins[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
# define four outputs and set to high
    for j in range(len(columnPins)):
        GPIO.setup(columnPins[j], GPIO.OUT)
        GPIO.output(columnPins[j], 1)
def activateButton( rowPin, colPin):
    # get the button index
    btnIndex = buttonIDs[rowPin][colPin] - 1
    lcd.message('{0}'.format(btnIndex+1))
        
    a.append(btnIndex+1)
    return btnIndex+1
def buttonHeldDown(pin):
    if(GPIO.input(rowPins[pin]) == 0):
        return True
        return False
def indeButtons():
    buttons = [37,33,35,22]
    for button in buttons:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   
    for button in buttons:
        if(GPIO.input(button) == 0):
            if(button==37):
                button='+'
            elif(button==33):
                button='-'
            elif(button==22):
                button='*'
            else:
                button='/'
            lcd.message('{0}'.format(button))
            b.append(button)
            time.sleep(0.5)
            return button
def matrixButtons():
     # initial the button matrix
     
     while(True):
         for j in range(len(columnPins)):
             GPIO.setup(columnPins[j],GPIO.OUT)
             # set each output pin to low
             GPIO.output(columnPins[j],0)
             for i in range(len(rowPins)):
                 if GPIO.input(rowPins[i]) == 0:
                     # button pressed, activate it
                     activateButton(i,j)
                  #   print("button " + str(activateButton) + "pressed")
                  #   lcd.message('{0}'.format(activateButton))
                     # do nothing while button is being held down
                     while(buttonHeldDown(i)):
                         pass
                     break
              # return each output pin to high
             GPIO.output(columnPins[j],1)
         break
def add(a):
    count=a[-2]+a[-1]
    return count
def sub(a):
    count=a[-2]-a[-1]
    return count
def mul(a):
    count=a[-2]*a[-1]
    return count
def div(a):
    count=a[-2]/a[-1]
    return count
def touch():
    # define touch pin
    touch_pin = 11
    #set GPIO pin to INPUT
    GPIO.setup(touch_pin,GPIO.IN)#,pull_up_down=GPIO.PUD_UP)
    # check if touch detected
    if(GPIO.input(touch_pin)):
        lcd.message('=')
        if(indeButtons):
            if(b[-1]=='+'):
                count=add(a)
            elif(b[-1]=='-'):
                count=sub(a)
            elif(b[-1]=="*"):
                count=mul(a)
            else:
                count=div(a)
        a.append(count)
        lcd.message('{0}'.format(count))
    time.sleep(0.5)
try:
    while True:
        lcd.set_backlight(0)
        matrixButtons()
        indeButtons()
        touch() 
except KeyboardInterrupt:
    lcd.clear()
    lcd.set_backlight(1)
    cleanup()
                    
