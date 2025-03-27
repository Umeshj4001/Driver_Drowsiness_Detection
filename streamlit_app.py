import streamlit as st
import sys
import subprocess

# Function to install packages
def install_package(package):
    st.info(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    st.success(f"Successfully installed {package}")

# Try importing required packages
try:
    import cv2
except ImportError:
    st.error("OpenCV not found. Installing now...")
    install_package("opencv-python")
    import cv2

try:
    import numpy as np
except ImportError:
    st.error("NumPy not found. Installing now...")
    install_package("numpy")
    import numpy as np

import time
from datetime import datetime
import threading
import base64
try:
    from PIL import Image
except ImportError:
    st.error("Pillow not found. Installing now...")
    install_package("Pillow")
    from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Driver Drowsiness Detection",
    page_icon="🚗",
    layout="wide"
)

# Initialize session state variables
if 'drowsiness_detected' not in st.session_state:
    st.session_state.drowsiness_detected = False
if 'alert_active' not in st.session_state:
    st.session_state.alert_active = False
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'session_duration' not in st.session_state:
    st.session_state.session_duration = 0
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'sensitivity' not in st.session_state:
    st.session_state.sensitivity = 5
if 'alert_volume' not in st.session_state:
    st.session_state.alert_volume = 7
if 'alert_type' not in st.session_state:
    st.session_state.alert_type = "both"

# Constants
EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 20  # Number of consecutive frames for drowsiness detection

def initialize_opencv():
    # Load the pre-trained Haar cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    return face_cascade, eye_cascade

def eye_aspect_ratio(eye):
    # Calculate the eye aspect ratio
    # This is a simplified version - in a real implementation, you'd use facial landmarks
    # to calculate the actual eye aspect ratio
    height, width = eye.shape[:2]
    return height / width if width > 0 else 0

def detect_drowsiness(frame, face_cascade, eye_cascade):
    # Process frame for drowsiness detection
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
        st.session_state.counter = 0
        st.session_state.drowsiness_detected = False
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
            eyes_closed = 0
            
            # Draw rectangles around eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
                
                # Extract eye region
                eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
                
                # Calculate eye aspect ratio (simplified)
                ear = eye_aspect_ratio(eye_roi)
                
                # Check if eye is closed based on aspect ratio
                if ear < EYE_AR_THRESH:
                    eyes_closed += 1
            
            # If all detected eyes are closed
            if eyes_closed == len(eyes):
                st.session_state.counter += 1
            else:
                st.session_state.counter = 0
        else:
            # If eyes are not detected, increment counter
            st.session_state.counter += 1
        
        # Check if drowsiness is detected
        if st.session_state.counter >= EYE_AR_CONSEC_FRAMES:
            st.session_state.drowsiness_detected = True
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Increment alert count when drowsiness is first detected
            if not st.session_state.alert_active:
                st.session_state.alert_count += 1
                st.session_state.alert_active = True
        else:
            st.session_state.drowsiness_detected = False
            st.session_state.alert_active = False
    
    return frame

def start_monitoring():
    st.session_state.monitoring = True
    st.session_state.start_time = time.time()
    st.session_state.session_duration = 0
    st.session_state.alert_count = 0

def stop_monitoring():
    st.session_state.monitoring = False
    st.session_state.start_time = None

def update_session_duration():
    if st.session_state.monitoring and st.session_state.start_time:
        current_time = time.time()
        st.session_state.session_duration = int(current_time - st.session_state.start_time)

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def main():
    st.title("Driver Drowsiness Detection System")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Camera Feed")
        # Placeholder for the camera feed
        video_placeholder = st.empty()
        
    with col2:
        st.header("Status")
        
        # Status indicator
        status_placeholder = st.empty()
        
        # Stats section
        st.subheader("Statistics")
        duration_placeholder = st.empty()
        alerts_placeholder = st.empty()
        
        # Controls section
        st.subheader("Controls")
        control_cols = st.columns(2)
        
        with control_cols[0]:
            if not st.session_state.monitoring:
                start_button = st.button("Start Monitoring", key="start", on_click=start_monitoring)
            else:
                start_button = st.button("Start Monitoring", key="start", on_click=start_monitoring, disabled=True)
        
        with control_cols[1]:
            if st.session_state.monitoring:
                stop_button = st.button("Stop Monitoring", key="stop", on_click=stop_monitoring)
            else:
                stop_button = st.button("Stop Monitoring", key="stop", on_click=stop_monitoring, disabled=True)
        
        # Settings section
        st.subheader("Settings")
        st.session_state.sensitivity = st.slider("Detection Sensitivity", 1, 10, st.session_state.sensitivity)
        st.session_state.alert_volume = st.slider("Alert Volume", 0, 10, st.session_state.alert_volume)
        st.session_state.alert_type = st.selectbox("Alert Type", ["beep", "voice", "both"], index=2)
    
    # Initialize OpenCV
    face_cascade, eye_cascade = initialize_opencv()
    
    # Create a video capture object
    cap = cv2.VideoCapture(0)
    
    try:
        # Main application loop
        while True:
            # Update session duration
            update_session_duration()
            
            # Update status display
            if st.session_state.drowsiness_detected:
                status_placeholder.markdown('<div style="background-color: red; color: white; padding: 10px; border-radius: 5px; text-align: center;"><h3>DROWSINESS DETECTED!</h3></div>', unsafe_allow_html=True)
            else:
                if st.session_state.monitoring:
                    status_placeholder.markdown('<div style="background-color: green; color: white; padding: 10px; border-radius: 5px; text-align: center;"><h3>Monitoring...</h3></div>', unsafe_allow_html=True)
                else:
                    status_placeholder.markdown('<div style="background-color: gray; color: white; padding: 10px; border-radius: 5px; text-align: center;"><h3>Not Monitoring</h3></div>', unsafe_allow_html=True)
            
            # Update statistics
            duration_placeholder.markdown(f"**Session Duration:** {format_duration(st.session_state.session_duration)}")
            alerts_placeholder.markdown(f"**Alerts:** {st.session_state.alert_count}")
            
            if st.session_state.monitoring:
                # Capture frame-by-frame
                ret, frame = cap.read()
                
                if ret:
                    # Process frame for drowsiness detection
                    frame = detect_drowsiness(frame, face_cascade, eye_cascade)
                    
                    # Convert the frame to RGB (from BGR)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Display the frame
                    video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                else:
                    st.error("Failed to capture video frame")
                    break
            else:
                # Display a placeholder image when not monitoring
                video_placeholder.markdown("Camera feed will appear here when monitoring is started.")
            
            # Add a short delay
            time.sleep(0.1)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        # Release the video capture when done
        cap.release()

if __name__ == "__main__":
    main() 