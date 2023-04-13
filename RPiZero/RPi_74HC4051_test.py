
#This is a test to check if the Multiplexer is correctly displaying outputs (or x_X)
#Update: Note: The enable pin has to be between GPIOs 0 to 8 bc have pull-ups enabled - the rest have pull-downs enabled

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
i = 0 

# Pin 74HC4051 that multiplex to the 8 outputs
GPIO.setup(17, GPIO.OUT) #S0
GPIO.setup(27, GPIO.OUT) #S1
GPIO.setup(22, GPIO.OUT) #S2
GPIO.setup(2, GPIO.OUT) #Enable, check notes
GPIO.output(2, GPIO.LOW)
tiempo = 0.5
#First channel 000
        #Second channel 100
        #Third channel 010
        #Fourth channel 110
        #Fifth channel 001
        #Sixth channel 101
        #Seventh channel 011
        #Eigth channel 111
keys = ["000", "100", "010", "110", "001", "101", "011", "111"]
while i < 2:
    for keyStroke in keys:
        print("Key", keyStroke)
        GPIO.output(17, int(keyStroke[0]))
        GPIO.output(27, int(keyStroke[1]))
        GPIO.output(22, int(keyStroke[2]))
        time.sleep(tiempo)
    #Now backwards    
    for keyStroke in reversed(keys):
        print("Key", keyStroke)
        GPIO.output(17, int(keyStroke[0]))
        GPIO.output(27, int(keyStroke[1]))
        GPIO.output(22, int(keyStroke[2]))
        time.sleep(tiempo)
    print("Everything off")
    i += 1 #Repeat i times
print("End of while") 

GPIO.output(2, GPIO.HIGH) #Disable EN pin
time.sleep(2)
GPIO.cleanup() #Clear GPIO condig

#Carlos Motta
#https://github.com/mottamx/InterfazPyQt
