#Time out for RELAY
TIMEOUT = 5
TIME_FLOW1 = 1
TIME_FLOW2 = 1
TIME_FLOW3 = 1
TIME_PUMP = 10

#MQTT 
AIO_FEED_ID = ["schedule"]
AIO_USERNAME = "smartfarm0330"
AIO_KEY = "aio_FPNu49hP58ZDmuLsYzytS2lMo9IR"

#FSM State
INIT = 0
MIXER_1 = 1
MIXER_2 = 2
MIXER_3 = 3
PUMP_IN = 4
SELECTOR = 5
PUMP_OUT = 6
FINAL = 7
ERROR = 8

# RS485 lookup table 
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

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
