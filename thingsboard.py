import serial.tools.list_ports
import paho.mqtt.client as mqttclient
import time
import json
import random

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "xMvVEmhpVjVrDSJDWnyI"

print("here")

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def on_message(client, userdata, msg):
    print("topic: ", msg.topic, " message: ", str(msg.payload) )


def recv_message(client, userdata, message):
    # print("Received: ", message.payload.decode("utf-8"))
    jsonobj = json.loads(message.payload)
    keys = jsonobj.keys()
    print("Received: ", keys, " | ")
    for key in keys:
        print(key)
        
   
def connected(client, usedata, flags, rc):
    if rc == 0:
        client.subscribe("v1/devices/me/attributes")
        print("Connected to Thingsboard successfully")

    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

client.loop_forever()
