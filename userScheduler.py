import time
import constants
import handleData
import copy
class UserScheduler:
    def __init__(self):
        self.scheduler = {}
        self.active_scheduler = []
        self.predict_scheduler = []
        self.tasks = []
        self.cnt = 0
        self.in_progress = False
        
    def updateActiveScheduler(self):
        existing_schedules = {schedule['_id'] for schedule in self.active_scheduler}
        print("exist", existing_schedules)
        new_schedules = sorted(
            [
                handleData.estimateSchedule(copy.deepcopy(schedule))
                for schedule in self.scheduler.values()
                if schedule["isActive"] == "1" and 
                schedule["isDone"] == False and
                schedule["startTime"] >= handleData.getTime("int") and
                handleData.estimateSchedule(schedule)['loads'] > 0 and
                schedule['_id'] not in existing_schedules
            ],
            key=lambda schedule: schedule["priority"]
        )
        # print("new", new_schedules)

        # print("OLD", self.active_scheduler)
        self.active_scheduler.extend(new_schedules)
        # print("NEW", self.active_scheduler)

        # print("UPDATE CALL")
    def removeFromActiveScheduler(self, schedule_id):
        self.active_scheduler = [schedule for schedule in self.active_scheduler if schedule['_id'] != schedule_id]
    def addToActiveScheduler(self, schedule):
        self.active_scheduler.append(handleData.estimateSchedule(copy.deepcopy(schedule)))
        self.active_scheduler = sorted(self.active_scheduler, key=lambda schedule: schedule["priority"])
    def addOneShotScheduler(self, schedule):
        schedule = self.active_scheduler.append(handleData.estimateSchedule(copy.deepcopy(schedule)))
        schedule["priority"] = 0
        self.active_scheduler.append(schedule)
        self.active_scheduler = sorted(self.active_scheduler, key=lambda schedule: schedule["priority"])

    
    def updatePredictScheduler(self):
        self.predict_scheduler = []
        for id, schedule in self.scheduler.items():
            if (schedule["isActive"] == "True") and (handleData.compare_times(schedule["startTime"], handleData.getTime("string"))):
                temp_schedule = copy.deepcopy(schedule)
                if handleData.estimateSchedule(temp_schedule)['loads'] > 0:
                    self.predict_scheduler.append(handleData.estimateSchedule(temp_schedule))
        self.predict_scheduler = sorted(self.predict_scheduler, key=lambda schedule: schedule["priority"])
        # q=[]
        # for s in self.predict_scheduler:
        #     q.append(copy.deepcopy(s))
        i = 0
        while len(self.predict_scheduler) > 0:
            i +=1
            schedule = self.predict_scheduler.pop(0)
            task = self.makeTaskTemp(schedule)
            schedule = handleData.estimateSchedule(schedule)
            self.tasks.append(task)
            print("task ",i,": ",schedule["schedulerName"], task)
            print("---")
            
            if(schedule["loads"] > 0):
                self.predict_scheduler.append(schedule)
            
                
            self.predict_scheduler =sorted(self.predict_scheduler, key=lambda schedule: schedule["priority"])
    def predictTasks(self):
        q=[]
        for s in self.active_scheduler:
            q.append(copy.deepcopy(s))
        i = 0
        while len(q) > 0:
            i +=1
            schedule = q.pop(0)
            task = self.makeTaskTemp(schedule)
            schedule = handleData.estimateSchedule(schedule)
            self.tasks.append(task)
            print("task ",i,": ",schedule["schedulerName"], task)
            print("---")
            
            if(schedule["loads"] > 0):
                q.append(schedule)
            
                
            q =sorted(q, key=lambda schedule: schedule["priority"])
        

    def taskPerCycle(self, task, schedule, cycle):
        if cycle > 1:
            rate = constants.TIMEOUT/schedule['pumpIn']
        else:
            rate = 1
        task["flow1"] = schedule["flow1"]*rate
        task["flow2"] = schedule["flow2"]*rate
        task["flow3"] = schedule["flow3"]*rate
        task["pumpIn"] = schedule["pumpIn"]*rate
        task["id"] = schedule["_id"]
        task["gardenName"] = schedule["gardenName"]
        task["schedulerName"] = schedule["schedulerName"]
        schedule["flow1"] -= task["flow1"]
        schedule["flow2"] -= task["flow2"]
        schedule["flow3"] -= task["flow3"]
        schedule["pumpIn"] -= task["pumpIn"]
    def makeTaskTemp(self, schedule):
        task = {"flow1":0,"flow2":0,"flow3":0, "pumpIn":0}
        if schedule["pumpIn"] < constants.TIMEOUT:
            self.taskPerCycle(task, schedule, 1)
        else:
            cycle = round(schedule["pumpIn"]/constants.TIMEOUT)
            self.taskPerCycle(task, schedule, cycle)

        return task
    def makeTask(self):
        if self.isEmptyTask():
            pass
        else:
            self.cnt+=1
            print("___________")
            task = {"id":"", "schedulerName":"","flow1":0,"flow2":0,"flow3":0, "pumpIn":0}
            i=0
            while self.active_scheduler[i]["loads"] - 0 <= 0.0001:
                i+=1
            schedule = self.active_scheduler[i]
            if schedule["pumpIn"] <= constants.TIMEOUT:
                self.taskPerCycle(task, schedule, 1)
                #update complete schedule
                #
                #
                self.active_scheduler.pop(0)
                self.scheduler[schedule["_id"]]["isDone"] = True
            else:
                self.taskPerCycle(task, schedule, schedule['cycle'])
                self.active_scheduler[i] = handleData.estimateSchedule(schedule)
            print("TASK: ",self.cnt,"---", task)
            self.active_scheduler = sorted(self.active_scheduler, key=lambda schedule: schedule["priority"])
            return task
    def isEmptyTask(self):
        #print(f"Size of active scheduler {len(self.active_scheduler)}")
        if len(self.active_scheduler) >0:
            return False
        else:
            return True
    def isDoneTask(self):
        return not self.in_progress
    def doneTask(self):
        self.in_progress = False  
    def startTask(self):
        self.in_progress = True 
    def isReadyforNewTask(self):
        return (not self.isEmptyTask()) and (self.isDoneTask()) and (self.active_scheduler[0]['loads']>0)     
    def printL(self):
        print("________", self.active_scheduler)
US = UserScheduler()