import logging
import cv2
import mediapipe as mp
import numpy as np
import math

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Program started')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_pose(frame, landmarks, color):
    """Draws joint points and connections for the arms"""
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=color, thickness=2))

def calculate_angle(p1, p2, p3):
    """Calculates the angle between three given points"""
    a = np.array([p1.x, p1.y]) - np.array([p2.x, p2.y])
    b = np.array([p3.x, p3.y]) - np.array([p2.x, p2.y])
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    angle = math.acos(dot_product / (magnitude_a * magnitude_b))
    return math.degrees(angle)

def check_curl(landmarks):
    """Checks the curl movement for both arms and returns the angles"""
    # Get arm landmarks
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    return left_angle, right_angle

def process_frame(frame, pose, curl_count, was_below_threshold):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_angle, right_angle = check_curl(landmarks)
        if (left_angle < 100 or right_angle < 100) and not was_below_threshold:
            was_below_threshold = True
        elif left_angle > 160 and right_angle > 160 and was_below_threshold:
            curl_count += 1
            was_below_threshold = False

        color = (0, 255, 0) if was_below_threshold else (255, 0, 0)
        draw_pose(frame, results.pose_landmarks, color)

    return frame, curl_count, was_below_threshold

def show_camera():
    cap = cv2.VideoCapture(0)
    curl_count = 0
    was_below_threshold = False

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        if not cap.isOpened():
            logging.error("Cannot open camera.")
            return

        cv2.namedWindow("Pose Detection", cv2.WINDOW_NORMAL)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logging.error("Cannot receive frame.")
                break

            frame, curl_count, was_below_threshold = process_frame(frame, pose, curl_count, was_below_threshold)

            cv2.imshow('Pose Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    show_camera()
    logging.debug('Program finished')
