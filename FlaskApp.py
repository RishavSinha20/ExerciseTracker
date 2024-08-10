import sys
from flask import Flask,jsonify,send_file
from flask_cors import CORS
import cv2
import mediapipe as mp
import time
import datetime
import os

sys.path.append("\Parkinson\Recording Video")


app = Flask(__name__)
CORS(app)



@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)



@app.route('/run_script',methods = ['GET'])
def run_script():
    result = record()
    return jsonify({'result' : result})
def record():
    # Initialize MediaPipe Holistic
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    frame_width = 640
    frame_height = 480
    fps = 20

    # Define the output directory
    output_dir = 'Recording Video\Recordings'    # Replace with your desired directory path
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename using a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'Arm Curl_{timestamp}.mp4')

    # Start video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Wait for 3 seconds for the user to prepare
    print("Get ready! Recording will start in 3 seconds...")
    time.sleep(3)

    print("Recording started. Press 'e' to stop recording.")

    # Create VideoWriter object
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Process frame with MediaPipe Holistic
        results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Draw landmarks (optional)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
        if results.face_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.face_landmarks,
                mp_holistic.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1))
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

        out.write(frame)

        # Display the frame
        cv2.imshow('Recording', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            print("Recording stopped by user.")
            break

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Video saved as {output_file}")




if __name__ == "__main__":
    app.run(debug = True)

