# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 16:47:51 2021

@author: SmartBridgePC
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 15:10:05 2020

@author: SmartBridgePC
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #import the AWSIoTPython by using Pip install AWSIoTPythonSDk
import time,json#importing time and Json
import datetime
import random 

host = "a11psdqb7suj8h-ats.iot.ap-south-1.amazonaws.com"#Replace with AWS EndPoint
rootCAPath = "rootCA.pem" #Replace the directory with your Saved Root Certificate Location
certificatePath = "2abbf6b651-certificate.pem.crt"#Replace the directory with your Saved thing ertificate Location
privateKeyPath = "2abbf6b651-private.pem.key"#Replace the directory with your Saved private key Location
topic = "iot/topic"#Replace with your Topic Name


# Custom MQTT message callback this function is to retrive the Data from AWS IoT Core
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient("Divya")# replace with Client Name it Can be any string
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)


# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("iot/topic", 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0

while True:
        date=str (datetime.datetime.now()) 
        JSONPayload = {'id':"143",'sno': date,'temperature': random.randint(50,100), 'humidity': random.randint(1,100)} 
        print (json.dumps(JSONPayload))
        myAWSIoTMQTTClient.publish(topic,json.dumps(JSONPayload), 1)
        loopCount+=1
        time.sleep(5)
