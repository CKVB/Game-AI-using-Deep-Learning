import os
import cv2,os
from grabscreen import grab_screen
from glob import glob
import numpy as np
import keyboard,time
from tqdm import tqdm
from random import shuffle

train_file='train.npy'

left_direction=[]
right_direction=[]
reverse_direction=[]
forward_direction=[]

images_in_each_set=100
width=128
height=128

def one_hot_encoding(key):
	data_set=[0,0,0,0]
	if key not in ['a','d','w','s']:
		return(None)
	else:
		if key=='a':
			data_set[0]=1
		elif key=='d':
			data_set[1]=1
		elif key=='w':
			data_set[2]=1
		elif key=='s':
			data_set[3]=1
		return(data_set)
		
frequency=1
stop=False
n=len(glob(r"D:\DL PYTHON\AI\TRAINING MODELS\NPY FILES\*.npy"))+1

while(True):
	#initial_image=grab_screen(region=(185,228,580,373))
	#initial_image=cv2.resize(initial_image,(width,height))
	#initial_image=cv2.cvtColor(initial_image,cv2.COLOR_BGR2GRAY)
	#cv2.imshow('VIEW',initial_image)
	#initial_image=initial_image[66:125,3:width]
	#initial_image=initial_image[66:125,0:300]
	#cv2.imshow("ROI",initial_image)
	#print(initial_image.shape)
	key_pressed=one_hot_encoding(keyboard.read_key())
	
	if key_pressed!=None:
		
		initial_image=grab_screen(region=(185,228,580,373))
		initial_image=cv2.resize(initial_image,(width,height))
		initial_image=cv2.cvtColor(initial_image,cv2.COLOR_BGR2GRAY)
		initial_image=initial_image[66:125,0:300]
		cv2.imshow("ROI",initial_image)
		
		if key_pressed==[1,0,0,0]:
			left_direction.append([initial_image,key_pressed])
		
		elif key_pressed==[0,1,0,0]:
			right_direction.append([initial_image,key_pressed])
		
		elif key_pressed==[0,0,1,0]:
			forward_direction.append([initial_image,key_pressed])
		
		elif key_pressed==[0,0,0,1]:
			reverse_direction.append([initial_image,key_pressed])
		
		print("LEFT : {} RIGHT : {} FORWARD : {} REVERSE : {}".format(len(left_direction),len(right_direction),len(forward_direction),len(reverse_direction)))
		
		
		
		if len(left_direction)>images_in_each_set and len(right_direction)>images_in_each_set and len(reverse_direction)>images_in_each_set and len(forward_direction)>images_in_each_set:
			print("Please wait saving data...........")
			
			shuffle(forward_direction)
			shuffle(left_direction)
			shuffle(right_direction)
			shuffle(reverse_direction)
			
			forward_direction_save=forward_direction[:images_in_each_set]
			left_direction_save=left_direction[:images_in_each_set]
			right_direction_save=right_direction[:images_in_each_set]
			reverse_direction_save=reverse_direction[:images_in_each_set]
			
			training_data=left_direction_save+right_direction_save+forward_direction_save+reverse_direction_save
			
			file_name="train_data_"+str(n)+".npy"
			
			np.save(file_name,training_data)
			
			n+=1
			
			left_direction=left_direction[images_in_each_set:]
			right_direction=right_direction[images_in_each_set:]
			reverse_direction=reverse_direction[images_in_each_set:]
			forward_direction=forward_direction[images_in_each_set:]
			
			print(len(left_direction),len(right_direction),len(forward_direction),len(reverse_direction))
			
			training_data=[]
			
			print('DATA saved.')
					
	if cv2.waitKey(1) & 0xff==ord('q'):
		cv2.destroyAllWindows()