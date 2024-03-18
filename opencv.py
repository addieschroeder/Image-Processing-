import cv2
import numpy as np

# Initialize webcam capture
cap = cv2.VideoCapture(1)

# Zoom factor control
current_zoom_factor = 1.0  # Start with no zoom


def detect_skin(frame):
    # Convert frame to HSV color space for easier color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    # Detect skin based on range
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    return mask

def interpret_gesture(mask):
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Assume largest contour by area is the hand
        largest_contour = max(contours, key=cv2.contourArea)
        # Example: Check if the contour's area is within a certain range for simplicity
        area = cv2.contourArea(largest_contour)
        if area > 1000:  # Example threshold, needs tuning
            return "zoom_in"  # Placeholder for actual gesture recognition logic
    return "none"

def zoom_image(image, zoom_factor):
    if zoom_factor == 1.0:  # No zoom needed
        return image

    height, width = image.shape[:2]
    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

    # Resizing the image as the first step of zooming
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Calculating the cropping frame
    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2

    # Cropping the resized image to fit the original size
    cropped_image = resized_image[start_y:start_y+height, start_x:start_x+width]

    return cropped_image

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Skin detection
    skin_mask = detect_skin(frame)
    
    # Gesture interpretation based on the skin mask
    gesture = interpret_gesture(skin_mask)
    
    if gesture == "zoom_in":
        current_zoom_factor *= 1.01
    # Assuming another gesture "zoom_out" for demonstration
    elif gesture == "zoom_out":
        current_zoom_factor /= 1.01

    
    cv2.imshow('Gesture Recognition', zoom_image(frame, 1.01))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
