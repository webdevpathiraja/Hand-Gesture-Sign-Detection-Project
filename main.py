import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define colors for drawing
line_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)  # Green for lines
dot_spec = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)  # Red for dots

# Start video capture
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera started successfully!")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
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
            lm_list = []  # List to store landmark positions
            finger_fold_status = []

            for i, lm in enumerate(hand_landmarks.landmark):
                lm_list.append(lm)  # Append each landmark to the list

            for tip in finger_tips:
                x = int(lm_list[tip].x * w)  # Store x-coordinate
                y = int(lm_list[tip].y * h)  # Store y-coordinate

                # print(f"  Landmark {tip}: x={x}, y={y}") # Print coordinates

                # Draw a circle at the fingertip position
                cv2.circle(frame, (x, y), 12, (100, 149, 237), cv2.FILLED)

                # change the color of the fingertip if the finger is folded
                # if the fingertip's x is smaller than the finger's base x, that finger is folded
                if lm_list[tip].x < lm_list[tip - 3].x:

                    # change the color of the fingertip indicator to differentiate the folded state
                    cv2.circle(frame, (x, y), 12, (151, 53, 255), cv2.FILLED)
                    finger_fold_status.append(True)

                else:
                    finger_fold_status.append(False)

            print(finger_fold_status)

            # *************** LIKE (Thumbs-up) 👍 ***************
            # if the thumb is positioned upwards
            # the thumb tip should be above its previous joints
            # that is the thumb tip's y must be lower than its previous joint's y values

            if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y:

                # Verify if all other fingers are folded (indicating a thumbs-up gesture)
                if all(finger_fold_status):
                    print("LIKE👍 gesture detected")
                    cv2.putText(frame, "LIKE", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


            # *************** DISLIKE (Thumbs-down)👎 ***************
            # if the thumb is positioned downwards
            # the thumb tip must be below its previous joints
            # that is the thumb tip's y must be greater than its previous joint's y values

            if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
                if all(finger_fold_status):
                    print("DISLIKE👎 gesture detected")
                    cv2.putText(frame, "DISLIKE", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # ************************ OK 👌 ************************
            # check if thumb tip and index tip are close
            thumb_x, thumb_y = lm_list[thumb_tip].x, lm_list[thumb_tip].y
            index_x, index_y = lm_list[8].x, lm_list[8].y  # Index finger tip

            distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

            if distance < 0.05:  # Small threshold to detect touch

                # Check if the other three fingers are extended (not folded)
                if not finger_fold_status[1] and not finger_fold_status[2] and not finger_fold_status[3]:
                    print("OK👌 gesture detected")
                    cv2.putText(frame, "OK", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** PEACE ✌️ ***********************
            # check if thumb, ring, and pinky are close (using distance calculation)
            thumb_x, thumb_y = lm_list[thumb_tip].x, lm_list[thumb_tip].y
            ring_x, ring_y = lm_list[16].x, lm_list[16].y  # Ring fingertip
            pinky_x, pinky_y = lm_list[20].x, lm_list[20].y  # Pinky fingertip

            # calculate the distance between thumb, ring, and pinky tips
            distance_thumb_ring = ((thumb_x - ring_x) ** 2 + (thumb_y - ring_y) ** 2) ** 0.5
            distance_ring_pinky = ((ring_x - pinky_x) ** 2 + (ring_y - pinky_y) ** 2) ** 0.5

            if distance_thumb_ring < 0.05 and distance_ring_pinky < 0.05:  # check if the fingers are close
                # check if the index and middle fingers are extended (not folded)
                if not finger_fold_status[0] and not finger_fold_status[1]:  # index and middle fingers
                    print("PEACE✌️ gesture detected")
                    cv2.putText(frame, "PEACE", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** CALL ME 🤙 ***********************
            # check if middle, index, and pinky fingers are folded (their fold status is True)
            if finger_fold_status[0] and finger_fold_status[1] and finger_fold_status[3]:  # index, middle, pinky folded

                # check if the thumb and pinky are extended and far apart
                thumb_x, thumb_y = lm_list[thumb_tip].x, lm_list[thumb_tip].y
                pinky_x, pinky_y = lm_list[20].x, lm_list[20].y  # pinky finger tip

                # calculate distance between thumb and pinky
                distance_thumb_pinky = ((thumb_x - pinky_x) ** 2 + (thumb_y - pinky_y) ** 2) ** 0.5

                # if the distance between the thumb and pinky is high
                if distance_thumb_pinky > 0.4:
                    print("Call ME🤙 gesture detected")
                    cv2.putText(frame, "CALL ME", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** Stop ✋ ***********************
            # check if all fingers are extended (upward)
            if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and \
                    lm_list[8].y < lm_list[6].y < lm_list[5].y and \
                    lm_list[12].y < lm_list[10].y < lm_list[9].y and \
                    lm_list[16].y < lm_list[14].y < lm_list[13].y and \
                    lm_list[20].y < lm_list[18].y < lm_list[17].y:
                print("Stop✋ gesture detected")
                cv2.putText(frame, "STOP", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # *********************** FORWARD 👆 ***********************
            # check if index finger is extended upward (8.y < 6.y)
            # check if all 3 middle, ring and pinky fingers are folded
            # check if the thumb finger is folded (4.x < 3.x)
            if lm_list[8].y < lm_list[6].y < lm_list[5].y and \
                lm_list[12].y > lm_list[11].y > lm_list[10].y and \
                lm_list[16].y > lm_list[15].y > lm_list[14].y and \
                lm_list[20].y > lm_list[19].y > lm_list[18].y and \
                lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x:
                print("FORWARD✋ gesture detected")
                cv2.putText(frame, "FORWARD", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** LEFT 👈 ***********************
            # check if thumb is raised upwards (4.y < 2.y)
            # check if all 3 middle, ring and pinky finger's x coordinates
            # all 3 fingertips' x > finger's other two joints' x
            # check if index finger's base 5.x < wrist 0.x
            if lm_list[4].y < lm_list[2].y and \
                    lm_list[8].x < lm_list[6].x and \
                    lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and \
                    lm_list[20].x > lm_list[18].x and \
                    lm_list[5].x < lm_list[0].x:
                print("LEFT👈 gesture detected")
                cv2.putText(frame, "LEFT", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** RIGHT 👉 ***********************
            if lm_list[4].y < lm_list[2].y and \
                    lm_list[8].x > lm_list[6].x and \
                    lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and \
                    lm_list[20].x < lm_list[18].x:
                print("RIGHT👉 gesture detected")
                cv2.putText(frame, "RIGHT", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            # *********************** I LOVE YOU 🤟 ***********************
            # check if the index finger is raised upwards (8.y < 6.y)
            # check if the thumb is extended (4.x > 3.x)
            # check if the pinky finger is raised upwards (20.y < 19.y)
            # check if middle and ring fingers are folded
            if lm_list[8].y < lm_list[6].y < lm_list[5].y and \
                    lm_list[12].y > lm_list[11].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[15].y > lm_list[14].y and \
                    lm_list[20].y < lm_list[19].y < lm_list[18].y and \
                    lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x:
                print("I love you🤟 gesture detected")
                cv2.putText(frame, "I love you", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                # draw hand landmarks on the frame with red dots and green lines
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
