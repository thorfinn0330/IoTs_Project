from task import *
from private_task_1 import*
from private_task_2 import*
import time
task = {"flow1":1,"flow2":2,"flow3":1, "water":5}
def setDevice(id, state):
    if id == 8: 
        id = "Pump"
    if state == True:
        print("Turn on Flow",id)
    else:
        print("Turn off Flow",id)
def make_cycle(sche, task):
  sche.SCH_Add_Task(lambda: setDevice(1, True), 0, 0) # Turn on flow 1
  sche.SCH_Add_Task(lambda: setDevice(1, False), 100, 0) # Turn off flow 1
  sche.SCH_Add_Task(lambda: setDevice(2, True), 100, 0) # Turn on flow 2
  sche.SCH_Add_Task(lambda: setDevice(2, False), 200, 0) # Turn off flow 2
  sche.SCH_Add_Task(lambda: setDevice(3, True), 200, 0) # Turn on flow 3
  sche.SCH_Add_Task(lambda: setDevice(3, False),300, 0) # Turn off flow 3
  sche.SCH_Add_Task(lambda: setDevice(8, True), 300, 0) # Turn on pump
  sche.SCH_Add_Task(lambda: setDevice(8, False), 1300, 0) # Turn off pump




def t():
    print("turn on ")
def t2():
    print("turn ff ")
class Scheduler:
    TICK = 100                  
    SCH_MAX_TASKS = 40          
    SCH_tasks_G = []            # List task (type list)
    current_index_task = 0      # total number task current 
                                                                                                                                                       
    def __int__(self):
      return
                                                                                                                                                       
    def SCH_Init(self):
      self.current_index_task = 0                                                                                                                      
      
    def SCH_Add_Task(self, pFunction, DELAY, PERIOD):
      if self.current_index_task < self.SCH_MAX_TASKS:
        aTask = Task(pFunction, DELAY / self.TICK, PERIOD / self.TICK)       
        aTask.TaskID = self.current_index_task
        self.SCH_tasks_G.append(aTask)                                                                                                                 
        self.current_index_task += 1                                                                                                                   
      else:
        print("PrivateTasks are full!!!")
                                                                                                                                                       
    def SCH_Update(self):
      for i in range(0, len(self.SCH_tasks_G)):
        if self.SCH_tasks_G[i].Delay > 0:
          self.SCH_tasks_G[i].Delay -= 1                                                                                                               
        else:
          self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period                                                                                       
          self.SCH_tasks_G[i].RunMe += 1                                                                                                               
                    
                                                                                                                                                       
    def SCH_Dispatch_Tasks(self):
      deleteArr=[]                                                                                                                                     
      for i in range(0, len(self.SCH_tasks_G)):
        if self.SCH_tasks_G[i].RunMe > 0:
          self.SCH_tasks_G[i].RunMe -= 1                                                                                                               
          self.SCH_tasks_G[i].pTask()                                                                                                                  
          if self.SCH_tasks_G[i].Period == 0 :
            deleteArr.append(self.SCH_tasks_G[i])                                                                                                      
            # self.SCH_Delete(self.SCH_tasks_G[i])
            # self.SCH_Dispatch_Tasks()
            # break        
      for i in range(0,len(deleteArr)):
        self.SCH_Delete(deleteArr[i])                                  
    def SCH_Delete(self, aTask):
      if aTask in self.SCH_tasks_G:
        self.SCH_tasks_G.remove(aTask)                                                                                                                 
        self.current_index_task -= 1  
    
    def SCH_Detele_All(self):
      pass  
                                                                                                                                                       
    def SCH_GenerateID(self):
        return -1
sche =  Scheduler()
# sche.SCH_Add_Task(t,100,200)
# sche.SCH_Add_Task(t, 100, 0)  # Turn on flow 1
cnt =0
make_cycle(sche, task)
while True:
    print(cnt)
    sche.SCH_Update()
    sche.SCH_Dispatch_Tasks()
    time.sleep(1)
    cnt+=1
    print("---")
    
