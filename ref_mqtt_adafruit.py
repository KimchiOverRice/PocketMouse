from umqtt1 import MQTTClient
import network
import sys
import time
from keys import IOkey 

adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'kimia' # CHANGE THIS WITH YOUR OWN!
adafruitAioKey = IOkey # CHANGE THIS WITH YOUR OWN!
feedName = "kimia/feeds/mouse" # CHANGE THIS WITH YOUR OWN! (also known as "MQTT by key")
    
'''Function with everything needed to publish a message
Simply call this function anytime you want to publish a message.
The input is the message (string) you want to send.'''
def publish_mqtt(message):
    # Check wifi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ip = wlan.ifconfig()[0]
    if ip == '0.0.0.0':
        print("no wifi connection")
        sys.exit()
    else:
        #print("connected to WiFi at IP", ip)
        pass

    # Set up Adafruit connection
    global adafruitIoUrl
    global adafruitUsername
    global adafruitAioKey
    global feedName
    #print("Connecting to Adafruit")
    mqtt = MQTTClient(client_id='esp32',server=adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
    mqtt.connect()
    #print("Connected!")

    # Publish Message
    global feedName
    mqtt.publish(feedName, message)
    print("Published {} to {}.".format(message, feedName))
    
    
def receive_mqtt():
    def sub_cb(topic, msg):
        global incoming_message
        print((topic, msg))
        incoming_message = msg
    
    # Check wifi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ip = wlan.ifconfig()[0]
    if ip == '0.0.0.0':
        print("no wifi connection")
        sys.exit()
    else:
        #print("connected to WiFi at IP", ip)
        pass
        
    # Set up Adafruit connection
    global adafruitIoUrl
    global adafruitUsername
    global adafruitAioKey
    global feedName
    #print("Connecting to Adafruit")
    mqtt = MQTTClient(client_id='esp32',server=adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
    mqtt.connect()
    time.sleep(0.5)
    #print("Connected!")
    
    # Receive message
    mqtt.set_callback(sub_cb)
    mqtt.subscribe(feedName)
    mqtt.wait_msg()
    print("Received: {} from {}.".format(incoming_message, feedName))
    return incoming_message

''' Examples'''

'''1. Publish a message: '''
print('Publishing message...')
publish_mqtt("Hello Adafruit World")

'''2. Receive a message: '''
print('Looking for message...')
try:
    incoming_message = receive_mqtt()
except:
    print("No message received. Please try again.")
