import cv2
import mediapipe as mp

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam capture.
cap = cv2.VideoCapture(0)

# Zoom factor control
current_zoom_factor = 1.0  # Start with no zoom


# Function to check thumb position relative to other fingers 
#   This function compares the vertical position of thumb to the 
#   vertical position of fingers 

# Note: Lower values means higher in the frame (origin in top-left corner)

def check_thumb_position(hand_landmarks, comparison):
    
    # Extracts vertical position of thumb 
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y 

    # Extracts vertical position of remaining fingers 
    finger_tips_y = [hand_landmarks.landmark[finger_tip].y for finger_tip in [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP]]
    
    # compare vertical height of thumb and finger with min height (highest in frame)- returns boolean 
    return comparison(thumb_tip, min(finger_tips_y))

# Function to zoom image in (zoom_factor indicated how much the image should be zoomed in)
def zoom_image(image, zoom_factor):
    if zoom_factor == 1.0:  # No zoom needed
        return image
    
    # Extract the original height and width of the image 
    height, width = image.shape[:2]

    # Compute new dimensions (zoom in if ZF > 1, zoom out if ZF < 1)
    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

    # Rescale image to new dimensions 
    resized_image = cv2.resize(image, (new_width, new_height))

    # calculates top-left coordinates - ensures final image has same dimensions as original 
    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2

    # crops image while keeping original dimensions - this step is what creates the zooming effect 
    cropped_image = resized_image[start_y:start_y+height, start_x:start_x+width]
    return cropped_image

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    zoom_changed = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for thumbs-up (zoom in)
            if check_thumb_position(hand_landmarks, lambda thumb, others: thumb < others):
                current_zoom_factor *= 1.1  # Increase zoom by 10%
                zoom_changed = True

            # Check for thumbs-down (zoom out)
            elif check_thumb_position(hand_landmarks, lambda thumb, others: thumb > others):
                current_zoom_factor /= 1.1  # Decrease zoom by 10%
                zoom_changed = True

    # Apply the current zoom factor, if changed
    if zoom_changed:
        current_zoom_factor = max(1.0, min(current_zoom_factor, 3.0))  # Limit zoom factor range for practicality
        image = zoom_image(image, current_zoom_factor)

    cv2.imshow('MediaPipe Hands', image)

    # Press escape to exit 
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
