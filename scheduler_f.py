from task import *
from private_task_1 import*
from private_task_2 import*
import time
relay_ON = [                                                                                                                                  
      None,
      [1, 6, 0, 0, 0, 255, 201, 138],  # Relay 1 ON
      [2, 6, 0, 0, 0, 255, 201, 185],  # Relay 2 ON
      [3, 6, 0, 0, 0, 255, 200, 104],  # Relay 3 ON
      [4, 6, 0, 0, 0, 255, 201, 223],  # Relay 4 ON
      [5, 6, 0, 0, 0, 255, 200, 14],   # Relay 5 ON
      [6, 6, 0, 0, 0, 255, 200, 61],   # Relay 6 ON
      [7, 6, 0, 0, 0, 255, 201, 236],  # Relay 7 ON
      [8, 6, 0, 0, 0, 255, 201, 19],    # Relay 8 ON,
    ]                                                                                                                                                  
                                                                                                                                                       
relay_OFF = [                                                                                                                                 
      None,
      [1, 6, 0, 0, 0, 0, 137, 202],    # Relay 1 OFF
      [2, 6, 0, 0, 0, 0, 137, 249],    # Relay 2 OFF
      [3, 6, 0, 0, 0, 0, 136, 40],     # Relay 3 OFF
      [4, 6, 0, 0, 0, 0, 137, 159],    # Relay 4 OFF
      [5, 6, 0, 0, 0, 0, 136, 78],     # Relay 5 OFF
      [6, 6, 0, 0, 0, 0, 136, 125],    # Relay 6 OFF
      [7, 6, 0, 0, 0, 0, 137, 172],    # Relay 7 OFF
      [8, 6, 0, 0, 0, 0, 137, 83]      # Relay 8 OFF
          ]

def setDevice(id, state): 
    if state == True:
        print(relay_ON[id], "--------")
    else:
        print(relay_OFF[id], "--------")
    print("Turn ", "On" if state == True else "Off", "RELAY ", id)

task = {"flow1":2,"flow2":2,"flow3":1, "water":2.5}
# def setDevice(id, state):
#     if id == 8: 
#         id = "Pump"
#     if state == True:
#         print("Turn on Flow",id)
#     else:
#         print("Turn off Flow",id)
def make_cycle(sche, task):
  t1 = task['flow1']
  t2 = task['flow1']+task['flow2']
  t3 = task['flow1']+task['flow2']+task['flow3']
  sche.SCH_Add_Task(lambda: setDevice(1, True), 0, 0) # Turn on flow 1
  sche.SCH_Add_Task(lambda: setDevice(1, False),t1*sche.TICK , 0) # Turn off flow 1
  sche.SCH_Add_Task(lambda: setDevice(2, True), t1*sche.TICK, 0) # Turn on flow 2
  sche.SCH_Add_Task(lambda: setDevice(2, False), t2*sche.TICK, 0) # Turn off flow 2
  sche.SCH_Add_Task(lambda: setDevice(3, True), t2*sche.TICK, 0) # Turn on flow 3
  sche.SCH_Add_Task(lambda: setDevice(3, False),t3*sche.TICK, 0) # Turn off flow 3
  sche.SCH_Add_Task(lambda: setDevice(8, True), t3*sche.TICK, 0) # Turn on pump
  sche.SCH_Add_Task(lambda: setDevice(8, False), (t3+task['water'])*sche.TICK, 0) # Turn off pump




def t():
    print("turn on ")
def t2():
    print("turn ff ")
class Scheduler:
    TICK = 100                  
    SCH_MAX_TASKS = 400          
    SCH_tasks_G = []            # List task (type list)
    current_index_task = 0      # total number task current 
                                                                                                                                                       
    def __int__(self):
      return
                                                                                                                                                       
    def SCH_Init(self):
      self.current_index_task = 0                                                                                                                      
      
    def SCH_Add_Task(self, pFunction, DELAY, PERIOD):
      if self.current_index_task < self.SCH_MAX_TASKS:
        aTask = Task(pFunction, DELAY*10 / self.TICK, PERIOD*10 /self.TICK)       
        aTask.TaskID = self.current_index_task
        self.SCH_tasks_G.append(aTask)                                                                                                                 
        self.current_index_task += 1   
        return self.current_index_task                                                                                                               
      else:
        print("PrivateTasks are full!!!")
        return -1
                                                                                                                                                       
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
    def SCH_Check(self):
       return self.current_index_task == 0
    def SCH_Size(self):
       return self.current_index_task
# sche =  Scheduler() # Turn on flow 1
# cnt =0
# sche.SCH_Add_Task(lambda: make_cycle(sche, task), 0, 1000)

# while True:
#     print(cnt/10)
#     sche.SCH_Update()
#     sche.SCH_Dispatch_Tasks()
#     time.sleep(0.1)
#     cnt+=1

#     if cnt%10 == 0: print("---")
    
