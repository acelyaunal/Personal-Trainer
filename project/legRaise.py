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

def check_leg_raise(landmarks):
    # Get hip, knee, and ankle landmarks for both legs
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate angles for both legs
    left_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = calculate_angle(right_hip, right_knee, right_ankle)

    # Check if the legs are raised and if the knees are above hip level
    left_leg_raised = left_angle > 160 and left_knee.y < left_hip.y and left_ankle.y < left_hip.y
    right_leg_raised = right_angle > 160 and right_knee.y < right_hip.y and right_ankle.y < right_hip.y

    return left_leg_raised, right_leg_raised

def process_frame(frame, pose, leg_raise_count, was_below_threshold):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_leg_raised, right_leg_raised = check_leg_raise(landmarks)
        logging.debug(f'Left leg raised: {left_leg_raised}, Right leg raised: {right_leg_raised}')
        
        # Check the leg raise count
        if (left_leg_raised or right_leg_raised) and not was_below_threshold:
            was_below_threshold = True
        elif not (left_leg_raised or right_leg_raised) and was_below_threshold:
            leg_raise_count += 1
            was_below_threshold = False

        color = (0, 255, 0) if was_below_threshold else (255, 0, 0)
        draw_pose(frame, results.pose_landmarks, color)

    # Display the leg raise count on the screen
    cv2.putText(frame, f'Leg Raise Count: {leg_raise_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame, leg_raise_count, was_below_threshold

# Main function
def main():
    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose()

    leg_raise_count = 0
    was_below_threshold = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame, leg_raise_count, was_below_threshold = process_frame(frame, pose, leg_raise_count, was_below_threshold)
        cv2.putText(frame, f'Leg Raise Count: {leg_raise_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Leg Raise Tracker', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.debug('Program finished')

if __name__ == '__main__':
    main()
