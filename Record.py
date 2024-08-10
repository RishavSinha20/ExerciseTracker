import cv2
import mediapipe as mp
import numpy as np
import os
from CalculateAngle import calculate_angle

def record(exercise_name, points_sets):
    output_directory = f"static/Recordings/{exercise_name}"
    os.makedirs(output_directory, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_path = os.path.join(output_directory, f"{exercise_name}_trainer.mp4")
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'H264'), 18, (width, height))
        
        angles = {i: [] for i in range(len(points_sets))}  # Dictionary to store angles for each set
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                for idx, points in enumerate(points_sets):
                    try:
                        p1 = [landmarks[points[0]].x, landmarks[points[0]].y]
                        p2 = [landmarks[points[1]].x, landmarks[points[1]].y]
                        p3 = [landmarks[points[2]].x, landmarks[points[2]].y]
                        
                        angle = calculate_angle(p1, p2, p3)
                        angles[idx].append(angle)
                        
                        cv2.putText(image, f"Angle {idx+1}: {angle}", 
                                    tuple(np.multiply(p2, [width, height]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    except IndexError:
                        print(f"Index error with points: {points}")
                           
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, 
                                                      mp.solutions.pose.POSE_CONNECTIONS,
                                                      mp.solutions.drawing_utils.DrawingSpec(color=(245,117,66),
                                                      thickness=2, circle_radius=2), 
                                                      mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230),
                                                      thickness=2, circle_radius=2))
            
            cv2.imshow('Mediapipe Feed', image)
            out.write(image)
    
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        return angles
