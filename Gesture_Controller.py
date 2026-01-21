import cv2
import mediapipe as mp
import pyautogui
import math
import time

pyautogui.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize video capture
cap = cv2.VideoCapture(0)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Camera frame dimensions (will be set after first frame)
cam_width, cam_height = 0, 0

# Define detection box (use only center portion of camera for better control)
# Adjust these values: smaller = more sensitive, larger = more stable
box_left = 0.1  # 10% from left
box_right = 0.9  # 90% from left (80% of frame width)
box_top = 0.1  # 10% from top
box_bottom = 0.9  # 90% from bottom (80% of frame height)

# Smoothing variables
prev_x, prev_y = 0, 0
smoothing = 5  # Lower value = more responsive

# Gesture state tracking
prev_gesture = None
gesture_start_time = 0
gesture_delay = 0.5  # Delay between repeated actions


# Function to classify gestures based on finger states
def classify_gesture(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Check thumb (left/right position)
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Check other fingers (up/down position)
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = sum(fingers)

    # Map finger states to gestures
    if total_fingers == 5:
        return 'OPEN_PALM'  # Move mouse
    elif total_fingers == 0:
        return 'FIST'  # Click
    elif fingers[1] == 1 and sum(fingers[2:]) == 0:
        return 'POINT_INDEX'  # Right click
    elif fingers[1] == 1 and fingers[2] == 1 and sum(fingers[3:]) == 0:
        return 'TWO_FINGERS'  # Double click
    else:
        return 'UNKNOWN'


# Main loop
with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
) as hands:
    print("Gesture Mouse Control Started!")
    print("Gestures:")
    print("  - Open Palm (5 fingers): Move mouse")
    print("  - Fist (0 fingers): Left click")
    print("  - Index finger only: Right click")
    print("  - Index + Middle finger: Double click")
    print("Press 'Esc' to exit")

    while True:
        success, image = cap.read()
        if not success:
            print("Failed to capture image")
            break

        # Get camera dimensions
        height, width, _ = image.shape
        if cam_width == 0:
            cam_width, cam_height = width, height

        # Flip and convert image to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        # Convert back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw detection box
        box_x1 = int(width * box_left)
        box_y1 = int(height * box_top)
        box_x2 = int(width * box_right)
        box_y2 = int(height * box_bottom)
        cv2.rectangle(image, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)
        cv2.putText(image, 'Control Zone', (box_x1 + 5, box_y1 + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        current_time = time.time()

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Classify gesture
            gesture = classify_gesture(hand_landmarks)

            # Get coordinates for mouse movement
            index_finger_tip = hand_landmarks.landmark[8]

            # Get raw hand position
            hand_x = index_finger_tip.x * width
            hand_y = index_finger_tip.y * height

            # Map the detection box to full screen
            # Clamp hand position within detection box
            hand_x = max(box_x1, min(hand_x, box_x2))
            hand_y = max(box_y1, min(hand_y, box_y2))

            # Normalize to 0-1 range within detection box
            norm_x = (hand_x - box_x1) / (box_x2 - box_x1)
            norm_y = (hand_y - box_y1) / (box_y2 - box_y1)

            # Map to full screen coordinates with amplification
            x = int(norm_x * screen_width)
            y = int(norm_y * screen_height)

            # Apply smoothing for mouse movement
            curr_x = prev_x + (x - prev_x) / smoothing
            curr_y = prev_y + (y - prev_y) / smoothing

            prev_x, prev_y = curr_x, curr_y

            # Map gestures to actions
            if gesture == 'OPEN_PALM':
                # Move mouse smoothly
                pyautogui.moveTo(curr_x, curr_y, duration=0.1)
                cv2.putText(image, 'Moving Mouse', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif gesture == 'FIST':
                # Left click with delay to prevent multiple clicks
                if prev_gesture != 'FIST' or (current_time - gesture_start_time) > gesture_delay:
                    pyautogui.click()
                    gesture_start_time = current_time
                    cv2.putText(image, 'Left Click', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            elif gesture == 'POINT_INDEX':
                # Right click with delay
                if prev_gesture != 'POINT_INDEX' or (current_time - gesture_start_time) > gesture_delay:
                    pyautogui.rightClick()
                    gesture_start_time = current_time
                    cv2.putText(image, 'Right Click', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            elif gesture == 'TWO_FINGERS':
                # Double click with delay
                if prev_gesture != 'TWO_FINGERS' or (current_time - gesture_start_time) > gesture_delay:
                    pyautogui.doubleClick()
                    gesture_start_time = current_time
                    cv2.putText(image, 'Double Click', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                cv2.putText(image, 'Unknown Gesture', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)

            prev_gesture = gesture

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

        else:
            cv2.putText(image, 'No Hand Detected', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display instructions
        cv2.putText(image, 'Press ESC to exit', (10, height - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, f'Screen: {screen_width}x{screen_height}', (10, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Show the image
        cv2.imshow('Gesture Mouse Control', image)

        # Exit on pressing 'Esc'
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Gesture Mouse Control Stopped!")