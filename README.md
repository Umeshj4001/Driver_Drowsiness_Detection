# Driver Drowsiness Detection System

A real-time driver drowsiness detection system using computer vision and web technologies. This system monitors a driver's face through a webcam and alerts them when signs of drowsiness are detected.

## Features

- Real-time face and eye detection using OpenCV
- Drowsiness detection based on eye aspect ratio
- Visual and audio alerts when drowsiness is detected
- User-friendly web interface with camera feed and status display
- Google Sign-In authentication
- Customizable settings for alert sensitivity and volume

## Tech Stack

- **Backend**: Python with Flask
- **Computer Vision**: OpenCV
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Google Sign-In API

## Prerequisites

- Python 3.7+
- Webcam
- Modern web browser (Chrome, Firefox, Edge)
- Internet connection (for Google Sign-In)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/driver-drowsiness-detection.git
   cd driver-drowsiness-detection
   ```
2. Create a virtual environment (recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Add an alert sound file:

   - Download an alert sound (MP3 format)
   - Save it as `static/audio/alert.mp3`
5. Configure Google Sign-In:

   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Set up OAuth 2.0 credentials
   - Replace `YOUR_GOOGLE_CLIENT_ID` in `templates/index.html` with your actual client ID

## Usage

1. Start the application:

   ```
   python app.py
   ```
2. Open your web browser and navigate to:

   ```
   http://127.0.0.1:5000
   ```
3. Sign in with your Google account when prompted
4. Click "Start Monitoring" to begin drowsiness detection
5. The system will alert you when signs of drowsiness are detected

## Customization

You can customize the following settings through the UI:

- Detection sensitivity
- Alert volume
- Alert type (beep, voice, or both)

## Future Improvements

- Integration with Bootstrap for enhanced UI
- Mobile app version
- Data logging and analytics
- Integration with vehicle systems
- Machine learning for improved detection accuracy

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV community
- Flask framework
- Google Sign-In API
