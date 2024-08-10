# After clicking on the button with the required exercise, we have to show
# the trainers video on the left side of the screen and the users video on the 
# right side of the screen. When the user presses start, the trainers video starts playing
# on a loop and the users video starts getting recorded. 
# 
import cv2
import mediapipe as mp
import time
import datetime
import os
def followExercise():
    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None

    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
        
            results = pose.process(image)
    
        
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                
            except:
                pass