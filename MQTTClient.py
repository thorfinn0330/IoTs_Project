from Adafruit_IO import MQTTClient
from constants import*
import sys
import time
import json
import handleData

# Add a new task

class MQTTClientHelper:
    def  __init__(self, _isUpdated):
        self.isUpdated = _isUpdated
        self.mqttClient = MQTTClient(AIO_USERNAME, AIO_KEY)
        self.mqttClient.on_connect = self.connected
        self.mqttClient.on_disconnect = self.disconnected
        self.mqttClient.on_message = self.message
        self.mqttClient.on_subscribe = self.subcribe
        self.mqttClient.connect()
        self.mqttClient.loop_background()
                
    def setFlag(self, state):
        self.isUpdated = state


    def connected(self, client):
        print("Connected successfully")
        for topic in AIO_FEED_ID:
            client.subscribe(topic)

    def subcribe(self, client, userdata, mid, granted_qos):
        print("Subscribed successfully")

    def disconnected(client):
        print("Disconnected...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Received: " + payload + " , feed id: " + feed_id)
        handleData.handle_payload(payload[2:])

        
                

mqttClientHelper = MQTTClientHelper(False)

