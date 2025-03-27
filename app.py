from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import time
import threading
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Global variables
drowsiness_detected = False
alert_active = False
face_cascade = None
eye_cascade = None
video_capture = None
EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 20  # Number of consecutive frames for drowsiness detection
COUNTER = 0

def initialize_opencv():
    global face_cascade, eye_cascade
    # Load the pre-trained Haar cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def eye_aspect_ratio(eye):
    # Calculate the eye aspect ratio
    # This is a simplified version - in a real implementation, you'd use facial landmarks
    # to calculate the actual eye aspect ratio
    height, width = eye.shape[:2]
    return height / width if width > 0 else 0

def detect_drowsiness(frame):
    global COUNTER, drowsiness_detected, alert_active
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Reset drowsiness flag if no faces detected
    if len(faces) == 0:
        COUNTER = 0
        drowsiness_detected = False
        return frame
    
    # Process each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Region of interest for the face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        if len(eyes) >= 2:  # At least two eyes detected
            # Reset counter if eyes are open
            COUNTER = 0
            drowsiness_detected = False
            
            # Draw rectangles around eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
                
                # Extract eye region
                eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
                
                # Calculate eye aspect ratio (simplified)
                ear = eye_aspect_ratio(eye_roi)
                
                # Check if eye is closed based on aspect ratio
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    COUNTER = 0
        else:
            # If eyes are not detected, increment counter
            COUNTER += 1
        
        # Check if drowsiness is detected
        if COUNTER >= EYE_AR_CONSEC_FRAMES:
            drowsiness_detected = True
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            drowsiness_detected = False
    
    return frame

def generate_frames():
    global video_capture
    
    # Initialize video capture
    if video_capture is None:
        video_capture = cv2.VideoCapture(0)
    
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        
        # Process frame for drowsiness detection
        processed_frame = detect_drowsiness(frame)
        
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the frame in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_drowsiness')
def check_drowsiness():
    return jsonify({'drowsiness_detected': drowsiness_detected})

def cleanup():
    global video_capture
    if video_capture is not None:
        video_capture.release()

if __name__ == '__main__':
    initialize_opencv()
    try:
        app.run(debug=True, threaded=True)
    finally:
        cleanup() 