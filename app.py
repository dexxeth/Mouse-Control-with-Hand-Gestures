import streamlit as st
from gesture_mouse import GestureMouse
import time

st.set_page_config(page_title="Gesture Mouse", layout="centered")

st.title("🖱️ Finger Gesture Mouse Control")
st.markdown("Control your mouse using hand gestures. Built with OpenCV, Mediapipe, and PyAutoGUI.")

# Sidebar gesture settings
st.sidebar.header("🛠️ Settings")
smoothing = st.sidebar.slider("🧊 Smoothing Factor", 0.0, 1.0, 0.8, 0.05)
click_threshold = st.sidebar.slider("⏱️ Double Click Threshold (s)", 0.1, 1.0, 0.3, 0.05)
click_distance = st.sidebar.slider("👆 Click Gesture Distance (px)", 20, 100, 45, 5)

# Main screen toggle button
st.markdown("---")
toggle = st.toggle("🚀 Start / Stop Gesture Mouse Control", key="gesture_toggle_main")

# Camera feed and FPS counter
frame_window = st.empty()
fps_placeholder = st.empty()

# Run gesture tracking loop
if toggle:
    gesture_mouse = GestureMouse(
        smoothing=smoothing,
        double_click_threshold=click_threshold,
        click_distance=click_distance
    )

    prev_time = time.time()

    while st.session_state.gesture_toggle_main:
        frame = gesture_mouse.get_frame()
        if frame is not None:
            # Calculate and display FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            fps_placeholder.markdown(f"**🔁 FPS:** `{fps:.2f}`")

            # Show webcam feed
            frame_window.image(frame)
        else:
            st.error("❌ Failed to read from webcam.")
            break

        # Small delay to keep UI responsive
        time.sleep(0.01)

    gesture_mouse.release()
    fps_placeholder.markdown("🛑 Gesture control stopped.")
    st.success("🛑 Gesture tracking stopped.")
