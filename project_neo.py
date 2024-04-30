from machine import ADC, Pin, PWM, Timer
from neopixel import NeoPixel
from time import sleep, ticks_ms
import machine as ma

from umqtt.simple import MQTTClient
import network
import sys
from keys import sess
    

# Session information for MQTT communication
session = sess
BROKER = 'broker.hivemq.com'

# Set pins A0 and A2 for DAC and ADC respectively
xcontrol = Pin(34, mode=Pin.IN)
ycontrol = Pin(39, mode=Pin.IN)
led = Pin(13, mode=Pin.OUT)

# Set pin for the button on the joystick
swcontrol = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)

# Set variables for button debouncing
state = 0
last_time = ticks_ms()
index = 0
delay = 200
last_state = 0;

# Assign DAC and ADC converter objects to each pin
adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)

# ADC configs
adc_x.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_y.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_val_x = 0  # set val of ADC to dummy value to start off
adc_val_y = 0
joystick_on = True

'''
# Initialize NeoPixel
pwr = ma.Pin(2, ma.Pin.OUT)
pwr.value(1)
np = NeoPixel(Pin(0), ma.Pin.OUT)
'''

 # Report function to print counter value when ISR callback updated
def report(pin):
     global counter
     global state
     print('Counter = ' + str(counter))
     
def bhandler(pin):
     global counter
     global state
     global last_time
     global delay
     global t
     global joystick_on
     t = ticks_ms()
     state = swcontrol()
     if t - last_time > delay and state == 0:
         last_state = 0
         last_time = t
         joystick_on = not joystick_on
     else:
         last_state = 1

   
def position(timer):

    global adc_x
    global adc_y
    global joystick_on
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    
    topic = "{}/coord".format(session)
    data = "{},{},{}".format(adc_val_x, adc_val_y, joystick_on)
    try:
        mqtt.publish(topic, data)
    except:
        mqtt.connect()
        mqtt.publish(topic, data)
        
    print("send topic='{}' data='{}'".format(topic, data))
    print(ticks_ms())
    
    print('')


def NEO_cb(timer):
    global np
    global adc_x
    global adc_y
    global adc_val_x
    global adc_val_y
    global joystick_on
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    
    topic = "{}/coord".format(session)
    data = "{},{},{}".format(adc_val_x, adc_val_y, joystick_on)
    try:
        mqtt.publish(topic, data)
    except:
        mqtt.connect()
        mqtt.publish(topic, data)
        
    print("send topic='{}' data='{}'".format(topic, data))
    
    print('')

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

'''
np[0] = (10,0,0) # Start with NeoPixel OFF
np.write()
print('Neopixel RED')
'''   

swcontrol.irq(handler=bhandler,trigger=Pin.IRQ_FALLING)
t1 = Timer(4)
t1.init(period=700, mode=t1.PERIODIC, callback=position)
#t2 = Timer(3)
#t2.init(period=2000, mode=t2.PERIODIC, callback=NEO_cb)



sleep(30)
t1.deinit()
#t2.deinit()

        
