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

# Set variables for left and right click buttons
counter1 = 0
state1 = 0
last_time1 = ticks_ms()
button1 = Pin(15, mode=Pin.IN, pull=Pin.PULL_UP)
counter2 = 0
state2 = 0
last_time2 = ticks_ms()
button2 = Pin(32, mode=Pin.IN, pull=Pin.PULL_UP)

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
     global joystick_on
     global state
     print('Counter = ' + str(joystick_on))
     
     
def report1(pin):
     global counter1
     global state1
     print('Counter1 = ' + str(counter1))
# # Report function to print counter value when ISR callback updated
def report2(pin):
     global counter2
     global state2
     print('Counter2 = ' + str(counter2))
     
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
         
         topic = "{}/joystick".format(session)
         data = "{}".format(joystick_on)
         try:
             mqtt.publish(topic, data)
         except:
             mqtt.connect()
             mqtt.publish(topic, data)
        
         print("send topic='{}' data='{}'".format(topic, data))
     else:
         last_state = 1

# Button for 
def bhandler1(pin):
    global counter1
    global state1
    global last_time1
    global t1
    global delta_t1
    #counter += 1
    #report(button)
# 
#     # Part A 4. Insert here your debounce code (from lecture)
    state1 = button1()
    t1 = time.ticks_ms()
    delta_t1= t1-last_time1
    if state1 ==0 and delta_t1>50:
        last_state1 = 0
        last_time1 = t1
        counter1+= 1
        #report1(button1)
        
        topic = "{}/button".format(session)
        data = "{}".format('right')
        try:
            mqtt.publish(topic, data)
        except:
            mqtt.connect()
            mqtt.publish(topic, data)
        print("send topic='{}' data='{}'".format(topic, data))
        
    else:
        last_state1 = 1
    #led.value(last_state)
        
    
        
def bhandler2(pin):
    global counter2
    global state2
    global last_time2
    global t2
    global delta_t2
    #counter += 1
    #report(button)
# 
#     # Part A 4. Insert here your debounce code (from lecture)
    state2 = button2()
    t2 = time.ticks_ms()
    delta_t2= t2-last_time2
    if state2 == 0 and delta_t2>50:
        last_state2 = 0
        last_time2 = t2
        counter2+= 1
        #report2(button2)
        
        topic = "{}/button".format(session)
        data = "{}".format('left')
        try:
            # print('im trying')
            mqtt.publish(topic, data)
        except:
            mqtt.connect()
            mqtt.publish(topic, data)
        print("send topic='{}' data='{}'".format(topic, data))
        
    else:
        last_state2 = 1

def position(timer):

    global adc_x
    global adc_y
    global joystick_on
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    
    topic = "{}/coord".format(session)
    data = "{},{},{}".format(adc_val_x, adc_val_y, joystick_on)
    if joystick_on:
        try:
            mqtt.publish(topic, data)
        except:
            mqtt.connect()
            mqtt.publish(topic, data)
        
        print("send topic='{}' data='{}'".format(topic, data))
        print(ticks_ms())
    
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
button1.irq(handler=bhandler1,trigger=Pin.IRQ_FALLING) # Change the trigger to Pin.IRQ_RISING or Pin.IRQ_FALLING
button2.irq(handler=bhandler2,trigger=Pin.IRQ_FALLING) # Change the trigger to Pin.IRQ_RISING or Pin.IRQ_FALLING


sleep(30)
t1.deinit()
#t2.deinit()

        
