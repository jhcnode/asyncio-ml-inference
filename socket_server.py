import asyncio
import requests
import os
from socket import *
from inference import inference
from timer import Timer
import numpy as np
import json
from datetime import datetime

def infer(predictor,x):
	result=predictor.infer(x)
	return result
class Server:
	def __init__(self,predictor):
		self.loop = asyncio.get_event_loop()
		self.clients = {}
		self.predictor=predictor
		self.delimiter='\n'
	def __del__(self):
		for addr in self.clients:
			self.connection_lost(self.clients[addr],addr)

	def run(self,IP,Port):
		self.loop.create_task(self.echo_server((IP, Port)))
		print("serving on\n")
		self.loop.run_forever()
	def connection_lost(self,client,addr):
		del self.clients[addr]
		client.close()
		print('disconnection from {}'.format(str(addr)))		
	async def receive_check(self,msg,client):
		if msg[-1] != self.delimiter:
			total_msg=''
			total_msg+=msg
			while(True):
				_msg = await self.loop.sock_recv(client, 1)
				if _msg:
					_msg = _msg.decode()
					total_msg+=_msg
					if total_msg[-1] == self.delimiter:
						return total_msg
		else:
			return msg		
	async def decode_data(self,msg):
		data=msg.split(self.delimiter)
		data_list=[]
		for raw_d in data:
			if raw_d !='':
				d = json.loads(raw_d)
				if d['header']=="data":
					x=[]
					x_str_list=d['content'].split(' ')
					for x_str in x_str_list:
						if x_str!='':
							x.append(float(x_str))		
					d['content']=x		
				
				data_list.append(d)
		return data_list		
	async def echo_server(self, address):
		sock = socket(AF_INET, SOCK_STREAM)
		sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		sock.bind(address)
		sock.listen(10)
		sock.setblocking(False)
		while True:
			client, addr = await self.loop.sock_accept(sock)
			self.clients[addr]=client
			print('Connection from {}'.format(str(addr)))
			self.loop.create_task(self.echo_handler(client,addr))
	async def echo_handler(self, client,addr):
		with client:
			while True:
				try:
					msg = await self.loop.sock_recv(client, 1)
					msg = msg.decode()
					if not msg:
						break					
					else:
						msg = await self.receive_check(msg,client)
						data_list= await self.decode_data(msg)
						text_log={}
						for data in data_list:
							if data['header']=="info":
								x=json.loads(data['content'])
								result = await self.loop.run_in_executor(None,infer,self.predictor,x)
								result = (str(result)+self.delimiter).encode()
								await self.loop.sock_sendall(client, result)
								
								text_log['info']=str(data['content'])	
								log=str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))+","+str(text_log['info'])+"\n"
								print("(info):"+log)
								f = open("./log.txt", 'a+')
								f.write(log)
								f.close()

							
				except:
					break
			self.connection_lost(client,addr) 
			print('Connection closed.')
			
			
num_label=3
num_dim=100
IP="0.0.0.0"
Port=9000
weights_file='./weight/w'
predictor=inference(num_label,num_dim,weights_file)
server = Server(predictor)
server.run(IP,Port)