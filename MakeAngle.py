import cv2
import os
import glob
import mediapipe as mp
import numpy as np
from AngleDef import angles_org
import CalculateAngle
import ConnectDatabase
from PoseLandmarkClass import PoseLandmarks
import tensorflow as tf
import logging
tf.get_logger().setLevel('ERROR')

def process_video(exercise_name, conn_cursor):
    conn_cursor[1].execute("SELECT videopath FROM algoinput WHERE exercisename = %s", (exercise_name,))
    result = conn_cursor[1].fetchone()

    if not result:
        raise ValueError(f"No video path found for exercise: {exercise_name}")
    
    video_folder = result[0]
    
    if not os.path.exists(video_folder):
        raise ValueError(f"Video folder does not exist: {video_folder}")

    video_files = glob.glob(os.path.join(video_folder, '*.mp4'))
    if not video_files:
        raise ValueError(f"No video files found in folder: {video_folder}")

    video_names = [os.path.basename(video) for video in video_files]
    ch = int(input("Enter the index"))
    
    if ch < 0 or ch >= len(video_names):
        raise ValueError("Invalid video choice index")
    
    video_path = os.path.join(video_folder, video_names[ch])
    logging.info(f"Processing video: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        resultant_points = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                pose_landmarks = PoseLandmarks(landmarks)

                conn_cursor[1].execute('SELECT * FROM algoinput WHERE exercisename = %s', (exercise_name,))
                row = conn_cursor[1].fetchone()
                conn_cursor[0].commit()

                angle_no = [i for i, value in enumerate(row) if value == 1]
                angle_structure = [angles_org[j][1] for j in angle_no]

                imp_points = []
                for angle_def in angle_structure:
                    f = pose_landmarks.get_landmark(angle_def[0])
                    m = pose_landmarks.get_landmark(angle_def[1])
                    l = pose_landmarks.get_landmark(angle_def[2])
                    angle = CalculateAngle.calculate_angle(f, m, l)
                    imp_points.append(angle)

                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(m, [640, 480]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                resultant_points.append(imp_points)

            except Exception as e:
                logging.error(f"Error processing frame: {e}")
                pass

            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                            mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))              

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    return resultant_points
