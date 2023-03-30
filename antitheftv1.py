# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 18:56:42 2023

@author: antog
"""

from flask import Flask, render_template, request
import os
import cv2
import mediapipe as mp
import os
import time
from PIL import Image
import face_recognition
from numpy import asarray
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Function to recognize faces
def recognition(im1, known_face_encodings):
    A = False
    rgb = asarray(im1)
    rgb_small_frame = rgb[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_small_frame)
    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if face_distances[0] < .50:
            print('It is Anto',face_distances)
        else:
            print('Its not Anto')
            A = True
    return A

# Function to save detected faces into folder
def saving_faces(array, im, frame_no, count, main_folder, known_face_encodings):
    num=1
    if count > 0:
        for value in array:
            im1= im.crop((value[0], value[1], value[2], value[3]))
            B = recognition(im1, known_face_encodings)
            if B:
                im1.save(main_folder + '\\faces_detected\\' + str(frame_no) + '_' + str(num) + 'image.jpg')
            num += 1
# Function to count number of faces
def detector(face_detection, frame, frame_no, main_folder, known_face_encodings):
    count = 0
    array=[]
    frame_no = frame_no + 1
    height, width, channel = frame.shape
    im = Image.fromarray(frame)
    color_count = im.getcolors()
    if color_count:
        print('')
    else:
        # Detect faces in the frame
        result = face_detection.process(frame)

        # When face is detected
        try:
            for count, detection in enumerate(result.detections):
                score = detection.score
                score = int(round(score[0]*100, 2))
                box = detection.location_data.relative_bounding_box
                x, y, w, h = int(box.xmin*width), int(box.ymin * height), int(box.width*width),int(box.height*height)
                x_min, y_min, x_max, y_max = int(box.xmin*width), int(box.ymin * height), int(box.width*width+box.xmin*width),int(box.height*height+box.ymin * height)
                array.append([x_min, y_min, x_max, y_max])
            count += 1
            saving_faces(array, im, frame_no, count, main_folder, known_face_encodings)
        # When no face is detected
        except:
            print('no face detected')
    return frame_no

app = Flask(__name__)

# Path to the folder containing the photos
PHOTO_FOLDER = 'path/to/photo/folder'

@app.route('/')
def index():
    # Get a list of all the photo files in the folder
    photo_files = [f for f in os.listdir(PHOTO_FOLDER) if os.path.isfile(os.path.join(PHOTO_FOLDER, f))]

    # Render the HTML template with the list of photo files
    return render_template('index.html', photo_files=photo_files)

if __name__ == '__main__':
   
	#html_file = index.serve()
	JOSE_image = face_recognition.load_image_file(r"C:\Users\antog\Documents\ECE 554 Embedded System\Project\antitheftece554-main\antitheftece554-main\server\antitheftserver\static\Anto.jpg")
	JOSE_face_encoding = face_recognition.face_encodings(JOSE_image)[0]
	known_face_encodings = [
	    JOSE_face_encoding
	]
	known_face_names = [
	    "JOSE"
	]
	process_this_frame = True
	video_capture = cv2.VideoCapture(0)
	face_detection = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
	main_folder = r"C:\Users\antog\documents\ECE 554 Embedded System\project"
	os.mkdir(main_folder +'\\faces_detected')
	frame_no = 0;
	while True:
		# Grab a single frame of video
		ret, frame = video_capture.read()
		if process_this_frame:
			frame_no = detector(face_detection, frame,frame_no,main_folder,known_face_encodings)
			# Hit 'q' on the keyboard to quit!
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			frame_no = detector(face_detection, frame,frame_no,main_folder,JOSE_face_encoding)
			cv2.imshow('Video', frame)
app.run()
video_capture.release()
cv2.destroyAllWindows()