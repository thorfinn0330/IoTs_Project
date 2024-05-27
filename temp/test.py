import json
str = '[{"_id":"662898b1023687c3d2779e0f","gardenName":"farm2","startTime":"1020","stopTime":"1050","cycle":"5","flow1":"70","flow2":"30","flow3":"30","pumpIn":"7000","isActive":"1","schedulerName":"Lịch tưới 2","__v":0},{"_id":"662898f3023687c3d2779e11","gardenName":"farm1","startTime":"420","stopTime":"450","cycle":"3","flow1":"20","flow2":"30","flow3":"30","pumpIn":"5000","isActive":"1","schedulerName":"Lịch tưới 1","__v":0}]'
data = json.loads(str)
strData = []
print(data, len(data))

for i in range(0,len(data)):
    print("--------------------", data[i]['schedulerName'], "--------------------")
    print(data[i])
    strData.append(data[i])
    print("-------------")

newStr = '{"_id":"662898b1023687c3d2779e0f","gardenName":"farm2","startTime":"1020","stopTime":"1050","cycle":"5","flow1":"70","flow2":"30","flow3":"30","pumpIn":"7000","isActive":"1","schedulerName":"Lịch tưới 2222","__v":0}'
strData.append(newStr)

for i in strData:
    print("------", json.loads(i))