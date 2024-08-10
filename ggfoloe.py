import cv2
import mediapipe as mp

def process_exercise_video(exercise_name, keypoints):
    # Load video file
    video_path = f'static/Recordings/{exercise_name}/{exercise_name}.mp4'
    cap = cv2.VideoCapture(video_path)

    # Initialize MediaPipe Pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    while cap.isOpened():
        # Read frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect poses
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw pose landmarks on the frame
            annotated_frame = frame.copy()
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                if idx in keypoints:
                    height, width, _ = frame.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    cv2.circle(annotated_frame, (cx, cy), 5, (255, 0, 0), -1)

            # Display annotated frame (or do further processing)
            cv2.imshow('Exercise Video', annotated_frame)

            # Calculate angles between keypoints (example calculation)
            angles = calculate_angles(results.pose_landmarks.landmark, keypoints)
            print('Angles:', angles)
            print('fwfef')

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
    cap.release()
    cv2.destroyAllWindows()

def calculate_angles(landmarks, keypoints):
    # Example function to calculate angles between keypoints
    angles = []
    for kp in keypoints:
        if kp < len(landmarks):
            # Assuming keypoints are provided as (p1, p2, p3) indices
            p1 = landmarks[kp - 1]
            p2 = landmarks[kp]
            p3 = landmarks[kp + 1]
            angle = calculate_angle(p1, p2, p3)
            angles.append(angle)
    return angles

def calculate_angle(p1, p2, p3):
    # Function to calculate angle between three points
    dx1 = p1.x - p2.x
    dy1 = p1.y - p2.y
    dx2 = p3.x - p2.x
    dy2 = p3.y - p2.y
    angle = abs((180 / 3.14159265359) * (dx1 * dy2 - dy1 * dx2) / (dx1 * dx2 + dy1 * dy2))
    return angle


exercise_name = "Arm Curl"
keypoints = [11,13,15]  # Example keypoints indices, adjust as per your requirement
process_exercise_video(exercise_name, keypoints)
