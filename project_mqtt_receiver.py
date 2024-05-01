import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import math

import pyautogui as p
from pynput import keyboard
from pynput.keyboard import Key
from keys import sess

"""
Get measurement results from microphyton board and plot on host computer.
Use in combination with mqtt_plot_mpy.py.

Install paho MQTT client and matplotlib on host, e.g.
    $ pip install paho-mqtt
    $ pip install matplotlib

Start this program first on the host from a terminal prompt, e.g.
    $ python mqtt_plot_host.py
then run mqtt_plot_mpy.py on the ESP32.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_mpy.py
session = sess
BROKER = "broker.hivemq.com"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client(paho.CallbackAPIVersion.VERSION2)
mqtt.connect(BROKER, port=1883)
print("Connected!")

def joystick(f):
    x = float(f[0])
    y = float(f[1])
    on = bool(f[2])
    
    # Map to pixels on screen
    # max value from joystick is 65535
    # max X-coord is 1920, max Y-coord is 1080
    if on:
        if x > 37000 and x < 41000 and y > 24000 and y < 30000:
            print('Do not move')
        else:
            #speed = 400/max(abs(32500-x), abs(32500-y))
            x = -(x - 32000)/400
            y = -(y - 38000)/400
            print(str(x)+'' + str(y))
                
                
        #x = (x/65535) * 1920
        #y = (y/65535) * 1080
    
            p.move(x, y, duration = 0.2)
   
def ultrasonic(f):
    print('ultrasonic')
    axis= f[0]
    val = f[1]
    
    # get current position
    pyx, pyy = p.position()
    #print(pyx, pyy)
    #print(type(pyx))
    # convert to vector of floats

    if axis == 'x':
        x = float(val)
        y = pyy
        if x > 110:
            x = pyx
        print("x", x)
    if axis == 'y':
        y = float(val)
        if y > 110:
            y = pyy
        x = pyx
        print("y", y)
    # append to data vectors, add more as needed
  
    # Map to pixels on screen
    # max value from joystick is 65535
    # max X-coord is 1920, max Y-coord is 1080

    x = (math.ceil(x)/55) * 1920
    y = (math.ceil(y)/55) * 1080
   
    p.moveTo(x, y, duration = 1)
    

# mqtt callbacks
def coordinates(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ x for x in msg.split(',') ]
    #print("received", f)
    # append to data vectors, add more as needed
    if len(f) == 3:
        joystick(f)
    else:
        ultrasonic(f)
        
def click(c, u, message):
    msg = message.payload.decode('ascii')
    if msg == 'right':
        p.click(button='right')
    if msg == 'left':
        p.click(button='left')
    


# subscribe to topics
coord_topic = "{}/coord".format(session)
mqtt.subscribe(coord_topic)
mqtt.message_callback_add(coord_topic, coordinates)

button_topic = "{}/button".format(session)
mqtt.subscribe(button_topic)
mqtt.message_callback_add(button_topic, click)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()