import cv2
import numpy as np
import pickle
import os
import sqlite3
import random

image_x, image_y = 250, 250


def get_hand_hist():
	with open("hist1", "rb") as f:
		hist = pickle.load(f)
	return hist

def init_create_folder_database():
	# create the folder and database if not exist
	if not os.path.exists("gestures1"):
		os.mkdir("gestures1")
	if not os.path.exists("gesture1_db.db"):
		conn = sqlite3.connect("gesture1_db.db")
		create_table_cmd = "CREATE TABLE gesture ( g_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, g_name TEXT NOT NULL )"
		conn.execute(create_table_cmd)
		conn.commit()


def create_folder(folder_name):
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)


def store_in_db(g_id, g_name):
	conn = sqlite3.connect("gesture1_db.db")
	cmd = "INSERT INTO gesture (g_id, g_name) VALUES (%s, \'%s\')" % (
	    g_id, g_name)
	try:
		conn.execute(cmd)
	except sqlite3.IntegrityError:
		choice = input("g_id already exists. Want to change the record? (y/n): ")
		if choice.lower() == 'y':
			cmd = "UPDATE gesture SET g_name = \'%s\' WHERE g_id = %s" % (g_name, g_id)
			conn.execute(cmd)
		else:
			print("Doing nothing...")
			return
	conn.commit()


def store_images(g_id):
    capture = cv2.VideoCapture(0)
    pic_no = 0
    create_folder("gestures1/"+str(g_id))
    while(pic_no < 120):
        ret, frame = capture.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pic_no+=1
        cv2.putText(frame, "Capturing...", (30, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (127, 255, 255))
        cv2.imwrite("gestures1/"+str(g_id)+"/"+str(pic_no)+".jpg", grayFrame)
    capture.release()
    cv2.destroyAllWindows()

def flip_images():
	gest_folder = "gestures1"
	images_labels = []
	images = []
	labels = []
	for g_id in os.listdir(gest_folder):
		for i in range(120):
			path = gest_folder+"/"+g_id+"/"+str(i+1)+".jpg"
			new_path = gest_folder+"/"+g_id+"/"+str(i+1)+".jpg"
			print(path)
			img = cv2.imread(path, 0)
			img = cv2.flip(img, 1)
			try:
				img = cv2.resize(img,(256,256))
				cv2.imwrite(new_path, img)
			except Exception as e:
				# print(str(e))
				pass

init_create_folder_database()
g_id = input("Enter gesture no.: ")
g_name = input("Enter gesture name/text: ")
store_in_db(g_id, g_name)
store_images(g_id)
flip_images()