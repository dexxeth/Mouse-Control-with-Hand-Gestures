
# 🖱️ Mouse Control with Hand Gestures

A Python-based gesture control system using **OpenCV**, **MediaPipe**, **PyAutoGUI**, and a **Streamlit UI** control the mouse cursor with hand gestures detected from the webcam.

---

## Table of Contents

- [Requirements](#requirements)
- [Features](#features)
- [Usage (CLI & UI)](#usage)
- [Controls](#controls)
- [Demo](#demo)
- [Credits](#credits)

---

## Requirements

Install the following Python packages:

```bash
pip install -r requirements.txt
```

Required packages:

- `opencv-python`
- `mediapipe`
- `pyautogui`
- `streamlit`

---

## Features

- Real-time finger gesture tracking  
- Smooth mouse movement with movement buffer  
- Deadzone filtering to reduce jitter  
- Single & Double Click via finger pinch  
- Hand Stability Filter to avoid false triggers  
- Visual feedback on-screen when clicking  
- Streamlit UI with:
    - Toggle to start/stop tracking
    - FPS Counter
    - Webcam feed display
    - Adjustable smoothing, click sensitivity, etc.

---

## Usage

1. **Clone the repository:**

```bash
git clone https://github.com/dexxeth/Mouse-Control-with-Hand-Gestures.git
cd Mouse-Control-with-Hand-Gestures
```
2. **Run via Streamlit:**

```bash
streamlit run app.py
```

Then open in your browser and use the toggle to start gesture mouse control.

---

## Controls

| Gesture                | Action        |
|------------------------|---------------|
| Pinch (thumb + index)  | Single click  |
| Quick double pinch     | Double click  |
| Move index finger      | Move mouse    |

---