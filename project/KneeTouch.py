import logging
import cv2
import mediapipe as mp
import numpy as np
import math

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Program started')

# MediaPipe Drawing and Pose modules
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_pose(frame, landmarks, color):
    # Draw body joint points and connections
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=color, thickness=2))

def calculate_angle(p1, p2, p3):
    # Calculate the angle
    a = np.array([p1.x, p1.y]) - np.array([p2.x, p2.y])
    b = np.array([p3.x, p3.y]) - np.array([p2.x, p2.y])
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    angle = math.acos(dot_product / (magnitude_a * magnitude_b))
    return math.degrees(angle)

def check_kneetouch(landmarks):
    # Get knee and elbow landmarks
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    # Calculate the distance between knee and opposite elbow and knee height
    left_distance = np.sqrt((left_knee.x - right_elbow.x)**2 + (left_knee.y - right_elbow.y)**2)
    right_distance = np.sqrt((right_knee.x - left_elbow.x)**2 + (right_knee.y - left_elbow.y)**2)

    left_knee_height = left_knee.y
    right_knee_height = right_knee.y

    left_hip_height = left_hip.y
    right_hip_height = right_hip.y

    # Check if the knees are raised high enough and if the angles are appropriate
    left_angle = calculate_angle(left_hip, left_knee, right_elbow)
    right_angle = calculate_angle(right_hip, right_knee, left_elbow)

    left_knee_up = left_knee_height < left_hip_height
    right_knee_up = right_knee_height < right_hip_height

    return left_distance, right_distance, left_angle, right_angle, left_knee_up, right_knee_up

def process_frame(frame, pose, kneetouch_count, was_below_threshold):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    frame_height, frame_width, _ = frame.shape

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_distance, right_distance, left_angle, right_angle, left_knee_up, right_knee_up = check_kneetouch(landmarks)
        
        # Check the distance between knee and elbow, knee lift angle, and height
        if ((left_distance < 0.1 and left_angle > 90 and left_knee_up) or (right_distance < 0.1 and right_angle > 90 and right_knee_up)) and not was_below_threshold:
            was_below_threshold = True
        elif (left_distance > 0.15 and right_distance > 0.15) and was_below_threshold:
            kneetouch_count += 1
            was_below_threshold = False

        color = (0, 255, 0) if was_below_threshold else (255, 0, 0)
        draw_pose(frame, results.pose_landmarks, color)

    return frame, kneetouch_count, was_below_threshold

def show_camera():
    cap = cv2.VideoCapture(0)
    kneetouch_count = 0
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

            frame, kneetouch_count, was_below_threshold = process_frame(frame, pose, kneetouch_count, was_below_threshold)

            cv2.imshow('Pose Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    show_camera()
    logging.debug('Program finished')
