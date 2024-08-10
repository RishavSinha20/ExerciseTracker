import cv2
import mediapipe as mp
from AngleDef import calculate_angle
cap = cv2.VideoCapture("Recording Video\\Recordings\\Arm Curl_20240606_144747.mp4")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
leftarm=list()
rightarm=list()

angleslist=list()
angnum=4
for i in range(angnum):
    angleslist.append(list())

angleslist[0].append()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        try:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            leval=calculate_angle(left_shoulder,left_elbow,left_wrist)
            leftarm.append(leval)
        except:
            pass
    # Process frame with MediaPipe Holistic
    # results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
curdir=0
base=leftarm[0]
imppoints=list()
imppoints.append(base)
for i in range(1,len(leftarm)):
    diff=leftarm[i]-base
    if(diff>0):
        if curdir==0:
            curdir=1
        elif curdir==-1:
            curdir=1
            base=leftarm[i]
            imppoints.append(base)
    elif(diff<0):
        if curdir==0:
            curdir=-1
        elif curdir==1:
            curdir=-1
            base=leftarm[i]
            imppoints.append(base)
    else:
        curdir=0
print(len(imppoints))
print(len(leftarm))
