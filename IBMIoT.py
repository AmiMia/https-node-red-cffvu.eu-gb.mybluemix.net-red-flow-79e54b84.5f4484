import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#IBM Credentials
organization="unuahm"
deviceType="DeviceFire"
deviceId="F1"
authMethod="token"
authToken="Amiya_1Fireproject"
​
​
def myCommandCallback(cmd):
        print("Command received: %s." %cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='lighton':
                print("Light is on.")
        elif i=='lightoff':
                print("Light is off.")
        elif i=='fanoff':
                print("Fan is switched off.")
        elif i=='fanon':
                print("Fan is switched on.")
        

​
try:
        deviceOptions={"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli=ibmiotf.device.Client(deviceOptions)
        
except Exception as e:
	print("Caught exception while connecting device: %s." %str(e))
	sys.exit()
​
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
​
while True:
        
        temp=random.randint(-20,110)
        gas=random.randint(1,100)
        #Send values to IBM
        data={'Temperature': temp, 'Gas': gas}
        #print
        def myOnPublishCallback():
            print ("Published Temperature = %s C" %temp, "Gas = %s %%" %gas, "to IBM Watson")
       
        success=deviceCli.publishEvent("CFFVU", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoT.")
        time.sleep(4)

deviceCli.commandCallback=myCommandCallback
​
# Disconnect the device and application from the cloud
deviceCli.disconnect()
       


