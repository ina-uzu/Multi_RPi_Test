#!/usr/bin/python

import io         # used to create file streams
from io import open
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings
import serial
from smbus import SMBus

from dco2 import DCO2
from do import AtlasI2C
from brix import BRIX

device = AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary
device_dco2 = DCO2()
device_brix = BRIX()


def readAll():
    print("DO " + device.query("R") + " ppm")
    device_dco2.send_read_cmd()
    device_brix.readData()
    print("")

def calAll():
    print("DO done" + device.query("Cal"))
    device_dco2.send_cal_cmd()
    #device_brix.readData()
    print("")


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

