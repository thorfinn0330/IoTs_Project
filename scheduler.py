import time
import json
import random
from queue import Queue
import sys
from Adafruit_IO import MQTTClient

TIMEOUT = 5
TIME_FLOW1 = 1
TIME_FLOW2 = 1
TIME_FLOW3 = 1
TIME_PUMP = 10
task = {
    "flow1": 20,
    "flow2": 10,
    "flow3": 20,
    "water":200,
    "isActive": True,
    "areaSelector":4,
    "schedulerName": "LỊCH TƯỚI 1",
    "startTime": "18:30",
    "stopTime": "18:40"
}
jsonObj = {
    "task": ""
}
dataStrs = []

AIO_FEED_ID = ["schedule"]
AIO_USERNAME = "smartfarm0330"
AIO_KEY = "aio_EDId92jShTaHS0cxXtZK5D3PgQQz"

def connected(client):
    print("Connected successfully")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subcribe(client, userdata, mid, granted_qos):
    print("Subscribed successfully")

def disconnected(client):
    print("Disconnected...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Received: " + payload + " , feed id: " + feed_id)
    if feed_id == "schedule":
        dataStrs.append(payload)

   

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subcribe
client.connect()
client.loop_background()
def getTime():
    # Get current time in seconds
    current_time = time.time()

    # Convert seconds to struct_time object
    local_time = time.localtime(current_time)

    # Extract hour and minute
    hour = local_time.tm_hour
    minute = local_time.tm_min

    # Format the time string (optional)
    time_string = f"{hour:02d}:{minute:02d}"

    print(time_string)  # Output: Current hour:minute in 00:00 format
    return hour, minute, time_string
def compare_times(start_time, stop_time):
  """Compares two times in H:M format.

  Args:
      start_time: The start time in H:M format (e.g., "18:30").
      stop_time: The stop time in H:M format (e.g., "18:40").

  Returns:
      True if the start time is before the stop time, False otherwise.
  """

  # Convert times to integers (in minutes)
  start_hour, start_minute = map(int, start_time.split(":"))
  stop_hour, stop_minute = map(int, stop_time.split(":"))
  start_time_in_minutes = start_hour * 60 + start_minute
  stop_time_in_minutes = stop_hour * 60 + stop_minute

  # Consider wrapping around midnight
  if start_time_in_minutes > stop_time_in_minutes:
    return False
  else:
    return True
def calculate_loads(task):
    task["loads"] = task["flow1"]*TIME_FLOW1 + task["flow2"]*TIME_FLOW2 + task["flow3"]*TIME_FLOW3 + task["water"]*TIME_PUMP*2
def calculate_priority(task):
    h, m , strTime= getTime()
    sh, sm = task["stopTime"].split(":")
    sh = int(sh)
    sm = int(sm)
    #check 
    task["priority"] = (sh-h)*3600 + (sm-m)*60 - task["loads"]
    # if not compare_times(task["startTime"], strTime):
    #     task["priority"] = -task["priority"]
def sort_schedules(schedules):
    return sorted(schedules, key=lambda task: task["priority"])
def taskPerCycle(task, schedule, cycle):
    task["flow1"] = schedule["flow1"]/cycle
    task["flow2"] = schedule["flow2"]/cycle
    task["flow3"] = schedule["flow3"]/cycle
    task["water"] = schedule["water"]/cycle

    schedule["flow1"] -= task["flow1"]
    schedule["flow2"] -= task["flow2"]
    schedule["flow3"] -= task["flow3"]
    schedule["water"] -= task["water"]
def makeTask(schedule):
    task = {"flow1":0,"flow2":0,"flow3":0, "water":0}
    if schedule["water"] < TIMEOUT:
        taskPerCycle(task, schedule, 1)
    else:
        cycle = schedule["water"]/TIMEOUT
        taskPerCycle(task, schedule, cycle)

    return task


dataStr1 = '{"flow1":10,"flow2":10,"flow3":30, "water":7.5,"isActive":true,"areaSelector":4,"schedulerName":"LỊCH TƯỚI 1","startTime":"10:30","stopTime":"19:40"}'
dataStr2 = '{"flow1":20,"flow2":30,"flow3":50, "water":20,"isActive":true,"areaSelector":4,"schedulerName":"LỊCH TƯỚI 2","startTime":"10:30","stopTime":"19:30"}'
#dataStr3 = '{"flow1":20,"flow2":30,"flow3":40, "water":300,"isActive":true,"areaSelector":4,"schedulerName":"LỊCH TƯỚI 3","startTime":"10:20","stopTime":"14:30"}'

# task = json.loads(dataStr)
# task["loads"] =  (task["flow1"]+task["flow2"]+task["flow3"]+task["water"])
# task["cycle"] = task["water"]/TIMEOUT

# print(type(task), ": ", task)
# print(json.dumps(task))
# jsonObj["task"] =task 


# Tạo danh sách dataStr
# dataStrs.append(dataStr1)
# dataStrs.append(dataStr2)
#dataStrs.append(dataStr3)

def main():
    
    h, m, strTime = getTime()
   


    # Chuyển đổi dataStr sang JSON
    
    while True:
        tasks =[]
        schedules = []
        for dataStr in dataStrs:
            task = json.loads(dataStr)
            calculate_loads(task)
            calculate_priority(task)
            task["cycle"] = round(task["water"]/TIMEOUT)

            schedules.append(task)

        # Sắp xếp lịch trình
        sorted_schedules = sort_schedules(schedules)
        q = []

        # In lịch trình đã được sắp xếp
        for schedule in sorted_schedules:
            if compare_times(schedule["startTime"],strTime):
                q.append(schedule)
            print(schedule["schedulerName"], schedule["startTime"], schedule["priority"], schedule["loads"])
        print("---Task---")

        i=0
        while len(q) > 0:
            i +=1
            schedule = q.pop(0)
            task = makeTask(schedule)
            tasks.append(task)
            print("task ",i,": ",schedule["schedulerName"], task)
            print("---")
            calculate_loads(schedule)
            calculate_priority(schedule)
            if(schedule["loads"] > 0):
                q.append(schedule)
            
               
            q = sort_schedules(q)
            #print(q)
        
        i = 1
        for task in tasks:
        
            print("Task ",i,": ",task)
            i+=1
        time.sleep(10)

if __name__ == '__main__':
    main()