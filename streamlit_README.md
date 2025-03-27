# Driver Drowsiness Detection System - Streamlit Version

This is a Streamlit application for real-time driver drowsiness detection using computer vision techniques. The application uses your webcam to monitor eye movements and detect signs of drowsiness.

## Features

- Real-time drowsiness detection through webcam
- Visual and audio alerts when drowsiness is detected
- Session statistics (duration, alert count)
- Customizable sensitivity and alert settings
- Clean and intuitive user interface

## Requirements

- Python 3.7+
- Webcam/Camera

## Installation

1. Clone this repository or download the project files.
2. Install the required dependencies:

```bash
pip install -r streamlit_requirements.txt
```

## Usage

1. Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

2. The application will open in your default web browser.
3. Click the "Start Monitoring" button to begin drowsiness detection.
4. The application will use your webcam to monitor your eyes for signs of drowsiness.
5. If drowsiness is detected, an alert will be displayed.
6. You can adjust the sensitivity and alert settings in the settings panel.
7. Click the "Stop Monitoring" button to end the session.

## How It Works

The application uses the Haar Cascade Classifier from OpenCV to detect faces and eyes in the video stream. It then calculates the eye aspect ratio (width-to-height ratio) to determine if the eyes are closed. If the eyes remain closed for a certain number of consecutive frames, the system considers the driver to be drowsy and triggers an alert.

## Differences from Flask Version

This Streamlit version offers the same core functionality as the original Flask application, but with these differences:

- Uses Streamlit's reactive framework instead of Flask's server-based approach
- State management through Streamlit's session state instead of global variables
- UI elements are rendered using Streamlit's widgets instead of HTML/CSS/JS
- No separate HTML template files needed

## License

[MIT License](LICENSE)
