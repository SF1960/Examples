RPi.GPIO as GPIO import Adafruit_CharLCD as LCD
Then we need to set the mode of GPIO. After setting this mode, the GPIO number and the physical pin number on the Raspberry Pi board are corresponding.
# set GPIO board mode
GPIO.setmode(GPIO.BOARD)
Then create two lists to distinguish the independent key data and the matrix key data, initialize the lcd, and then set the id of the matrix button and the corresponding GPIO port of the row and column.
a=[]
b=[]
# matrix button id # define LCD column and row size for 16x2 LCD
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
In the activateButton () function, we get what the button is pressed and display it on the lcd, then add the pressed button value to the a list.
def activateButton( rowPin, colPin):
    # get the button index
    btnIndex = buttonIDs[rowPin][colPin] - 1
    lcd.message('{0}'.format(btnIndex+1))
        
    a.append(btnIndex+1)
    return btnIndex+1
In the indeButton () function, we need to define the gpio of the button, and what is represented when the different GPIO port buttons are pressed and displayed on the lcd, and finally add the button value to the b list. def indeButtons():
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
In the matrixButtons () function, we will set the mode of the matrix button to determine if the button has been pressed, if it is pressed, call the activateButton function (display the pressed button and add it to the a list), and finally restore the button state.
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
                     # do nothing while button is being held down
                     while(buttonHeldDown(i)):
                         pass
                     break
              # return each output pin to high
             GPIO.output(columnPins[j],1)
         break
