from umqtt1 import MQTTClient
import network
import sys
import time

adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'kimia' # CHANGE THIS WITH YOUR OWN!
adafruitAioKey = 'aio_zWii02jK6Cuxd9qUZj9eucQkS5he' # CHANGE THIS WITH YOUR OWN!
feedName = "kimia/feeds/mouse" # CHANGE THIS WITH YOUR OWN! (also known as "MQTT by key")

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

try:
    incoming_message = receive_mqtt()
except:
    print("No message received. Please try again.")
