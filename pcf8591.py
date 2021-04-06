#!/usr/bin/python3
#script-poti-pcf8591.py
# by MKO - Mario Kowalczyk | www.trackimo.info

# using potentiometer for AIN0 and voltmeter to simulate U
# check it by sudo i2cdetect -y 1
# Value range AIN1: 0 - 255 , and AOUT: 0 - 3V or 0 - 5V

import smbus    # import the library
import time
import paho.mqtt.client as mqtt
import json

adress = 0x48   # define variables , modul address and chanel
A0 = 0x40       # AOUT liefert Dezimalwert 0 bis 3
A1 = 0x41       # AIN1 liefert Integer 0 bis 255
A2 = 0x42       
A3 = 0x43


bus = smbus.SMBus(1)   # create an object
broker_address="localhost" 
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker  print("connecting to broker")



# Funktion erstellen zum Callback von Messages:
def on_message(client, userdata, message):
    a_wert = str(message.payload.decode("utf-8"))
    print(a_wert)                                    # Wert am Terminal anzeigen

#Spannungs-Wert am Ausgang einstellen
# Info Hexwerte sind für Volllast: 0xff, für 50%: 0x80, für Aus: 0x00
    
    write = bus.write_byte_data(adress, 0x40, int(a_wert)) # Wert am AOUT setzen
    set (a_wert)  # Wert am AOUT setzen
    
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)


client.on_message=on_message #attach function to callback

client.loop_start() #start the loop

print("Subscribing to topic","adda/aout")
a_wert = client.subscribe("adda/aout")    # Wert aus MQTT Out an das Topic übergeben


time.sleep(1) # wait
client.loop_stop() #stop the loop


#Wert am Eingang messen und mit MQTT senden

while True:
    bus.write_byte(adress,A1)         # make the analog measurement
    value = bus.read_byte(adress)    # stores the adress read in the variable value
           
    print(value)
    
    # publish.single("adda/poti", value, hostname="192.168.178.40") # sende mit mqtt , den Wert vom Poti
    # direkter Terminalbefehl ist: mosquitto_pub( -d -t adda/poti -m "hello")
    client.publish("adda/poti", value)
    
    client.loop(0.5)
    print("Subscribing to topic","adda/aout")
    a_wert = client.subscribe("adda/aout")    # Wert aus MQTT Out an das Topic übergeben

    
    time.sleep(0.1)
    

    