import cv2
import mediapipe as mp
import pyautogui
import time
import math
import subprocess
import tkinter as tk
from tkinter import ttk
import numpy as np

# ---------------- Volume Controller ----------------
def volume_controller():
    print('Volume Control Activated')
    webcam = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands()
    draw = mp.solutions.drawing_utils

    try:
        while True:
            ret, img = webcam.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            h, w, _ = img.shape
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            out = hands.process(rgb)

            if out.multi_hand_landmarks:
                for hand in out.multi_hand_landmarks:
                    draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
                    lm = hand.landmark
                    x1 = y1 = x2 = y2 = 0
                    for id, l in enumerate(lm):
                        x, y = int(l.x * w), int(l.y * h)
                        if id == 8:  # Index tip
                            x1, y1 = x, y
                            cv2.circle(img, (x, y), 8, (0, 255, 255), 3)  # Yellow
                        if id == 4:  # Thumb tip
                            x2, y2 = x, y
                            cv2.circle(img, (x, y), 8, (0, 0, 255), 3)  # Red

                    distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green line

                    if distance > 80:
                        cv2.putText(img, 'VOLUME UP', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        pyautogui.press("volumeup")
                        time.sleep(0.1)
                    else:
                        cv2.putText(img, 'VOLUME DOWN', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                        pyautogui.press("volumedown")
                        time.sleep(0.1)

            cv2.putText(img, 'Press ESC to exit', (10, h-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Volume Control", img)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        webcam.release()
        cv2.destroyAllWindows()


# ---------------- Virtual Mouse ----------------
def virtual_mouse():
    print('Virtual Mouse Activated')
    webcam = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
    draw = mp.solutions.drawing_utils
    screen_w, screen_h = pyautogui.size()
    last_action_time, gesture_delay = 0, 1.5
    dragging = False

    try:
        while True:
            ret, img = webcam.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            h, w, _ = img.shape
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            out = hands.process(rgb)

            if out.multi_hand_landmarks:
                for hand in out.multi_hand_landmarks:
                    draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
                    lm = [(int(p.x * w), int(p.y * h)) for p in hand.landmark]

                    thumb, index, middle, ring, pinky = lm[4], lm[8], lm[12], lm[16], lm[20]
                    thumb_pip, index_pip, middle_pip, ring_pip, pinky_pip = lm[3], lm[6], lm[10], lm[14], lm[18]

                    index_up, middle_up = index[1] < index_pip[1], middle[1] < middle_pip[1]
                    ring_up, pinky_up = ring[1] < ring_pip[1], pinky[1] < pinky_pip[1]
                    thumb_up, thumb_down = thumb[1] < thumb_pip[1], thumb[1] > thumb_pip[1] + 20

                    # Move mouse
                    if index_up:
                        pyautogui.moveTo(int((index[0]/w)*screen_w), int((index[1]/h)*screen_h))

                    current_time = time.time()
                    if current_time - last_action_time > gesture_delay:
                        if index_up and middle_up and not ring_up and not pinky_up and not thumb_up:
                            pyautogui.click()
                            cv2.putText(img, 'LEFT CLICK', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            last_action_time = current_time
                        elif index_up and middle_up and ring_up and not pinky_up and not thumb_up:
                            pyautogui.rightClick()
                            cv2.putText(img, 'RIGHT CLICK', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            last_action_time = current_time
                        elif thumb_up and not any([index_up, middle_up, ring_up, pinky_up]):
                            pyautogui.scroll(3)
                            cv2.putText(img, 'SCROLL UP', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                            last_action_time = current_time
                        elif thumb_down and not any([index_up, middle_up, ring_up, pinky_up]):
                            pyautogui.scroll(-3)
                            cv2.putText(img, 'SCROLL DOWN', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                            last_action_time = current_time

                    # Dragging
                    if math.hypot(thumb[0]-index[0], thumb[1]-index[1]) < 30:
                        cv2.line(img, thumb, index, (0, 255, 255), 3)
                        if not dragging:
                            pyautogui.mouseDown()
                            cv2.putText(img, 'DRAG START', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            dragging = True
                    else:
                        if dragging:
                            pyautogui.mouseUp()
                            cv2.putText(img, 'DRAG END', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            dragging = False

                    # ---- Draw fingertip colors ----
                    cv2.circle(img, thumb, 8, (255, 0, 0), -1)   
                    cv2.circle(img, index, 8, (0, 0, 255), -1)   
                    cv2.circle(img, middle, 8, (0, 255, 0), -1)  
                    cv2.circle(img, ring, 8, (255, 255, 0), -1)  
                    cv2.circle(img, pinky, 8, (255, 0, 255), -1) 
            
            cv2.putText(img, 'Press ESC to exit', (10, h-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Virtual Mouse", img)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        if dragging: pyautogui.mouseUp()
        webcam.release()
        cv2.destroyAllWindows()


# ---------------- Virtual Keyboard ----------------
def virtual_keyboard():
    print("Open Palm Gesture for Notepad + Virtual Keyboard Activated")
    cap = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
    draw_utils = mp.solutions.drawing_utils
    screen_w, screen_h = pyautogui.size()
    notepad_opened = False
    caps_lock = False

    keys = list("QWERTYUIOPASDFGHJKLZXCVBNM")
    number_keys = list("1234567890")
    special_keys = ["Space", "Enter", "Caps", "Back"]
    all_keys = number_keys + keys + special_keys
    key_map = {}
    key_height, key_width = 60, 60
    start_x, start_y = 50, 150

    def draw_keyboard(img):
        key_map.clear()
        x, y = start_x, start_y
        for i, key in enumerate(all_keys):
            end_x, end_y = x + key_width, y + key_height
            cv2.rectangle(img, (x, y), (end_x, end_y), (255, 255, 255), -1)
            cv2.putText(img, key, (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            key_map[key] = (x, y, end_x, end_y)
            x += key_width + 10
            if (i + 1) % 10 == 0:
                x = start_x
                y += key_height + 10

    def get_key_pressed(x, y):
        for key, (x1, y1, x2, y2) in key_map.items():
            if x1 < x < x2 and y1 < y < y2:
                return key
        return None

    pressed_key = None
    last_press_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (1280, 720))
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                draw_utils.draw_landmarks(frame, hand_landmarks)

                tip_ids = [8, 12, 16, 20]
                count = 0
                for tip_id in tip_ids:
                    if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                        count += 1
                thumb_open = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x

                if not notepad_opened and count + int(thumb_open) == 5:
                    print("Opening Notepad and Virtual Keyboard...")
                    subprocess.Popen(['notepad.exe'])
                    time.sleep(2)
                    notepad_opened = True

                if notepad_opened:
                    draw_keyboard(frame)

                    index_finger = hand_landmarks.landmark[8]
                    x = int(index_finger.x * 1280)
                    y = int(index_finger.y * 720)
                    cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

                    key_now = get_key_pressed(x, y)

                    if key_now and time.time() - last_press_time > 1:
                        print(f"Key Pressed: {key_now}")
                        if key_now == "Space":
                            pyautogui.press("space")
                        elif key_now == "Enter":
                            pyautogui.press("enter")
                        elif key_now == "Back":
                            pyautogui.press("backspace")
                        elif key_now == "Caps":
                            caps_lock = not caps_lock
                        else:
                            char = key_now.lower() if not caps_lock else key_now.upper()
                            pyautogui.press(char)
                        last_press_time = time.time()

            cv2.putText(frame, 'Press ESC to exit', (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("Notepad + Virtual Keyboard", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print('Virtual Keyboard Deactivated')



# ---------------- GUI ----------------
def main_gui():
    root = tk.Tk()
    root.title("Gesture Control Interface")
    root.geometry("400x300")
    root.configure(bg="#2e2e2e")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14), padding=10)

    ttk.Button(root, text="Volume Control", command=volume_controller).pack(pady=20)
    ttk.Button(root, text="Virtual Mouse", command=virtual_mouse).pack(pady=20)
    ttk.Button(root, text="Virtual Keyboard", command=virtual_keyboard).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
