Copyright © 2025 webdevpathiraja
All rights reserved. This project is licensed under the MIT License.

# 🫲🏼👌🏼Real-Time Hand Tracking with MediaPipe 🤚🏼👋🏼

This project uses **MediaPipe** and **OpenCV** to track hands in real-time using a webcam. It detects hand landmarks and draws them on the frame, displaying the tracking in a live video window. The hand landmarks are displayed as red dots, and the connections between the landmarks are drawn with green lines.

## Prerequisites

To run this project, make sure you have the following Python libraries installed:

- `opencv-python` (for webcam capture and image processing)
- `mediapipe` (for hand tracking)

You can install these libraries using `pip`:

```bash
pip install opencv-python mediapipe
```

## How to Run the Project 🦾🔥

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/webdevpathiraja/AI-Hand-Tracking-on-CPU-in-Real-Time.git
    cd AI-Hand-Tracking-on-CPU-in-Real-Time
    ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python main.py
    ```

    This will open a webcam window showing the tracked hand landmarks. The landmarks will be drawn as red dots, and green lines will represent the connections between the landmarks.

4. Press `q` to exit the program.

## How It Works 👷🏻‍♀️🪜

- **MediaPipe Hands** is used to detect the hand landmarks and their connections in real-time. Each hand's landmarks are stored in a list of 21 points, each with 3D coordinates (x, y, z).
- The script starts by opening the webcam feed using OpenCV. It then processes each frame to detect hands.
- Once hands are detected, the landmarks and connections are drawn on the frame using OpenCV.
- The frame is displayed in a window, and you can press `q` to exit the application.

## Landmarks Information ⭕️❎

Each hand has 21 landmarks, numbered from 0 to 20. Here are the main landmarks:

- 0: Wrist
- 1-4: Thumb (with points for the thumb base, tip, etc.)
- 5-8: Index finger (base to tip)
- 9-12: Middle finger (base to tip)
- 13-16: Ring finger (base to tip)
- 17-20: Little finger (base to tip)

These landmarks are used to draw connections between each joint in the hand.
