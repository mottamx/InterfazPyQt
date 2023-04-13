#Rpi and 74HC4051 
#Pinout of RPi Zero from https://es.pinout.xyz/pinout/# 
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
while i < 2:
    # First channel 000
    print("Y0")
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    time.sleep(tiempo)

    # Second channel 100
    print("Y1")
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    time.sleep(tiempo)

    #Third channel 010
    print("Y2")
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    time.sleep(tiempo)

    #Fourth channel 110
    print("Y3")
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    time.sleep(tiempo)

    #Fifth channel 001
    print("Y4")
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(tiempo)

    #Sixth channel 101
    print("Y5")
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(tiempo)

    #Seventh channel 011
    print("Y6")
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(tiempo)

    #Eigth channel 111
    print("Y7")
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(tiempo)

    print("Everything off")
    i += 1 #Repeat i times

print("End of while") 

GPIO.output(2, GPIO.HIGH) #Disable EN pin
time.sleep(2)
GPIO.cleanup() #Clear GPIO condig

#Carlos Motta
#https://github.com/mottamx/InterfazPyQt
