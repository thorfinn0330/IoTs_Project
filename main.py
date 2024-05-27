import time
import MQTTClient
import handleData
import CM4Scheduler
import userScheduler

if __name__ == "__main__":
    cnt =0
    CM4Scheduler.scheduler.SCH_Add_Task(userScheduler.US.updateActiveScheduler, 0, 1500)
    while 1:
    # while (not userScheduler.US.isEmptyTask()) :
    #     print(1)
    #     task = userScheduler.US.makeTask()
    #     CM4Scheduler.add_new_fsm_task(CM4Scheduler.scheduler, task)
        
    #     userScheduler.US.printL()
    #     while not CM4Scheduler.scheduler.getState():
        if (not userScheduler.US.isEmptyTask()) and (userScheduler.US.isDoneTask()) and (userScheduler.US.active_scheduler[0]['loads']>0):
            task = userScheduler.US.makeTask()
            CM4Scheduler.add_new_fsm_task(CM4Scheduler.scheduler, task)
            for s in userScheduler.US.active_scheduler:
                print(s["schedulerName"], s)

        CM4Scheduler.scheduler.SCH_Update()
        CM4Scheduler.scheduler.SCH_Dispatch_Tasks()
        time.sleep(0.1)
        cnt += 1

        if cnt % 10 == 0:
            print(cnt/10, "---")
    