import multiprocessing
import socket_client as client




if __name__ == '__main__':
	for i in range(10):
		p = multiprocessing.Process(target=client.run)
		p.start()
	print("done!")