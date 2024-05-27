import time
import json
import random
from queue import Queue
from CM4Scheduler import *
from MQTTClient import *






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
    return task['loads']
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

def update_schedules(dataStrs, tasks):
    updated_schedules = []
    for dataStr in dataStrs:
        task = json.loads(dataStr)
        if task["isActive"]:
            updated_schedules.append(task)
        else:
            # Xóa các task của lịch trình không hoạt động nữa
            tasks = [t for t in tasks if t["schedulerName"] != task["schedulerName"]]
    return updated_schedules, tasks

def make_schedules_and_tasks():
    schedules =[]
    tasks = []
    _, _, strTime = getTime()
    for dataStr in dataStrs:
        print(dataStrs)
        task = json.loads(dataStr)
        calculate_loads(task)
        calculate_priority(task)
        task["cycle"] = round(task["water"]/TIMEOUT)

        schedules.append(task)

    # Sắp xếp lịch trình
    schedules = sort_schedules(schedules)
    q = []

    # In lịch trình đã được sắp xếp
    for schedule in schedules:
        if (compare_times(schedule["startTime"], strTime)) and (schedule["isActive"] == "True"):
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
    
    return schedules, tasks
mainSche = Scheduler()
def main():
    
    mainSche.SCH_Add_Task(lambda: setFlag(True), 0, 0)
    sche =  Scheduler()


    # Chuyển đổi dataStr sang JSON
    
    while True:
        tasks =[]
        schedules = []
        schedules, tasks = make_schedules_and_tasks()
        print(tasks)

            #print(q)
        
        i = 0
        cnt = 0
        loads = 0
        while len(tasks) > 0:
            print(cnt)
            
            if sche.SCH_Check():
                print(tasks)
                task = tasks[0]
                print("------Task ",i,": ",task)
                tasks.pop(0) 
                sche.SCH_Add_Task(lambda: make_cycle(sche, task), 0, 0)
                i+=1
                loads += calculate_loads(task)
            sche.SCH_Update()
            sche.SCH_Dispatch_Tasks()
            time.sleep(0.1) 
            cnt +=1
            print("size: ",sche.SCH_Size(), "-----")   
            if (sche.SCH_Size()==0) and (not isUpdated):
                schedules, tasks= make_schedules_and_tasks()
                setFlag(True)

            
        while sche.SCH_Size():
            print(cnt/10)
            sche.SCH_Update()
            sche.SCH_Dispatch_Tasks()
            time.sleep(0.1) 
            cnt +=1
        print("-----------------------Test end--------------------")    
        time.sleep(10)

if __name__ == '__main__':
    main()