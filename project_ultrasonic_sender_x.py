#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:50:43 2024

@author: kimiasattary
"""

main.py for y

-----------------------------------------------------------------

from machine import ADC, Pin, PWM, Timer
from time import sleep, ticks_ms
import machine as ma
from rcwl1601 import RCWL1601

from umqtt.simple import MQTTClient
import network
import sys
   
session = 'kimia/esp32/helloworld/'
BROKER = 'broker.hivemq.com'

# Set pins A0 and A2 for DAC and ADC respectively

sensor1 = RCWL1601(trigger_pin=14, echo_pin=22,echo_timeout_us=1000000) # Change Pins
#sensor2 = RCWL1601(trigger_pin=15, echo_pin=21,echo_timeout_us=1000000) # Change Pins


# Set variables
counter = 0
state = 0
joystick_on = True
distance = 0



 # Report function to print counter value when ISR callback updated
def report(pin):
     global counter
     global state
     
     print('Counter = ' + str(counter))

   
def position(timer):

    global sensor1
    global distance
    distance = sensor1.distance_cm()


def ult2mqtt(timer):
    global np
    global sensor1
    global distance
    global joystick_on
    distance = sensor1.distance_cm()
    print(distance)
    x = 'x'
   
    topic = "{}/coord".format(session)
    data = "{0}, {1}".format(x,distance)
    
    if joystick_on == False:
    
        try:
            mqtt.publish(topic, data)
        except:
            mqtt.connect()
            mqtt.publish(topic, data)
           
        print("send topic='{}' data='{}'".format(topic, data))
       
        print('')


def switch(c, u, message):
    global joystick_on
    msg = message.payload.decod('ascii')
    # Use this boolean to decide whether or not to publish to MQTT
    joystick_on = bool(msg)

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)
   
# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(client_id="esp32", server=BROKER, port=1883)
mqtt.connect()
print("Connected!")

joystick_topic = "{}/joystick".format(session, qos)
mqtt.subscribe(joystick_topic)
mqtt.message_callback_add(joystick_topic, switch)

t2 = Timer(3)
t2.init(period=2000, mode=t2.PERIODIC, callback=ult2mqtt)

sleep(15)
t2.deinit()
print("Timer 2 deinit")