import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque

class GestureMouse:
    def __init__(self, smoothing=0.8, double_click_threshold=0.3, click_distance=45, buffer_size=5, deadzone=3):
        self.smoothing = smoothing
        self.double_click_threshold = double_click_threshold
        self.click_distance = click_distance
        self.deadzone = deadzone

        self.hand_detect = mp.solutions.hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()

        self.prev_x, self.prev_y = self.screen_width // 2, self.screen_height // 2
        self.last_click_time = 0
        self.cap = cv2.VideoCapture(0)
        self.pos_buffer = deque(maxlen=buffer_size)

        # Stability tracking
        self.hand_visible = False
        self.hand_stable_start_time = None
        self.stability_threshold_sec = 0.2  # Must be visible for this duration to be considered stable

        # Feedback text
        self.feedback_text = ""
        self.feedback_time = 0
        self.feedback_duration = 0.5  # seconds

    def smooth_move(self, x, y):
        self.pos_buffer.append((x, y))
        avg_x = sum(p[0] for p in self.pos_buffer) / len(self.pos_buffer)
        avg_y = sum(p[1] for p in self.pos_buffer) / len(self.pos_buffer)
        return avg_x, avg_y

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.hand_detect.process(rgb_frame)
        hands = output.multi_hand_landmarks

        index_x = index_y = thumb_x = thumb_y = 0

        current_time = time.time()

        if hands:
            # Hand is visible now
            if not self.hand_visible:
                self.hand_visible = True
                self.hand_stable_start_time = current_time

            hand_stable = (current_time - self.hand_stable_start_time) > self.stability_threshold_sec

            for hand in hands:
                self.drawing_utils.draw_landmarks(
                    frame,
                    hand,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )
                landmarks = hand.landmark

                for id, lm in enumerate(landmarks):
                    x = int(lm.x * frame_width)
                    y = int(lm.y * frame_height)

                    if id == 8:
                        index_x = int(self.screen_width * lm.x)
                        index_y = int(self.screen_height * lm.y)
                        cv2.circle(frame, (x, y), 10, (255, 255, 0), -1)

                    if id == 4:
                        thumb_x = int(self.screen_width * lm.x)
                        thumb_y = int(self.screen_height * lm.y)
                        cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                if hand_stable and index_x and thumb_x:
                    distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

                    if distance < self.click_distance:
                        if current_time - self.last_click_time < self.double_click_threshold:
                            pyautogui.doubleClick()
                            self.feedback_text = "Double Click"
                        else:
                            pyautogui.click()
                            self.feedback_text = "Click"
                        self.last_click_time = current_time
                        self.feedback_time = current_time
                    else:
                        smoothed_x, smoothed_y = self.smooth_move(index_x, index_y)

                        dx = abs(smoothed_x - self.prev_x)
                        dy = abs(smoothed_y - self.prev_y)

                        if dx > self.deadzone or dy > self.deadzone:
                            pyautogui.moveTo(smoothed_x, smoothed_y)
                            self.prev_x, self.prev_y = smoothed_x, smoothed_y
        else:
            self.hand_visible = False
            self.hand_stable_start_time = None

        # Draw feedback text if active
        if current_time - self.feedback_time < self.feedback_duration:
            cv2.putText(
                frame,
                self.feedback_text,
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 255),
                3
            )

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release(self):
        self.cap.release()
