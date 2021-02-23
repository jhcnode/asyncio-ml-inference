import tensorflow as tf
import numpy as np
from model import model

class inference(object):

	def __init__(self,num_label,num_dim,weights_file):
		self.weights_file=weights_file
		self.net= model(num_label,num_dim)
		y=tf.nn.softmax(self.net.logits, name="prob_y")
		self.argmax=tf.argmax(y, 1,name="argmax")
		config = tf.ConfigProto()
		config.gpu_options.allow_growth = True
		config.gpu_options.per_process_gpu_memory_fraction = 1.0
		self.sess = tf.Session(config=config)
		self.saver = tf.train.Saver()
		self.saver.restore(self.sess, self.weights_file)
		
		x=[]
		for i in range(100):
			x.append(1.0)
		result=self.infer(x)
		print("initialize_a_tensorflow")
		


	def infer_batch(self,data):
		x=np.array(data)
		
		batch_size=x.shape[0]
		num_dim=x.shape[1]
		x=x.reshape(batch_size,num_dim)
		result=self.sess.run(self.argmax,feed_dict={self.net.x: x})
		
		return result
		
	def infer(self,data):
		x=np.array(data)
		num_dim=x.shape[0]
		x=x.reshape(1,num_dim)
		result=self.sess.run(self.argmax,feed_dict={self.net.x: x})
		result=int(result)
		return result

# num_label=21
# num_dim=100
# weights_file='./weight/w'
# predictor=inference(num_label,num_dim,weights_file)
# x=[]
# for i in range(100):
	# x.append(1.0)
# predictor.infer(x)
		


		