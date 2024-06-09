import time
from constants import *
from userScheduler import*
from MQTTClient import*
from enum import Enum
from serialCommunication import*
from task import*

class CM4Scheduler:
    TICK = 100
    SCH_MAX_TASKS = 400
    SCH_tasks_G = []  # List of tasks
    current_index_task = 0  # Total number of current tasks

    def __init__(self):
        self.current_index_task = 0
        self.success = True

    def SCH_Init(self):
        self.current_index_task = 0

    def SCH_Add_Task(self, pFunction, DELAY, PERIOD):
        if self.current_index_task < self.SCH_MAX_TASKS:
            aTask = Task(pFunction, DELAY * 10 / self.TICK, PERIOD * 10 / self.TICK)
            aTask.TaskID = self.current_index_task
            self.SCH_tasks_G.append(aTask)
            self.current_index_task += 1
            return self.current_index_task
        else:
            print("PrivateTasks are full!!!")
            return -1

    def SCH_Update(self):
        for i in range(len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].Delay > 0:
                self.SCH_tasks_G[i].Delay -= 1
            else:
                self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period
                self.SCH_tasks_G[i].RunMe += 1

    def SCH_Dispatch_Tasks(self):
        deleteArr = []
        for i in range(len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].RunMe > 0:
                self.SCH_tasks_G[i].RunMe -= 1
                self.SCH_tasks_G[i].pTask()
                if self.SCH_tasks_G[i].Period == 0:
                    deleteArr.append(self.SCH_tasks_G[i])
        for task in deleteArr:
            self.SCH_Delete(task)

    def SCH_Delete(self, aTask):
        if aTask in self.SCH_tasks_G:
            self.SCH_tasks_G.remove(aTask)
            self.current_index_task -= 1

    def SCH_Delete_All(self):
        self.SCH_tasks_G.clear()
        self.current_index_task = 0

    def SCH_GenerateID(self):
        return -1

    def SCH_Check(self):
        return self.current_index_task == 0

    def SCH_Size(self):
        return self.current_index_task
    def setState(self, state):
        self.success = state
    def getState(self):
        return self.success
class FSM:
   
    def __init__(self, scheduler, task):
        self.scheduler = scheduler
        self.task = task
        self.state = INIT
        self.success = False
        self.timeout = False
        self.t1 = task['flow1']
        self.t2 = task['flow2']
        self.t3 = task['flow3']
        self.t4 = task['pumpIn']
        self.selector = task['gardenName']

    def process(self):
        if self.timeout == True:
            self.timeout = False
        if self.state == INIT:
            # self.success = self.setDevice(1, True, self.t1)
            self.scheduler.SCH_Add_Task(US.startTask, 0,0)
            self.scheduler.SCH_Add_Task(lambda: self.scheduler.setState(False), 0, 0)

            self.scheduler.SCH_Add_Task(lambda: self.setDevice(1, True,self.t1), 0, 0)
            mqttClientHelper.publishState(self.task, "flow1", True)

        elif self.state == MIXER_1 :
            # if self.success:
                mqttClientHelper.publishState(self.task, "flow1", False)
                self.scheduler.SCH_Add_Task(lambda: self.setDevice(1, False,0), 0, 0)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(2, True, self.t2), 0, 0)
                mqttClientHelper.publishState(self.task, "flow2", True)

        elif self.state == MIXER_2 :
            # if self.success:
                mqttClientHelper.publishState(self.task, "flow2", False)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(2, False,0), 0, 0)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(3, True, self.t3), 0, 0)
                mqttClientHelper.publishState(self.task, "flow3", True)
        elif self.state == MIXER_3:
            # if self.success:
                mqttClientHelper.publishState(self.task, "flow3", False)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(3, False,0), 0, 0)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(7, True, self.t4), 0, 0)
                mqttClientHelper.publishState(self.task, "pumpIn", True)
        elif self.state == PUMP_IN :
            # if self.success:
                mqttClientHelper.publishState(self.task, "pumpIn", False)

                self.scheduler.SCH_Add_Task(lambda: self.setDevice(7, False,0), 0, 0)
                self.scheduler.SCH_Add_Task(lambda: self.setDevice(self.selector, True, 1), 0, 0)
                
        elif self.state == SELECTOR :
            # if self.success:
                self.scheduler.SCH_Add_Task(lambda: self.setDevice(self.selector, False,0), 0, 0)
                self.scheduler.SCH_Add_Task(lambda: self.setDevice(8, True, self.t4), 0, 0)
                mqttClientHelper.publishState(self.task, "pumpOut", True)
        elif self.state == PUMP_OUT :
            # if self.success:
                mqttClientHelper.publishState(self.task, "pumpOut", False)
                self.scheduler.SCH_Add_Task(lambda: self.setDevice(8, False,0), 0, 0)
                self.success = True
                self.scheduler.SCH_Add_Task(lambda: self.scheduler.setState(True), 0, 0)
                self.next_state()
                
        elif self.state == FINAL :
                self.scheduler.SCH_Add_Task(US.doneTask,0,0)
                print("END TASK: ", self.task)
                mqttClientHelper.publishDoneTask(self.task)
                self.next_state()
            #     self.success = self.setDevice(2, True, self.t2)
            # else:
            #     self.error("Failed to turn on Flow 1")
        # elif self.state == 2:
        #     if self.success:
        #         self.scheduler.SCH_Add_Task(lambda: self.setDevice(2, False), 0, 0)
        #         self.success = self.setDevice(3, True, self.t3)
        #     else:
        #         self.error("Failed to turn on Flow 2")
        # elif self.state == 3:
        #     if self.success:
        #         self.scheduler.SCH_Add_Task(lambda: self.setDevice(3, False), 0, 0)
        #         self.success = self.setDevice(8, True, self.t4)
        #     else:
        #         self.error("Failed to turn on Flow 3")
        # elif self.state == 4:
        #     if self.success:
        #         self.scheduler.SCH_Add_Task(lambda: self.setDevice(8, False), 0, 0)
        #         self.state = 5
        #     else:
        #         self.error("Failed to turn on Pump")
    def setTimeOut(self):
        self.timeout = True
        self.next_state()

    def setDevice(self, id, state, timeout):
        if state:
            command = relay_ON[id]
        else:
            command = relay_OFF[id]
        # Simulate sending command and getting response
        if timeout != 0:
            self.scheduler.SCH_Add_Task(lambda: self.setTimeOut(), timeout* self.scheduler.TICK, 0)
        RS485.setDevice(id, state)
        print(f"Sending command to {'turn ON' if state else 'turn OFF'} relay {id}: {command}")
        response = True  # Replace with actual communication result
        return response

    def next_state(self):
        self.state += 1
        if self.state < 8:
            self.process()

    def error(self, message):
        print(message)
        self.state = 8  # Terminate the FSM


def add_new_fsm_task(scheduler, task):
    fsm = FSM(scheduler, task)
    fsm.process()

scheduler = CM4Scheduler()

# # Initial task
# task = {"flow1": 1, "flow2": 2, "flow3": 3, "pumpIn": 2.5}
# scheduler = CM4Scheduler()
# add_new_fsm_task(scheduler, task)

# cnt = 0
# isTask2= False
# while cnt < 10000:  # Simulate 10 seconds of operation
#     print(cnt / 10)
#     scheduler.SCH_Update()
#     scheduler.SCH_Dispatch_Tasks()
#     time.sleep(0.1)
#     cnt += 1
#     if cnt % 10 == 0:
#         print("---")
#     if cnt >= 100 and isTask2 == False:
#         task2 = {"flow1": 3, "flow2": 2, "flow3": 1, "water": 5}
#         add_new_fsm_task(scheduler, task2)
#         print("-------------------------------------")

#         isTask2 = True