import cv2
import time
import threading
import os

# Specific path for saving images. Images will be saved to current directory script is run in
# This pathway bypasses permission issues with work laptop
#os.chdir(
#    "C:/Users/cnuenthe/OneDrive - State of North Dakota/Desktop/MotionTrack")

# Create a VideoCapture object and set the camera index to 0 (default webcam)
cap = cv2.VideoCapture(0)
time.sleep(2)

# Define the minimum motion threshold
motion_threshold = 100000

# set camera resolution
cap.set(3, 640)
cap.set(4, 480)


# Define a variable to keep track of the last frame
last_frame = None

# Define a function to capture and save images
def capture_and_save():
    # Wait for 2 seconds
    time.sleep(2)
    # Capture the current frame
    ret, frame = cap.read()
    # Save the first image
    filename = f"motion-{time.time()}.jpg"
    cv2.imwrite(f"SavedImages/{filename}.jpg", frame)
    # Wait for 2 more seconds
    time.sleep(2)
    # Capture the current frame again
    ret, frame = cap.read()
    # Save the second image
    filename = f"motion-{time.time()}.jpg"
    cv2.imwrite(f"SavedImages/{filename}.jpg", frame)

# Define a function to detect motion and start a new thread to save images
def detect_motion():
    global last_frame
    while True:
        # Capture the current frame
        ret, frame = cap.read()
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blur the frame to reduce noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # If the last frame is not None, compute the difference between the current frame and the last frame
        if last_frame is not None:
            diff = cv2.absdiff(last_frame, gray)
            # Threshold the difference image to get a binary image of moving areas
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            # Count the number of non-zero pixels in the binary image
            motion_count = cv2.countNonZero(thresh)
            # If the number of moving pixels is above the threshold, start a new thread to save images
            if motion_count > motion_threshold:
                thread = threading.Thread(target=capture_and_save)
                thread.start()
        # Update the last frame
        last_frame = gray.copy()

        # Display the frame with motion detection
        cv2.imshow("Motion Detection", frame)

        # Check for user input to stop the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Introduce a delay of 100 milliseconds (i.e., 1/10th of a second)
        time.sleep(0.1)

# Start the motion detection thread
thread = threading.Thread(target=detect_motion)
thread.start()

# Wait for the thread to finish (which it won't, unless there's an error or the program is interrupted)
thread.join()

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()