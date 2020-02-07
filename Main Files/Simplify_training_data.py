import numpy as np
from glob import glob 

training_data_files=glob("*.npy")

left=[];right=[];forward=[];reverse=[]

for each_file in training_data_files:
	data=np.load(each_file,allow_pickle=True)
	for each_sample in data:
		if each_sample[1]==[1,0,0,0]:
			left.append(each_sample)
		elif each_sample[1]==[0,1,0,0]:
			right.append(each_sample)
		elif each_sample[1]==[0,0,1,0]:
			forward.append(each_sample)
		elif each_sample[1]==[0,0,0,1]:
			reverse.append(each_sample)
			
training_data=left+right+forward+reverse
file=open("Each_instance_size.txt","w+")
file.write("LEFT : "+str(len(left))+" RIGHT : "+str(len(right))+" FORWARD : "+str(len(forward))+" REVERSE : "+str(len(reverse)))
np.save("Training_data.npy",training_data)
