# Mouse Control with Hand Gestures

This Python program uses OpenCV, MediaPipe, and PyAutoGUI to control the mouse cursor with hand gestures detected from the webcam.

## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage](#usage)

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- Mediapipe (`pip install mediapipe`)
- PyAutoGUI (`pip install pyautogui`)

## Features

- Detects hand landmarks using MediaPipe.
- Draws landmarks and connections on the hand.
- Controls the mouse cursor:
  - Clicks on single and double finger pinch.
  - Moves the cursor smoothly.
  - Handles click and hold for drag functionality.

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dexxeth/Mouse-Control-with-Hand-Gestures.git
   cd Mouse-Control-with-Hand-Gestures
   
2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
