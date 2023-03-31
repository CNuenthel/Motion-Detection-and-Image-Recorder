import cv2
import numpy as np
import time
import os

# Specific path for saving images. Images will be saved to current directory script is run in
# This pathway bypasses permission issues with work laptop
#os.chdir(
#    "C:/Users/cnuenthe/OneDrive - State of North Dakota/Desktop/MotionTrack")

# Initialize the camera
cap = cv2.VideoCapture(1)

# Set image resolution
cap.set(3, 640)
cap.set(4, 480)

# Capture a reference frame without any motion
_, ref_frame = cap.read()
ref_frame = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
ref_frame = cv2.GaussianBlur(ref_frame, (21, 21), 0)

# Define motion threshold
motion_threshold = 10000

# Define wait time
wait_time = 20 # seconds

while True:
    # Capture a frame from the camera
    _, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale frame
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Calculate absolute difference between the reference frame and current frame
    diff_frame = cv2.absdiff(ref_frame, gray)

    # Threshold the difference frame
    thresh = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Count non-zero pixels in the thresholded frame
    non_zero_pixels = np.count_nonzero(thresh)

    # If motion is detected, save the current frame to a unique filename
    if non_zero_pixels > motion_threshold:
        for i in range(2):
            time.sleep(2)
            _, frame = cap.read()  
        
            # Generate a unique filename using the timestamp
            file_name = time.strftime("%Y%m%d-%H%M%S") + ".jpg"

            # Save the current frame to the file
            cv2.imwrite(f"SavedImages/{file_name}.jpg", frame)

        # Wait for some time before repeating the loop
        time.sleep(wait_time)

    # Update the reference frame
    ref_frame = gray

    # Display the frame with motion detection
    cv2.imshow("Motion Detection", frame)

    # Check for user input to stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
