import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()
import numpy as np
from tensorflow.python.framework import ops


class model(object):

	def __init__(self,num_class,input_dim):
		self.num_class = num_class
		self.input_dim = input_dim
		self.x = tf.placeholder(tf.float32, shape=[None, input_dim], name = 'x') 
		self.y_target = tf.placeholder(tf.float32, shape=[None, num_class], name = 'y_target')
		self.logits = self.build_network(x=self.x,input_dim=self.input_dim,num_class=self.num_class)

	
	def build_network(self,x,input_dim,num_class):
	
		# reshape input data
		x_data = tf.reshape(x, [-1,input_dim], name="x_data")

		# Build a fully connected layer
		W_fc1 = tf.Variable(tf.truncated_normal([input_dim, 32],stddev=np.sqrt(1/input_dim)), name = 'W_fc1')
		b_fc1 = tf.Variable(tf.random_normal([32],stddev=0), name = 'b_fc1')
		h_fc1 = tf.nn.relu(tf.matmul(x_data, W_fc1) + b_fc1, name="h_fc1")

		shape = h_fc1.get_shape().as_list()
		flat_num= shape[1]


		# Build a fully connected layer
		W_fc2 = tf.Variable(tf.random_normal([flat_num, num_class], stddev=np.sqrt(1/flat_num)), name = 'W_fc2')
		b_fc2 = tf.Variable(tf.random_normal([num_class],stddev=0), name = 'b_fc2')

		# Build a output layer
		return tf.matmul(h_fc1, W_fc2) + b_fc2
		
		
