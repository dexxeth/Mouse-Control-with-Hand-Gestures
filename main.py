import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
hand_detect = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

prev_x, prev_y = screen_width // 2, screen_height // 2

last_click_time = 0
double_click_threshold = 0.3

def smooth_move(x, y, prev_x, prev_y, smoothing=0.8):
    new_x = prev_x + (x - prev_x) * smoothing
    new_y = prev_y + (y - prev_y) * smoothing
    return new_x, new_y

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detect.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(
                frame,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS,
                drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
            landmarks = hand.landmark
            index_x, index_y = 0, 0
            thumb_x, thumb_y = 0, 0

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=12, color=(0, 255, 255), thickness=-1)
                    index_x = int(screen_width * landmark.x)
                    index_y = int(screen_height * landmark.y)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=12, color=(0, 255, 255), thickness=-1)
                    thumb_x = int(screen_width * landmark.x)
                    thumb_y = int(screen_height * landmark.y)

            if index_x and thumb_x:
                distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

                if distance < 45:
                    current_time = time.time()
                    if current_time - last_click_time < double_click_threshold:
                        pyautogui.doubleClick()
                        pyautogui.sleep(0.1)
                    else:
                        pyautogui.click()
                    last_click_time = current_time
                else:
                    new_x, new_y = smooth_move(index_x, index_y, prev_x, prev_y)
                    pyautogui.moveTo(new_x, new_y)
                    prev_x, prev_y = new_x, new_y

    cv2.imshow("Mouse Control with Hand Gestures", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
