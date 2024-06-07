from Adafruit_IO import MQTTClient
from constants import*
import sys
import time
import json
import handleData
from serialCommunication import*
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
        header = payload[0]
        if header == HEADER_SERVER_SEND_TASK:
            ack = handleData.handle_payload(payload[2:])
            self.mqttClient.publish("schedule", f"{HEADER_GATEWAY_SEND_ACK}:{ack}")
        elif header == HEADER_SERVER_DELETE_TASK:
            ack = handleData.deleteSchedule(payload[2:])
            self.mqttClient.publish("schedule", f"{HEADER_GATEWAY_SEND_ACK}:{ack}")

    def publishSensorsValue(self):
        temp, hum = ser.readAllSensors()        
        message = f"{HEADER_GATEWAY_SEND_SENSOR_VALUE}:{temp}:{hum}"
        self.mqttClient.publish("schedule", message)
    def publishDoneTask(self, task):
        message = f"{HEADER_GATEWAY_SEND_TASK_STATUS}:{task}"
        self.mqttClient.publish("schedule", message)            
    def publishState(self, task, key, isStart):
        _id = task["id"]
        if key == "pump_in" or key == "pump_out":
            value = task["water"]
        else:
            value = task[key]
        
        if isStart:
                value = 0
        message = f"{HEADER_GATEWAY_SEND_TASK_STATUS}:{_id}:{key}:{value}"
        self.mqttClient.publish("schedule", message)     
mqttClientHelper = MQTTClientHelper(False)

