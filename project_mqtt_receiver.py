import paho.mqtt.client as paho
import matplotlib.pyplot as plt

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
p.FAILSAFE = False
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
        if x > 35000 and x < 39000 and y > 35000 and y < 39000:
            print('Do not move')
        else:
            #speed = 400/max(abs(32500-x), abs(32500-y))
            x = -(x - 35000)/500
            y = -(y - 35000)/500
            print(str(x)+'' + str(y))
                
                
        #x = (x/65535) * 1920
        #y = (y/65535) * 1080
    
            p.move(x, y, duration = 0.2)
   
def ultrasonic(f):
    print('ultrasonic')
    

# mqtt callbacks
def data(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ x for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    if len(f) == 3:
        joystick(f)
    else:
        ultrasonic()
        


# subscribe to topics
data_topic = "{}/coord".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.message_callback_add(data_topic, data)


# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()