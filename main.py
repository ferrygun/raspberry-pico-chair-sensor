import netman
import time
from umqttsimple import MQTTClient
from time import sleep
from machine import Pin, PWM
import utime

country = 'SG'
ssid = 'SSID'
password = 'PASSWORD'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = 'HOMEASSISTANT_IP_ADDR'
client_id = 'PicoW'
user_t = 'MQTT_USERID'
password_t = 'MQTT_PWD'
topic_pub = 'hello'

last_message = 0
message_interval = 5
counter = 0

analog_value = machine.ADC(28)

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def callback(topic, msg): 
    print((topic, msg))
    msg = msg.decode('UTF-8')
    if msg == 'on':
        pwm.duty_ns(MIN)
        utime.sleep(1)
        pwm.duty_ns(MID)
    if msg == 'off':
        pwm.duty_ns(MAX)
        utime.sleep(1)
        pwm.duty_ns(MID)
    
while True:
    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()
    
    while True:
        try:
            reading = analog_value.read_u16()/1000
            print("ADC: ",round(reading))
            client.publish(topic_pub, msg=str(round(reading)))
            print('published')
            time.sleep(1)
        except:
            reconnect()
            pass
    client.disconnect()


