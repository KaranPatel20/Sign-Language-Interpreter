import cv2
import numpy as np
import pickle
import os
import sqlite3
import random

def store_images():
    capture = cv2.VideoCapture(0)
    #create_folder("gestures1/"+str(g_id))
    i=0
    print("Press c to capture image and press q to quit")
    while True:
        ret, frame = capture.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'): 
            cv2.putText(frame, "Capturing...", (30, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (127, 255, 255))
            cv2.imwrite(str(i)+".jpg", grayFrame)
            i+=1
        if(cv2.waitKey(1)) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()

store_images()