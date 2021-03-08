# simple-asyncio-ml-inference
ML Inference based Asyncio 

## Features 
1. classification model(input = 100 dimension featrue vector, output = label(3 category)) 
2. send and receive data using asyncio
3. Simple ML Inference 
4. 1:N communication 

## Environments
Tensorflow-gpu(<=2.0)

## Train 
1. [Train](https://github.com/jhcnode/asyncio-ml-inference/blob/main/train/MLP%2BSelu%2B5%20Hidden%20Layer.ipynb)

## Serving model 
1. Copy weight files and paste to Directory [./weight/](https://github.com/jhcnode/asyncio-ml-inference/tree/main/weight)
2. > python socket_server.py  
