import mediapipe as mp

class PoseLandmarks:
    def __init__(self, landmarks):
        self.landmark_dict = {
            "LEFT_SHOULDER": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y],
            "LEFT_ELBOW": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].y],
            "LEFT_WRIST": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST].y],

            "RIGHT_SHOULDER": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y],
            "RIGHT_ELBOW": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].y],
            "RIGHT_WRIST": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].y],

            "NOSE": [landmarks[mp.solutions.pose.PoseLandmark.NOSE].x, landmarks[mp.solutions.pose.PoseLandmark.NOSE].y],
            "RIGHT_HIP": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP].y],
            "LEFT_HIP": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP].y],

            "RIGHT_EYE_INNER": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EYE_INNER].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EYE_INNER].y],
            "LEFT_EYE_INNER": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE_INNER].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE_INNER].y],
            "LEFT_EYE_OUTER": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE_OUTER].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE_OUTER].y],

            "RIGHT_KNEE": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE].y],
            "LEFT_KNEE": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE].y],
            "LEFT_ANKLE": [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE].y],
            "RIGHT_ANKLE": [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE].y]
        }

    def get_landmark(self, landmark_name):
        return self.landmark_dict.get(landmark_name.upper(), None)
