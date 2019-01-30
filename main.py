#!/usr/bin/python

import io         # used to create file streams
from io import open
import fcntl      # used to access I2C parameters like addresses

from datetime import datetime
from pytz import timezone

import time       # used for sleep delay and timestamps
import string     # helps parse strings
import serial
from smbus import SMBus

from dco2 import DCO2
from do import AtlasI2C
from brix import BRIX

from kafka import KafkaProducer
import simplejson as json


DEVICE_ID = 1
SERVER_ADR = 'localhost:9092'
TOPIC_NAME = 'hello-kafka'

device = AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary
device_dco2 = DCO2()
device_brix = BRIX()


def readAll():
    do_val = device.query("R")
    dco2_val = device_dco2.send_read_cmd() 
    brix_val =[10.0,10.0]
    #brix_val = device_brix.readData()
   
    #timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

    
    data = {'created_time' : timestamp , 'device_id' : DEVICE_ID, 'do' : do_val, 'dco2' : dco2_val, 'brix_temp' : brix_val[0], 'brix_brix': brix_val[1] }    
   
    sendAll(data)

    print("DO " + do_val + " ppm")
    print("DCO2 " + str(dco2_val) + " ppm")
    print("Brix-Temp "+ str(brix_val[0]))
    print("Brix-Brix " + str(brix_val[1]) + " %Brix") 
    print("")

def calAll():
    print("DO done" + device.query("Cal"))
    device_dco2.send_cal_cmd()
    #device_brix.readData()
    print("")

def publish_message(producer, data):
    
    try:
        producer.send(TOPIC_NAME, json.dumps(data).encode('utf-8'))
        producer.flush()

    except Exception as e:
        print('Exception in publishing message')
        print(e)

def connect_kafka_producer():
    _producer = None
    try :
        _producer = KafkaProducer(bootstrap_servers= [SERVER_ADR], api_version = (0,10))
    except Exception as e :
        print('Exception while connecting kafka')
        print(e)
    return _producer 


def sendAll(data):
    kafka_producer = connect_kafka_producer()

    publish_message(kafka_producer, data)
    if kafka_producer is not None:
        kafka_producer.close()

def main():
    	real_raw_input = vars(__builtins__).get('raw_input', input)
	
	# main loop
	while True:
		user_cmd = real_raw_input("Enter command: ")

		if user_cmd.upper().startswith("LIST_ADDR"):
			devices = device.list_i2c_devices()
			for i in range(len (devices)):
				print( devices[i])

		# address command lets you change which address the Raspberry Pi will poll
		elif user_cmd.upper().startswith("ADDRESS"):
			addr = int(user_cmd.split(',')[1])
			device.set_i2c_address(addr)
			print("I2C address set to " + str(addr))

		# continuous polling command automatically polls the board
		elif user_cmd.upper().startswith("POLL"):
			delaytime = float(string.split(user_cmd, ',')[1])

			# check for polling time being too short, change it to the minimum timeout if too short
			if delaytime < AtlasI2C.long_timeout:
				print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
				delaytime = AtlasI2C.long_timeout

			print("%0.2f seconds, press ctrl-c to stop polling" % delaytime)

			try:
				while True:
					readAll()
                                        time.sleep(delaytime - AtlasI2C.long_timeout)
			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")

		# if not a special keyword, pass commands straight to board
		else:
			if len(user_cmd) == 0:
				print( "Please input valid command.")
			
                        if user_cmd =="Quit" :
                            break
                        
                        elif user_cmd =="Read":
				try:
                                    readAll()
                                except IOError as e:
					print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")

                        elif user_cmd =="Cal":
                    		try:
                                    calAll()
                                except IOError as e:
					print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")



if __name__ == '__main__':
	main()

