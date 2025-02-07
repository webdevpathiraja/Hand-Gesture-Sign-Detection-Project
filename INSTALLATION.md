# ⭕ Installation Guide for Hand Sign Detection Project 🔥

## Prerequisites
To run this project, make sure you have the following Python libraries installed:

- `opencv-python` (for webcam capture and image processing)
- `mediapipe` (for hand tracking)

You can install these libraries using pip:

```bash
pip install opencv-python mediapipe
```

## 🚀 How to Run the Project 
1. Fork this repository to your GitHub account.
2. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/AI-Hand-Tracking-on-CPU-in-Real-Time.git
cd AI-Hand-Tracking-on-CPU-in-Real-Time
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

4. Run the script:

```bash
python main.py
```

This will open a webcam window showing the tracked hand landmarks. The landmarks will be drawn as red dots, and green lines will represent the connections between the landmarks.

Press **q** to exit the program.

## 👷🏻‍♀️ How It Works 🪜
The detailed explanation of the logic and how the hand sign detection is implemented can be found in the [README file](README.md).

In this final phase of the project, hand gesture detection is integrated alongside hand landmark tracking. The system not only detects hand landmarks but also identifies specific hand gestures based on the positioning of the fingers.

⭕ Hand Landmark Tracking:

MediaPipe Hands is used to detect the hand landmarks and their connections in real-time. Each hand's landmarks are stored in a list of 21 points, each with 3D coordinates (x, y, z).
The script processes each video frame to detect hand landmarks using MediaPipe.

👉🏻 Gesture Recognition:

The project recognizes several hand gestures by analyzing the relative positions of the hand landmarks.

🤚🏽 Gesture Detection Logic:

The detailed explanation of the logic and how the hand sign detection is implemented can be found in the [README file](README.md).

## Project Features 👩🏽‍🍳
Real-time hand gesture recognition.

Multiple hand gestures (e.g., LIKE, DISLIKE, OK, PEACE, etc.).

Hand landmarks are drawn with red dots, and connections are shown with green lines.

