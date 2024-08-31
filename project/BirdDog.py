import cv2
import mediapipe as mp
import numpy as np
import math
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname=s - %(message=s')
logging.debug('Program başladı')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_pose(frame, landmarks, color):
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=color, thickness=2))

def calculate_angle(p1, p2, p3):
    a = np.array([p1.x, p1.y]) - np.array([p2.x, p2.y])
    b = np.array([p3.x, p3.y]) - np.array([p2.x, p2.y])
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    angle = math.acos(dot_product / (magnitude_a * magnitude_b))
    return math.degrees(angle)

def is_visible(landmark):
    return landmark.visibility > 0.5 if hasattr(landmark, 'visibility') else True

def check_bird_dog(landmarks):
    # Bird Dog egzersizinde ilgili eklem noktaları
    relevant_landmarks = [
        mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST,
        mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE,
        mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST,
        mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE
    ]
    
    for landmark in relevant_landmarks:
        if not is_visible(landmarks[landmark.value]):
            return False, False 

    left_arm_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], 
                                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], 
                                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    right_arm_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], 
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], 
                                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    left_leg_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value], 
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value], 
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    right_leg_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value], 
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value], 
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    left_correct = left_arm_angle > 160 and left_leg_angle > 160
    right_correct = right_arm_angle > 160 and right_leg_angle > 160

    return left_correct, right_correct

def process_frame(frame, pose, bird_dog_count, was_correct_position):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_correct, right_correct = check_bird_dog(landmarks)
        
        if left_correct or right_correct:
            if not was_correct_position:
                bird_dog_count += 1
                was_correct_position = True
        else:
            was_correct_position = False
        
        color = (0, 255, 0) if was_correct_position else (255, 0, 0)
        draw_pose(frame, results.pose_landmarks, color)

    return frame, bird_dog_count, was_correct_position

def show_camera():
    cap = cv2.VideoCapture(0)
    bird_dog_count = 0
    was_correct_position = False

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logging.error("Görüntü alınamıyor.")
                break

            frame, bird_dog_count, was_correct_position = process_frame(frame, pose, bird_dog_count, was_correct_position)

            cv2.imshow('Vücut Algılama', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    show_camera()
    logging.debug('Program bitti')
