import socket
import sys
import asyncio
import numpy as np
import json
import random
import string
from time import sleep
count=0
def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))
class vector:
	def __init__(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z		
		
class log:
	def __init__(self,userID):
		self.userid	=userID
		self.user_position=vector(float(("%0.3f"%random.random())), float(("%0.3f"%random.random())), float(("%0.3f"%random.random())))
		self.data=[1.0 for i in range(100)]
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)	
class packet:
	def __init__(self,userID):
		self.header="info"
		data=log(userID)
		self.content=str(data.toJSON())
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True)	
		
async def decode_data(msg,delimiter):
	data=msg.split(delimiter)
	data_list=[]
	for d in data:
		if d !='':
			data_list.append(d)
	return data_list

async def receive_check(loop,client,msg,delimiter):
	if msg[-1] != delimiter:
		total_msg=''
		total_msg+=msg
		while(True):
			_msg = await loop.sock_recv(client, 1)
			if _msg:
				_msg = _msg.decode()
				total_msg+=_msg
				if total_msg[-1] == delimiter:
					return total_msg
	else:
		return msg
		
		
async def send_handler(client,loop):
	try:
		UserID=random_char(5)
		for i in range(10):
			data=packet(UserID)
			result=str(data.toJSON())+"\n"
			result=result.encode()
			await loop.sock_sendall(client, result)
			await asyncio.sleep(0.1)
	except:
			sock.close()
			loop.close()
			
async def receive_handler(client,loop):
	global count
	print("receive_handler")
	while count<10:
		msg = await loop.sock_recv(client, 16384)
		msg = msg.decode()
		msg = await receive_check(loop,client,msg,'\n')
		data_list = await decode_data(msg,'\n')
		print("process1")
		for result in data_list:
			count+=1
			print("%d/result:%s"%(count,result))
			
async def echo_client(address,loop):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setblocking(False)
	await loop.sock_connect(sock, address)
	try:
		await loop.create_task(send_handler(sock,loop))
		await loop.create_task(receive_handler(sock,loop))
	except:
		sock.close()
		loop.close()
		
def run():
	loop = asyncio.get_event_loop()
	loop.create_task(echo_client(("127.0.0.1", 9000),loop))
	loop.run_forever()

