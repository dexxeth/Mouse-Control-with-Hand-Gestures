# Virtual Mouse Control with Hand Gestures

This Python script uses OpenCV, MediaPipe, and PyAutoGUI to control the mouse cursor with hand gestures detected from the webcam.

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
   git clone https://github.com/yourusername/virtual-mouse-control.git
   cd virtual-mouse-control
   
2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Run the code:**

   ```bash
   python virtual_mouse.py
   
4. **To quit the program, press q on the keyboard.**
