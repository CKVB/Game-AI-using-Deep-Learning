from keras.layers import Dense,Activation,Dropout,Flatten,Conv2D,MaxPooling2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from random import shuffle
import numpy as np
from glob import glob

Image_width=128
Image_height=59
threshold=50
Epochs=40

input_shape=(Image_width,Image_height,1)

model=Sequential()

model.add(Conv2D(32,(3,3),input_shape=input_shape))
model.add(Activation('relu'))

model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

model.add(Conv2D(64,(3,3)))
model.add(Activation('relu'))

model.add(Conv2D(64,(3,3)))
model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

model.add(Dense(128))

model.add(Activation('relu'))

model.add(Dropout(0.4))

model.add(Flatten())

model.add(Dense(4))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=1e-4,beta_1=0.9,beta_2=0.999,epsilon=1e-8),metrics=['accuracy'])

call_back=TensorBoard(log_dir="D:\DL PYTHON\AI\TRAINING MODELS\LOGS")

data=np.load("Training_data.npy",allow_pickle=True)
	
left=[];right=[];forward=[];reverse=[]
	
for each_sample in data:
	if each_sample[1]==[1,0,0,0]:
		left.append(each_sample)
	elif each_sample[1]==[0,1,0,0]:
		right.append(each_sample)
	elif each_sample[1]==[0,0,1,0]:
		forward.append(each_sample)
	elif each_sample[1]==[0,0,0,1]:
		reverse.append(each_sample)

training_data=left[:-threshold]+right[:-threshold]+forward[:-threshold]+reverse[:-threshold]
testing_data=left[-threshold:]+right[-threshold:]+forward[-threshold:]+reverse[-threshold:]

print("Total data-points considered for training : {}".format(len(training_data)))
print("Total data-points considered for testing  : {}".format(len(testing_data)))

input("Press any key to start training")
	
x_train=np.array([data[0] for data in training_data]).reshape(len(training_data),Image_width,Image_height,1)
x_train=x_train/255
y_train=np.array([data[1] for data in training_data])

x_test=np.array([data[0] for data in testing_data]).reshape(len(testing_data),Image_width,Image_height,1)
x_test=x_test/255
y_test=np.array([data[1] for data in testing_data])

h=model.fit(x_train,y_train,epochs=Epochs,validation_data=(x_test,y_test),callbacks=[call_back])

model.save('model.h5')