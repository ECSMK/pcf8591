#!/usr/bin/python3
#testingscript-poti-pc8591.py
# by MKO - Mario Kowalczyk | www.trackimo.info

# using potentiometer for AIN0 and voltmeter to simulate U
# check it by sudo i2cdetect -y 1
# Value range 0 - 255 , and 0 - 3V or 0 - 5V

import smbus    # import the library
import time
import json

adress = 0x48   # define variables , modul address and chanel
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
#AOUT = 0x41

bus = smbus.SMBus(1)   # create an object



# Was passiert
a_wert = input ("Geschwindigkeit Volllast-0xff, 50%-0x80, Aus-0x00: ")

#a = float(l) + float(b)

print("OK? " , a_wert)


def set (a_wert):
    write = bus.write_byte_data(adress, 0x40, a_wert)
print("Wert ", a_wert)
set (0x80)

#Spannung am Ausgang einstellen

while True:
    bus.write_byte(adress,A1)         # make the analog measurement
    value = bus.read_byte(adress)    # stores the adress read in the variable value
           
    print(value)
    
    # sende mit mqtt , erstellen ein JSON Objekt
    
#sende="{ \"messung\":{\"satz\": [{\"zeitpunkt\":\"$zeit\" },value ]}}"

 #  mosquitto_pub -d -t poti -m "$sende"    
    
    time.sleep(1.9)
    

    