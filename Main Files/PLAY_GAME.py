from keras.models import load_model
from grabscreen import grab_screen
import numpy as np
import keyboard
import cv2,time
from tkinter import *

model_1=load_model('AI.h5')
model_2=load_model("AI2.h5")
left_right_model=load_model("LEFT_RIGHT.h5")
forward_reverse_model=load_model("FORWARD_REVERSE.h5")
condition=True

keys=['a','d','w','s']

font_style="-family {Yu Gothic UI Semibold} -size 30 -weight bold -slant italic"
button_font="-family {Segoe UI Historic} -size 24 -slant italic"

def execute():
	global condition
	condition=True

	def move_forward():
		temp.append('w')
		keyboard.press('w')
		keyboard.release('a')
		keyboard.release('s')
		keyboard.release('d')
		choice("Forward")
		time.sleep(0.3)
	
	def move_left():
		keyboard.press('s')
		time.sleep(0.4)
		keyboard.release('s')
		temp.append('a')
		keyboard.press('a')
		keyboard.release('w')
		keyboard.release('s')
		keyboard.release('d')
		choice("Left")
		time.sleep(0.4)
		
		
	def move_right():
		keyboard.press('s')
		time.sleep(0.4)
		keyboard.release('s')
		temp.append('d')
		keyboard.press('d')
		keyboard.release('a')
		keyboard.release('s')
		keyboard.release('w')
		choice("Right")
		time.sleep(0.4)
	
	
	def apply_break():
		temp.append('s')
		keyboard.press('s')
		keyboard.release('a')
		keyboard.release('w')
		keyboard.release('d')
		choice("Break")
		time.sleep(1)
	
	def choice(data):
		Label(myapp,text=data,background="#117aee",font=font_style,foreground="#f9fd48",relief="flat").place(relx=0.547, rely=0.134, height=61, width=254)
		myapp.update()

	while condition:
		
		temp=[]
		initial_image=grab_screen(region=(185,228,580,373))
		initial_image=cv2.resize(initial_image,(128,128))
		initial_image=cv2.cvtColor(initial_image,cv2.COLOR_BGR2GRAY)
		initial_image=initial_image[66:125,0:300]		
		initial_image=initial_image.reshape(1,128,59,1)
		
		prediction_1=model_1.predict(initial_image)[0]
		prediction_2=model_2.predict(initial_image)[0]
		left_right_prediction=left_right_model.predict(initial_image)[0]
		forward_reverse_prediction=forward_reverse_model.predict(initial_image)[0]	
			
		prediction_1=list(np.around(prediction_1))
		prediction_2=list(np.around(prediction_2))
		left_right_prediction=list(np.around(left_right_prediction))
		forward_reverse_prediction=list(np.around(forward_reverse_prediction))
		
		if (prediction_1[3]>0.01 or prediction_2[3]>0.01) or forward_reverse_prediction[1]==1:
			apply_break()
		elif prediction_2[2]==1 and prediction_1[2]==1 and forward_reverse_prediction[0]==1:
			move_forward()
		elif prediction_1[0]==1 and prediction_2[0]==1 and left_right_prediction[0]==1:
			move_left()
		elif prediction_1[1]==1 and prediction_2[1]==1 and left_right_prediction[1]==1:
			move_right()
		else:
			choice("Neutral")
			keyboard.release('w')
			keyboard.release('s')
			keyboard.release('a')
			keyboard.release('d')
			pass
			
		if temp[-5:].count('w')==5:
			apply_break()
			temp=[]
def stop():
	global condition
	condition=False
myapp=Tk()
myapp.title("Deep Learning")
myapp.resizable(0,0)
myapp.geometry("640x224+333+299")
myapp.configure(background="#117aee")
Label(myapp,text="Current Choice :",background="#117aee",font=font_style,foreground="#fff").place(relx=0.063, rely=0.134, height=51, width=304)
Button(myapp,text="Start",command=execute,background="#f1d638",font=button_font,cursor="hand2",relief="groove",foreground="#fa2405").place(relx=0.188, rely=0.625, height=44, width=147)
Button(myapp,text="Stop",command=stop,background="#f1d638",font=button_font,cursor="hand2",relief="groove",foreground="#fa2405").place(relx=0.563, rely=0.625, height=44, width=147)
myapp.mainloop()
