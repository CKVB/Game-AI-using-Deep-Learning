import cv2,time
import numpy as np
from argparse import ArgumentParser
ap=ArgumentParser()
ap.add_argument('-f','--file',required=True,help="Provide file name")
args=vars(ap.parse_args())
training_file=np.load(args['file'],allow_pickle=True)
for n,data in enumerate(training_file):
	image=data[0]
	choice=data[1]
	cv2.imshow("TEST",image)
	print(choice,n+1)
	time.sleep(2)
	if cv2.waitKey(25) & 0XFF==ord('q'):
		cv2.destroyAllWindows()
		break