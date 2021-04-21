from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Global Variables
#--------------------------------------------------------
#Minimum Eye Aspect Ratio Threshold to determine eyes closing
ear_threshold = 0.3

#Minimum consecutive frames for which eye ratio is below threshold for alarm to be triggered
ear_frames = 15

#keeps track of number of consecutive frames 
counter = 0

#GPIO pins for led and buzzer 
ledpin = 17
GPIO.setup(ledpin,GPIO.OUT)

buzzer_pin = 27
GPIO.setup(buzzer_pin,GPIO.OUT)

#Loads opencv xml file to draw rectangle around face
face_cascade = cv2.CascadeClassifier("xml_files/haarcascade_frontalface_default.xml")

#function that calculates eye aspect ratio
def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])

	ear = (A+B) / (2*C)
	return ear

def alertON():
	GPIO.output(buzzer_pin,1)
	GPIO.output(ledpin,1)
	time.sleep(0.5)
	GPIO.output(ledpin,0)

def alertOFF():
	GPIO.output(buzzer_pin,0)
	GPIO.output(ledpin,0)



detector = dlib.get_frontal_face_detector()
#loads file to predict 68 points of the face
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(left_start, left_end) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(right_start, right_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#Defines video capture object
vid = cv2.VideoCapture(0)

#sleeps for camera to start
time.sleep(2)

while(True):
	#Read each frame and flip it, and convert to grayscale
	ret, frame = vid.read()
	frame = cv2.flip(frame,1)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#Detect facial points through detector function
	faces = detector(gray, 0)

	#Detect faces through haarcascade_frontalface_default.xml
	face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)

	#Draw rectangle around each face detected
	for (x,y,w,h) in face_rectangle:
	  cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #Detect facial points
	for face in faces:
		shape = predictor(gray, face)
		shape = face_utils.shape_to_np(shape)

		#Retrieves coordinates for the left eye and the right eye
		leftEye = shape[left_start:left_end]
		rightEye = shape[right_start:right_end]

		#Calculate aspect ratio of both eyes
		leftEyeAspectRatio = eye_aspect_ratio(leftEye)
		rightEyeAspectRatio = eye_aspect_ratio(rightEye)

		eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2

		#Use hull to remove convex contour discrepencies and draw eye shape around eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		#checks if eye aspect ratio is less than threshold 
		if(eyeAspectRatio < ear_threshold):
			counter += 1
			#if eye aspect ratio less than threshold, then chekcs if number of frames greater than threshold and alerts driver
			if counter >= ear_frames:
				cv2.putText(frame, "Drowsiness Detected!", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
				alertON()
		else:
			counter = 0
			alertOFF()
	

	#Displays video frame 
	cv2.imshow('FRAME', frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break


vid.release()
cv2.destroyAllWindows()
