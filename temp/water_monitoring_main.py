import PrivateTasks.private_task_1
import PrivateTasks.private_task_2
import PrivateTasks.main_ui_task
import PrivateTasks.led_blinky_task
import PrivateTasks.water_monitoring_task
import PrivateTasks.rapido_server_task
import Utilities.modbus485
from Scheduler.scheduler import  *
from Utilities.softwaretimer import *
from Utilities.modbus485 import *
import time

ser = serial.Serial(port="COM7", baudrate=9600)
m485 = Utilities.modbus485.Modbus485(ser)
watermonitoring_timer = softwaretimer()

scheduler = Scheduler()
scheduler.SCH_Init()
soft_timer = softwaretimer()

task1 = PrivateTasks.private_task_1.Task1()
task2 = PrivateTasks.private_task_2.Task2()

ledblink = PrivateTasks.led_blinky_task.LedBlinkyTask(soft_timer)

watermonitoring = PrivateTasks.water_monitoring_task.WaterMonitoringTask(watermonitoring_timer, m485)
main_ui = PrivateTasks.main_ui_task.Main_UI(watermonitoring)
rapidoserver = PrivateTasks.rapido_server_task.RapidoServerTask()

#scheduler.SCH_Add_Task(task1.Task1_Run, 1000,2000)
#scheduler.SCH_Add_Task(task2.Task2_Run, 1000,4000)
# scheduler.SCH_Add_Task(soft_timer.Timer_Run, 1, 1)
# scheduler.SCH_Add_Task(ledblink.LedBlinkyTask_Run, 1, 1)


scheduler.SCH_Add_Task(main_ui.UI_Refresh, 1, 100)

scheduler.SCH_Add_Task(watermonitoring_timer.Timer_Run, 1, 100)
#scheduler.SCH_Add_Task(rapidoserver.uploadData, 1, 1000)
scheduler.SCH_Add_Task(watermonitoring.WaterMonitoringTask_Run, 1, 1)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()

    time.sleep(0.1)