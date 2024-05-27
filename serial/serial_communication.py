import serial.tools.list_ports
import time
import random
import numpy as np
                                                                                                                                                       
mess = ""
class SerialCommunicate:
  def __init__(self, RSport, RSbaudrate, USBport="COM3"):
    self.RSport = RSport                                                                                                                               
    self.RSbaudrate = RSbaudrate                                                                                                                       
    self.USBport = USBport                                                                                                                             
    self.current_time = time.time()                                                                                                                    
    self.relay_ON = [                                                                                                                                  
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
                                                                                                                                                       
    self.relay_OFF = [                                                                                                                                 
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
    
    self.relay_Distance = [                                                                                                                            
      [9, 3, 0, 5, 0, 1, 149, 67],                                                                                                                     
      [12, 3, 0, 5, 0, 1, 149, 22]                                                                                                                     
    ]                                                                                                                                                  
    self.relay_status= [None, False, False, False, False, False, False, False, False, False, False]
    self.sensor_data = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]                                                                                      
    
    self.serRS = serial.Serial(port = self.RSport, baudrate = self.RSbaudrate)                                                                         
    
  def read_distance(self, relayID):
    # self.serRS.write(self.relay_Distance[relayID])
    # time.sleep(0.1)
    # bytesToRead = self.serRS.inWaiting()
    # if bytesToRead > 0:
    #   out = self.serRS.read(bytesToRead)
    #   data_array = [b for b in out]
    #   if len(data_array) >= 7:
    #     array_size = len(data_array)
    #     current_distance = data_array[array_size - 4] * 256 + data_array[array_size - 3]
    #     return current_distance # or / 100
    #   else:
    #     return -1
    # else:
    #   return 0
    
    # distance = int(input("Enter the current distance: \n"))
    # return distance
    return 2500
  def read_sensor(self):
    
    humi = -1.0                                                                                                                                        
    update_time = time.time()                                                                                                                          
    elapsed_time = update_time - self.current_time                                                                                                     
    # print(elapsed_time)
                                                                                                                                                       
    if elapsed_time > 60*10:
        humi = round(random.uniform(62.0, 63.0), 1)                                                                                                    
    else:
        humi = round(random.uniform(60.0, 61.0), 1)                                                                                                    
    temp = round(random.uniform(28.0, 29.0), 1)                                                                                                        
    # humi = round(random.uniform(60.0, 64.0), 0)
    ph = round(random.uniform(4.0, 4.2), 1)                                                                                                            
    ec = round(random.uniform(1.8, 2.1), 1)                                                                                                            
    n = round(random.uniform(20.0, 75.0), 1)                                                                                                           
    p = round(random.uniform(10.0, 20.0), 1)                                                                                                           
    k = round(random.uniform(2.0, 6.0), 1)                                                                                                             
    
    self.sensor_data = [temp, humi, ph, ec, n, p, k]                                                                                                   
    result = self.sensor_data                                                                                                                          
    return result
                                                                                                                                                       
      
  def control_relay(self, relayID, state):
    # print(relayID, self.relay_status[relayID])
    if state and not self.relay_status[relayID]:
      self.serRS.write(self.relay_ON[relayID])                                                                                                         
      self.serial_read_data()                                                                                                                          
      self.relay_status[relayID] = True
      print('Turn on relay')
    elif not state and self.relay_status[relayID]:
      self.serRS.write(self.relay_OFF[relayID])                                                                                                        
      self.serial_read_data()                                                                                                                          
      self.relay_status[relayID] = False
      print('Turn off relay')
      
  def turn_off_all(self):
    for i in range(1, 9):
      self.serRS.write(self.relay_OFF[i])                                                                                                              
      self.serial_read_data()                                                                                                                          
      self.relay_status[i] = False
      print('Relay: ', i, " - ", self.relay_status[i])
  
  def serial_read_data(self):
    bytesToRead = self.serRS.inWaiting()                                                                                                               
    if bytesToRead > 0: 
      out = self.serRS.read(bytesToRead)                                                                                                               
      data_array = [b for b in out]
      # print(data_array, len(data_array))
      if len(data_array) >= 7:
        array_size = len(data_array)                                                                                                                   
        value = data_array[array_size - 4] * 256 + data_array[array_size - 3]                                                                          
        return value
      else:
        return -1
    return 0