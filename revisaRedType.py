import itertools
import os
import socket
import subprocess
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #GPIO
GPIO.setwarnings(False)
# Define the GPIO pin number to which the button is connected (GPIO 21)
button_pin = 21
# Set the GPIO pin as an input pin with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


modelDict = {}

#Load dictionary
with open("AX-325.txt", 'r', encoding='utf-8') as fileA:
    content = fileA.read()
    modelDict = eval(content)
#print("Diccionario ya cargado")
pins = {
   #Pins decoder 1
    'S0_1': {'pin' : 10}, #10, 9, 11
    'S1_1': {'pin' : 9},
    'S2_1': {'pin' : 11},
   #Pins decoder 2
    'S0_2': {'pin' : 17}, #17, 27, 22
    'S1_2': {'pin' : 27},
    'S2_2': {'pin' : 22},
   #enablers 
    'EN_1': {'pin' : 2},
    'EN_2': {'pin' : 3},
}
for i, pin_name in enumerate(pins):
    if i < len(pins) - 2:
        GPIO.setup(pins[pin_name]["pin"], GPIO.OUT) 
        GPIO.setup(pins[pin_name]["pin"], GPIO.LOW)


def check_wlan_connection():
    global CONNECTED
    max_attempts = 4
    reset_attempts = 3
    attempt_count = 0
    reset_count = 0

    while attempt_count < max_attempts:
        try:
            # Attempt to resolve a hostname to check if WLAN is connected
            socket.gethostbyname("google.com")
            print("WLAN is connected.")
            CONNECTED = True
            return True
        except socket.error:
            CONNECTED = False
            attempt_count += 1
            if reset_count < reset_attempts:
                print(f"WLAN is not connected. Retrying ({attempt_count}/{max_attempts})...")
            else:
                print(f"WLAN is not connected after {reset_attempts} attempts. Resetting Wi-Fi...")
                # Restart the Wi-Fi network using wpa_supplicant
                subprocess.run(["sudo", "systemctl", "restart", "wpa_supplicant"], check=True)
                print("Wi-Fi has been reset. Retrying connection...")
                reset_count = 0

            time.sleep(60)
            reset_count += 1

    print("WLAN is not connected after multiple attempts.")
    return False

def get_linux_wlan_name():
    try:
        output = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError:
        return None

def get_wlan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        return None

def print_data(NETWORK, IP):
    #print("WLAN Name:", NETWORK)
    #print("IP Address:", IP)
    # Pin 74HC4051 that multiplex to the 8 outputs
    GPIO.setmode(GPIO.BCM) #GPIO
    GPIO.setwarnings(False)
    GPIO.setup(10, GPIO.OUT) #S0
    GPIO.setup(9, GPIO.OUT) #S1
    GPIO.setup(11, GPIO.OUT) #S2
    GPIO.setup(3, GPIO.OUT) #Enable, check notes
    GPIO.setup(17, GPIO.OUT) #S0.2
    GPIO.setup(27, GPIO.OUT) #S1.2
    GPIO.setup(22, GPIO.OUT) #S2.2
    GPIO.setup(2, GPIO.OUT) #Enable2, check notes 
    GPIO.output(2, GPIO.HIGH)#Disable EN pin
    GPIO.output(3, GPIO.HIGH)
    for i, pin_name in enumerate(pins):
        if i < len(pins) - 2:
            GPIO.setup(pins[pin_name]["pin"], GPIO.LOW)
    alldata= NETWORK + ' '+ IP + '@' 
    for letter in alldata:
        codeTw = modelDict.get(letter, ' ') #For default
        subString = [] #To split if special char
        if len(codeTw) == 6: #If normal keystroke, just append
            subString.append(codeTw)
        elif len(codeTw) > 6:  #If triple jeystroke, split into threee
            for i in range(0, len(codeTw), 6):
                singleCode = codeTw[i:i+6]
                subString.append(singleCode)        
        #Now send accordingly
        for j, keyStroke in enumerate(subString):
            for i, pin_name in enumerate(pins):
                if i < len(pins) - 2:
                    GPIO.setup(pins[pin_name]["pin"], GPIO.LOW)
            time.sleep(0.024) #0.025 baseline
            #Here it changes the GPIO
            #print(keyStroke)
            GPIO.output(10, int(keyStroke[3])) #10 9 11
            GPIO.output(9, int(keyStroke[4]))
            GPIO.output(11, int(keyStroke[5]))
            GPIO.output(17, int(keyStroke[0])) #17 27 22
            GPIO.output(27, int(keyStroke[1]))
            GPIO.output(22, int(keyStroke[2]))
            #Now enable outputs
            time.sleep(0.024) #0.025  baseline
            GPIO.output(2, GPIO.LOW)
            GPIO.output(3, GPIO.LOW)
			# Wait  seconds
            time.sleep(0.16) #0.16 baseline
            #Disable again
            GPIO.output(2, GPIO.HIGH)#Disable EN pin
            GPIO.output(3, GPIO.HIGH)
            if letter =="@":
                time.sleep(0.50) #0.025  baseline
            #print(keyStroke)

    GPIO.output(pins["EN_1"]["pin"], GPIO.HIGH)#Disable EN pin
    GPIO.output(pins["EN_2"]["pin"], GPIO.HIGH)
    GPIO.output(pins["S0_1"]["pin"], GPIO.LOW)
    GPIO.output(pins["S1_1"]["pin"], GPIO.LOW)
    GPIO.output(pins["S2_1"]["pin"], GPIO.LOW)
    GPIO.output(pins["S0_2"]["pin"], GPIO.LOW)
    GPIO.output(pins["S1_2"]["pin"], GPIO.LOW)
    GPIO.output(pins["S2_2"]["pin"], GPIO.LOW)
    time.sleep(0.05)
			
def check_appservice():
    # Check if the 'app' service is active, otherwise reset it
    service_status = subprocess.run(["systemctl", "is-active", "app"], capture_output=True, text=True)
    
    if service_status.stdout.strip() != "active":
        try:
            subprocess.run(["sudo", "systemctl", "restart", "app"], check=True)
            print("The 'app' service has been restarted.")
            # Wait for a few seconds to allow the service to start
            time.sleep(5)

            # Check the service status again to see if it is running after restart
            service_status = subprocess.run(["systemctl", "is-active", "app"], capture_output=True, text=True)
            if service_status.stdout.strip() == "active":
                print("Service has been restarted successfully.")
                return True  # Service was restarted successfully
            else:
                print("Service restart failed.")
                return False  # Service restart failed
        except subprocess.CalledProcessError:
            print("Failed to restart the 'app' service.")
            return False  # Failed to restart the service
    else:
        print("Service is already active.")
        return True  # Service is already active

    
def button_pressed(channel):
    global CONNECTED
    CONNECTED = check_wlan_connection()
    if CONNECTED:
    # Get WLAN name on Linux
        NETWORK = get_linux_wlan_name()
        # Get IP address in the format like 192.168.x.x
        IP = get_wlan_ip()
        #Send to Type
        print("Typing data.")
        print_data(NETWORK, IP)

        if check_appservice():
            print_data('Server', 'ON')
        else:
            print_data('Vuelve a', 'presionar')
            time.sleep(1)
    else:
        print_data('Vuelve a', 'presionar')
        print("WLAN is still not connected. Exiting.")

# Add an event listener for button press (falling edge detection)
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)

if __name__ == "__main__":
    CONNECTED = False
    NETWORK = None
    IP = None

    try:
        print("Press the button on GPIO 21...")
        while True:
            # Your main program can continue running here
            pass

    except KeyboardInterrupt:
        # If the user presses Ctrl+C, clean up the GPIO settings
        GPIO.cleanup()


    
