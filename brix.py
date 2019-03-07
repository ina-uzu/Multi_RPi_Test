import serial
import string
import time
import RPi.GPIO as GPIO
from struct import *
BAUD_RATE = 9600
READ_RATE = 1
DATA_LENGTH =13

#Can be changed
ADDR = 0x01
CRC_L = 0x44
CRC_H = 0x0C

READ_CMD = [chr(ADDR),chr(0x3), chr(0x00) ,chr(0x00),chr(0x00),chr(0x08), chr(CRC_L), chr(CRC_H)]
READ_CMD_STR = ''.join(READ_CMD)

class BRIX :
	#CODE
	ser = serial.Serial("/dev/serial0", BAUD_RATE, timeout=1)

	def calCRC(self, crc, a):
		crc = crc^a
		for i in range(8):
			if crc & 1:
				crc = (crc>>1)^0xA001
			else :
				crc = (crc>>1)
		return crc

	def readData(self):
		#self.ser.write(READ_CMD_STR)
		res = []
		data=[]
	 	time.sleep(1) 
	 
		for i in range(DATA_LENGTH):
			tmp = self.ser.read(1)
		 	try :
				data.append(ord(tmp))
			except :
				data.append(0)
		
		#CRC check
		crc=0xFFFF;
		for i in range(11):
			crc = self.calCRC(crc,data[i])
		
		if crc%0x100 != data[11] or crc/0x100 != data[12]:
			return [-1,-1]

		brix = chr(data[3]) +  chr(data[4])+   chr(data[5])+ chr(data[6]) 
		temp = chr(data[7]) +  chr(data[8])+   chr(data[9])+ chr(data[10]) 
		print( unpack('f', brix))
		print( unpack('f', temp))
		brix= '%.2f' % (unpack('f', brix))
		temp ='%.2f' % (unpack('f', temp))
		res.append(temp)
		res.append(brix)
	 	return res
'''
		temp = data[3]
		for i in range(3):
			temp = temp << 4
			temp += data[i+4]

		res.append(float(temp))

		temp = data[7]
		for i in range(3):
			temp = temp << 4
			temp+= data[i+8]
		res.append(float(temp))
'''
