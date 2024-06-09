import json
import time
import constants
import math
from userScheduler import *

def processParameter(schedule):
    # Dictionary to map garden names to relay codes
    garden_name_to_code = {
        "farm1": 4,
        "farm2": 5,
        "farm3": 6
    }
    
    # Change garden name to relay code
    schedule["gardenName"] = garden_name_to_code.get(schedule["gardenName"], schedule["gardenName"])
    
    # List of keys to ensure are integers
    int_keys = ["flow1", "flow2", "flow3", "pumpIn", "startTime", "stopTime"]
    
    # Ensure parameter true data type
    for key in int_keys:
        schedule[key] = int(schedule[key])



def handle_payload(payload):
    try:
        data = json.loads(payload)                                                                                                                     
        id = data["_id"]
        data['isDone'] = False
                                                                                                                                                       
        processParameter(data)                                                                                                               
                                                                                                                                                       
        if data['schedulerName'] == "oneshot" or data['stopTime'] == -1:
            US.addOneShotScheduler(data)                                                                                                               
            US.scheduler[id] = data                                                                                                                    
        else:
            US.scheduler[id] = data                                                                                                                    
            # print("-----------ALL SCHEDULES-----------")
            # print(US.scheduler)
            US.removeFromActiveScheduler(id) #Xóa ra khỏi active_scheduler khi cập nhật/ nếu thêm mới thì k có trong active nên k làm gì
            US.updateActiveScheduler()                                                                                                                 
            # print("----------------ACTIVE--------------")
            # print(US.active_scheduler)
            US.updatePredictScheduler()                                                                                                                
            # print("----------------PREDICT--------------")
            # print(US.predict_scheduler)
            print(f"Schedule {id} added/updated.")
            #US.predictTasks()
            #print(US.active_scheduler)
        try:
            return data['ack']
        except KeyError:
            return "None"                                                                     
        
    except json.JSONDecodeError:
        print("Failed to decode payload")
def deleteSchedule(payload):
    try:
        data = json.loads(payload)
        id = data["_id"]
        isSuccess = US.scheduler.pop(id, "No data")
        if isSuccess == "No data":
            print("The Schedule does not exist")
        else:
            US.removeFromActiveScheduler(id) #Xóa ra khỏi active_scheduler khi cập nhật/ nếu thêm mới thì k có trong active nên k làm gì
            US.updateActiveScheduler()
            
            print(f"Schedule {id} deleted.")
        #US.predictTasks()
        #print(US.active_scheduler)
        try:
            return data['ack']
        except KeyError:
            return "None" 
    except json.JSONDecodeError:
        print("Failed to decode payload")
def getTime(type):
        # Get current time in seconds
        current_time = time.time()

        # Convert seconds to struct_time object
        local_time = time.localtime(current_time)

        # Extract hour and minute
        hour = local_time.tm_hour
        minute = local_time.tm_min

        # Format the time string (optional)
        time_string = f"{hour:02d}:{minute:02d}"

        #print(time_string)  # Output: Current hour:minute in 00:00 format
        if type == "int":
            return hour*60 + minute
        elif type == "string":
            return time_string

def compare_times(start_time, stop_time):

    # Convert times to integers (in minutes)
    start_hour, start_minute = map(int, start_time.split(":"))
    stop_hour, stop_minute = map(int, stop_time.split(":"))
    start_time_in_minutes = start_hour * 60 + start_minute
    stop_time_in_minutes = stop_hour * 60 + stop_minute

    # Consider wrapping around midnight
    return start_time_in_minutes <= stop_time_in_minutes

def calculate_loads(schedule):
    schedule["loads"] = schedule["flow1"]*constants.TIME_FLOW1 + schedule["flow2"]*constants.TIME_FLOW2 + schedule["flow3"]*constants.TIME_FLOW3 + schedule["pumpIn"]*constants.TIME_PUMP*2

def calculate_priority(schedule):
    current_time = getTime("int")
    stop_time = int(schedule["stopTime"])
    
    #check 
    schedule["priority"] = (stop_time-current_time)*60 - schedule["loads"]
def calculate_cycle(schedule):
    schedule["cycle"] = round(schedule["pumpIn"]/constants.TIMEOUT)
def estimateSchedule(schedule):
    calculate_loads(schedule)                                                                                                                          
    if schedule["schedulerName"] == "oneshot":
        schedule["priority"] = 0
    else:
        calculate_priority(schedule)                                                                                                                   
    calculate_cycle(schedule)                                                                                                                          
    return schedule