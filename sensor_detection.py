# sensor_detection.py
import cv2  # For person detection using OpenCV

#---------------------------------------------- Functions -------------------------------------------------------------#

def detect_person():
    """Detect a person using the webcam."""
    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    face_detected_frames = 0  # Counter for consecutive frames with detected faces
    frames_to_confirm = 10    # Number of consecutive frames to confirm presence of a person

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        persons = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(80, 80),  # Increase minSize to detect only larger faces
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Check if any faces are detected
        if len(persons) > 0:
            for (x, y, w, h) in persons:
                frame_center_x = frame.shape[1] // 2
                frame_center_y = frame.shape[0] // 2
                face_center_x = x + w // 2
                face_center_y = y + h // 2

                margin = 100  # Define a margin for center detection

                # If the face is near the center, consider it a valid detection
                if (frame_center_x - margin < face_center_x < frame_center_x + margin and
                        frame_center_y - margin < face_center_y < frame_center_y + margin):
                    face_detected_frames += 1
                    break  # Only count one face per frame
            else:
                # No valid face near the center detected
                face_detected_frames = 0
        else:
            face_detected_frames = 0

        # If a face is detected for a sufficient number of consecutive frames
        if face_detected_frames >= frames_to_confirm:
            print("Person detected!")
            break

        # Display the frame (for debugging purposes)
        cv2.imshow("Frame", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()
