"""
This script verifies and installs the required dependencies for the Drowsiness Detection app.
Run this script before running the main application if you're experiencing import errors.
"""
import sys
import subprocess
import pkg_resources

required_packages = {
    'streamlit': '1.35.0',
    'numpy': '1.26.4',
    'opencv-python': '4.9.0.80',
    'Pillow': '10.2.0'
}

def check_and_install():
    # Get installed packages
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    missing = []
    outdated = []
    
    # Check for missing or outdated packages
    for package, version in required_packages.items():
        if package.lower() not in installed:
            missing.append(f"{package}=={version}")
        elif installed[package.lower()] != version:
            outdated.append(f"{package}=={version}")
    
    # Install missing packages
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Update outdated packages
    if outdated:
        print(f"Updating outdated packages: {', '.join(outdated)}")
        for package in outdated:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    
    if not missing and not outdated:
        print("All required packages are already installed with the correct versions.")
    else:
        print("All required packages have been installed or updated.")

if __name__ == "__main__":
    print("Checking and installing required packages...")
    check_and_install()
    print("\nSetup complete. You can now run the main application with: streamlit run streamlit_app.py") 