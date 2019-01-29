from smbus import SMBus
START = 0x23
END = 0x21
READ = 0x0
CAL = 0x2
BUSY = 0x0
FREE = 0x01
READ_BYTE_NUM = 7

class DCO2:
    address = 0x31
    bus = SMBus(1)

    def send_cal_cmd(self):
	#send start signal & check response
	while self.bus.write_byte(self.address,START) == BUSY :
		pass

	#send READ cmd 
	self.bus.write_byte(self.address, CAL )
	
	#send stop signal 
	self.bus.write_byte(self.address, END)


	#send start signal & check response
	while self.bus.write_byte(self.address, START) == BUSY :
		pass

	#receive data (7-byte) from sensor
	data = self.bus.read_byte(self.address)
        if data ==1:
            print("DCO2 done")

        else :
            print("DCO2 failed")

    
    def send_read_cmd(self) :
	'''
        #send start signal & check response
	while self.bus.write_byte(self.address, START) == BUSY :
		pass

	#send READ cmd 
	bus.write_byte(self.address , READ)
		
	#send stop signal 
	self.bus.write_byte(self.address, READ)

	#send start signal & check response
	while self.bus.write_byte(self.address, START) == BUSY :
		pass
        '''

	#receive data (7-byte) from sensor
	data = self.bus.read_i2c_block_data(self.address,READ, READ_BYTE_NUM)
					
	res = data[1] << 8
	res += data[2] 
    
        return res
	
