import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
drawing_utils = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = screen_w // 2, screen_h // 2

def smooth_move(x, y, prev_x, prev_y, smoothing=0.9):
    new_x = int(prev_x + (x - prev_x) * smoothing)
    new_y = int(prev_y + (y - prev_y) * smoothing)
    return new_x, new_y

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = face_mesh.process(rgb_frame)
    if output.multi_face_landmarks:
        for face_landmarks in output.multi_face_landmarks:
            drawing_utils.draw_landmarks(
                frame,
                face_landmarks,
                mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_utils.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                connection_drawing_spec=drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=1)
            )

            left_eye_landmarks = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145]
            left_eye_points = []
            for idx in left_eye_landmarks:
                landmark = face_landmarks.landmark[idx]
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                left_eye_points.append((x, y))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            eye_avg_y = sum([point[1] for point in left_eye_points]) / len(left_eye_points)

            mouse_x = int(left_eye_points[0][0] * screen_w / frame_w)
            mouse_y = int(eye_avg_y * screen_h / frame_h)
            pyautogui.moveTo(mouse_x, mouse_y)

            eye_height = left_eye_points[8][1] - left_eye_points[0][1]
            if eye_height < 10:
                pyautogui.click()

    cv2.imshow('Eye Controlled Mouse', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
