import logging
import cv2
import mediapipe as mp
import numpy as np
import math

# Logging yapılandırması
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Program başladı')

# MediaPipe Drawing ve Pose modülleri
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_pose(frame, landmarks, color):
    # Vücut eklem noktalarını ve bağlantılarını çiz
    mp_drawing.draw_landmarks(
        frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=color, thickness=2))

def calculate_angle(p1, p2, p3):
    # Açıyı hesaplama
    a = np.array([p1.x, p1.y]) - np.array([p2.x, p2.y])
    b = np.array([p3.x, p3.y]) - np.array([p2.x, p2.y])
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    angle = math.acos(dot_product / (magnitude_a * magnitude_b))
    return math.degrees(angle)

def check_squat(landmarks):
    # Kalça, diz ve ayak bileği landmark'larını her iki bacak için al
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Her iki bacak için açıları hesapla
    left_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = calculate_angle(right_hip, right_knee, right_ankle)

    # Squat düzgün bir şekilde yapılıyorsa her iki bacak için açılar yaklaşık 90 derece olmalıdır
    return left_angle, right_angle

def process_frame(frame, pose, squat_count, was_below_threshold):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_angle, right_angle = check_squat(landmarks)
        if (left_angle < 100 or right_angle < 100) and not was_below_threshold:
            was_below_threshold = True
        elif left_angle > 160 and right_angle > 160 and was_below_threshold:
            squat_count += 1
            was_below_threshold = False

        color = (0, 255, 0) if was_below_threshold else (255, 0, 0)
        draw_pose(frame, results.pose_landmarks, color)

    # Squat sayısını ekrana yazdır
    cv2.putText(frame, f'Squat Count: {squat_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame, squat_count, was_below_threshold

logging.debug('Program bitti')
