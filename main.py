import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define colors for drawing
line_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)  # Green for lines
dot_spec = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)   # Red for dots

# Start video capture
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera started successfully!")

while True:
    ret, frame = cap.read()
    h, w, c = frame.shape
    if not ret:
        print("Failed to capture frame")
        break

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            print(f"Hand {hand_no + 1} Landmarks:")
            lm_list = []   # List to store landmark positions

            for i, lm in enumerate(hand_landmarks.landmark):
                lm_list.append(lm) # Append each landmark to the list

            for tip in finger_tips:
                x = int(lm_list[tip].x * w)  # Store x-coordinate
                y = int(lm_list[tip].y * h)  # Store y-coordinate

                print(f"  Landmark {tip}: x={x}, y={y}") # Print coordinates

                # Draw a circle at the fingertip position
                cv2.circle(frame, (x, y), 12, (255, 0, 0), cv2.FILLED)


            # Draw hand landmarks on the frame with red dots and green lines
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                dot_spec, line_spec
            )

    # Show the output frame
    cv2.imshow("Hand Tracking", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
print("Camera released and windows closed.")
