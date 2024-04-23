# ai_companion.py
import subprocess
import time
import os

# Function to run the window scripts
def run_window_scripts():
    # Run the window scripts as separate subprocesses
    window1_process = subprocess.Popen(["python", "ai_companion_window1.py"])
    window2_process = subprocess.Popen(["python", "ai_companion_window2.py"])

    # Wait for the window scripts to finish
    window1_process.wait()
    window2_process.wait()

# Main function
def main():
    # Start running the window scripts
    run_window_scripts()

if __name__ == "__main__":
    main()
