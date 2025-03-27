document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const videoFeed = document.getElementById('video-feed');
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const sessionDuration = document.getElementById('session-duration');
    const alertCount = document.getElementById('alert-count');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const settingsBtn = document.getElementById('settings-btn');
    const loginModal = document.getElementById('login-modal');
    const settingsModal = document.getElementById('settings-modal');
    const closeButtons = document.querySelectorAll('.close');
    const alertSound = document.getElementById('alert-sound');
    const sensitivitySlider = document.getElementById('sensitivity');
    const sensitivityValue = document.getElementById('sensitivity-value');
    const alertVolumeSlider = document.getElementById('alert-volume');
    const volumeValue = document.getElementById('volume-value');
    const alertTypeSelect = document.getElementById('alert-type');
    const saveSettingsBtn = document.getElementById('save-settings');

    // State variables
    let isMonitoring = false;
    let sessionStartTime = null;
    let sessionTimer = null;
    let alertsCount = 0;
    let isUserLoggedIn = true; // User Logging (Without logging = true )
    let checkDrowsinessInterval = null;
    
    // Settings
    let settings = {
        sensitivity: 5,
        alertVolume: 7,
        alertType: 'both'
    };

    // Show login modal on page load
    window.addEventListener('load', function() {
        if (!isUserLoggedIn) {
            loginModal.style.display = 'block';
        }
    });

    // Close modals when clicking the close button
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            loginModal.style.display = 'none';
            settingsModal.style.display = 'none';
        });
    });

    // Close modals when clicking outside the modal content
    window.addEventListener('click', function(event) {
        if (event.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (event.target === settingsModal) {
            settingsModal.style.display = 'none';
        }
    });

    // Handle Google Sign-In
    window.handleCredentialResponse = function(response) {
        // In a real application, you would verify the credential with your backend
        console.log("Google Sign-In successful:", response);
        isUserLoggedIn = true;
        loginModal.style.display = 'none';
    };

    // Start monitoring button
    startBtn.addEventListener('click', function() {
        if (!isUserLoggedIn) {
            loginModal.style.display = 'block';
            return;
        }

        isMonitoring = true;
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusIndicator.className = 'status-normal';
        statusText.textContent = 'Monitoring...';
        
        // Start session timer
        sessionStartTime = new Date();
        sessionTimer = setInterval(updateSessionDuration, 1000);
        
        // Start checking for drowsiness
        startDrowsinessDetection();
    });

    // Stop monitoring button
    stopBtn.addEventListener('click', function() {
        isMonitoring = false;
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusIndicator.className = 'status-normal';
        statusText.textContent = 'Monitoring stopped';
        
        // Stop session timer
        clearInterval(sessionTimer);
        
        // Stop checking for drowsiness
        stopDrowsinessDetection();
    });

    // Settings button
    settingsBtn.addEventListener('click', function() {
        if (!isUserLoggedIn) {
            loginModal.style.display = 'block';
            return;
        }
        
        // Update settings UI with current values
        sensitivitySlider.value = settings.sensitivity;
        sensitivityValue.textContent = settings.sensitivity;
        alertVolumeSlider.value = settings.alertVolume;
        volumeValue.textContent = settings.alertVolume;
        alertTypeSelect.value = settings.alertType;
        
        settingsModal.style.display = 'block';
    });

    // Update sensitivity value display
    sensitivitySlider.addEventListener('input', function() {
        sensitivityValue.textContent = this.value;
    });

    // Update volume value display
    alertVolumeSlider.addEventListener('input', function() {
        volumeValue.textContent = this.value;
    });

    // Save settings
    saveSettingsBtn.addEventListener('click', function() {
        settings.sensitivity = parseInt(sensitivitySlider.value);
        settings.alertVolume = parseInt(alertVolumeSlider.value);
        settings.alertType = alertTypeSelect.value;
        
        // Apply settings
        alertSound.volume = settings.alertVolume / 10;
        
        settingsModal.style.display = 'none';
    });

    // Update session duration display
    function updateSessionDuration() {
        if (!sessionStartTime) return;
        
        const now = new Date();
        const diff = now - sessionStartTime;
        
        const hours = Math.floor(diff / 3600000).toString().padStart(2, '0');
        const minutes = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
        const seconds = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
        
        sessionDuration.textContent = `${hours}:${minutes}:${seconds}`;
    }

    // Start drowsiness detection
    function startDrowsinessDetection() {
        // Check for drowsiness every second
        checkDrowsinessInterval = setInterval(checkDrowsiness, 1000);
    }

    // Stop drowsiness detection
    function stopDrowsinessDetection() {
        clearInterval(checkDrowsinessInterval);
    }

    // Check for drowsiness by querying the backend
    function checkDrowsiness() {
        if (!isMonitoring) return;
        
        fetch('/check_drowsiness')
            .then(response => response.json())
            .then(data => {
                if (data.drowsiness_detected) {
                    // Update UI to show alert
                    statusIndicator.className = 'status-alert';
                    statusText.textContent = 'DROWSINESS DETECTED!';
                    
                    // Play alert sound
                    if (settings.alertType === 'beep' || settings.alertType === 'both') {
                        alertSound.play();
                    }
                    
                    // Increment alert count
                    alertsCount++;
                    alertCount.textContent = alertsCount;
                } else {
                    // Reset UI to normal state
                    statusIndicator.className = 'status-normal';
                    statusText.textContent = 'Monitoring...';
                }
            })
            .catch(error => {
                console.error('Error checking drowsiness:', error);
            });
    }
}); 