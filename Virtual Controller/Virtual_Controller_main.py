import tkinter as tk
import cv2
import mediapipe as mp
import pyautogui
import subprocess
import time

# ---------------- Button 1: Volume Control ---------------- #
def button1_click():
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
            multi_hand_landmarks = out.multi_hand_landmarks

            if multi_hand_landmarks:
                for hand in multi_hand_landmarks:
                    draw.draw_landmarks(img, hand)
                    lm = hand.landmark
                    x1 = y1 = x2 = y2 = 0
                    for id, l in enumerate(lm):
                        x, y = int(l.x * w), int(l.y * h)
                        if id == 8:
                            x1, y1 = x, y
                            cv2.circle(img, (x, y), 8, (0, 255, 255), 3)
                        if id == 4:
                            x2, y2 = x, y
                            cv2.circle(img, (x, y), 8, (0, 0, 255), 3)

                    distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    if distance > 50:
                        pyautogui.press("volumeup")
                    else:
                        pyautogui.press("volumedown")
            
            cv2.imshow("Volume Control", img)
            if cv2.waitKey(1) & 0xFF == 27: 
                break

    finally:
        webcam.release()
        cv2.destroyAllWindows()

# ---------------- Button 2: Brigtness Control ---------------- #
def button2_click():
    print('Brightness Control Activated')
    webcam = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands()
    draw = mp.solutions.drawing_utils
    last_brightness = -1
    last_update_time = time.time()

    try:
        while True:
            ret, img = webcam.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            h, w, _ = img.shape
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            out = hands.process(rgb)
            multi_hand_landmarks = out.multi_hand_landmarks

            if multi_hand_landmarks:
                for hand in multi_hand_landmarks:
                    draw.draw_landmarks(img, hand)
                    lm = hand.landmark
                    x1 = y1 = x2 = y2 = 0
                    for id, l in enumerate(lm):
                        x, y = int(l.x * w), int(l.y * h)
                        if id == 8:
                            x1, y1 = x, y
                        if id == 4:
                            x2, y2 = x, y

                    distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
                    brightness = int(min(max((distance - 20) * 2, 0), 100))

                    if brightness != last_brightness and time.time() - last_update_time > 1:
                        subprocess.Popen(
                            ['powershell', f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})'],
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        last_brightness = brightness
                        last_update_time = time.time()

                    cv2.putText(img, f'Brightness: {brightness}%', (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    cv2.circle(img, (x1, y1), 8, (0, 255, 0), -1)
                    cv2.circle(img, (x2, y2), 8, (0, 0, 255), -1)

            cv2.imshow("Brightness Control", img)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        webcam.release()
        cv2.destroyAllWindows()

# ---------------- Button 3: Virtual Mouse ---------------- #
def button3_click():
    print('Virtual Mouse with Click, Scroll, and Drag Activated')
    cap = cv2.VideoCapture(0)
    detector = mp.solutions.hands.Hands()
    draw = mp.solutions.drawing_utils
    screen_w, screen_h = pyautogui.size()
    clicking = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = detector.process(rgb)
            hands = result.multi_hand_landmarks

            if hands:
                for hand in hands:
                    draw.draw_landmarks(frame, hand)
                    lm = hand.landmark
                    index_x = index_y = thumb_y = 0
                    middle_finger_up = False
                    ring_finger_up = False
                    pinky_up = False

                    x_index = int(lm[8].x * w)
                    y_index = int(lm[8].y * h)
                    x_thumb = int(lm[4].x * w)
                    y_thumb = int(lm[4].y * h)
                    x_middle = int(lm[12].x * w)
                    y_middle = int(lm[12].y * h)
                    x_ring = int(lm[16].x * w)
                    y_ring = int(lm[16].y * h)
                    x_pinky = int(lm[20].x * w)
                    y_pinky = int(lm[20].y * h)

                    # Move mouse with index
                    screen_x = screen_w / w * x_index
                    screen_y = screen_h / h * y_index
                    pyautogui.moveTo(screen_x, screen_y)

                    # Calculate distances
                    dist_thumb_index = ((x_thumb - x_index)**2 + (y_thumb - y_index)**2) ** 0.5
                    dist_index_middle = ((x_index - x_middle)**2 + (y_index - y_middle)**2) ** 0.5
                    dist_middle_ring = ((x_middle - x_ring)**2 + (y_middle - y_ring)**2) ** 0.5
                    dist_pinky_index = ((x_pinky - x_index)**2 + (y_pinky - y_index)**2) ** 0.5

                    # Gesture: Left Click (Index + Thumb close)
                    if dist_thumb_index < 40:
                        pyautogui.click()
                        time.sleep(0.3)

                    # Gesture: Right Click (Index + Middle + Thumb close)
                    if dist_thumb_index < 40 and dist_index_middle < 40:
                        pyautogui.rightClick()
                        time.sleep(0.3)

                    # Gesture: Drag (Ring finger close to index)
                    if dist_middle_ring < 30:
                        if not clicking:
                            pyautogui.mouseDown()
                            clicking = True
                    else:
                        if clicking:
                            pyautogui.mouseUp()
                            clicking = False

                    # Gesture: Scroll (Index vs Pinky vertical diff)
                    if dist_pinky_index < 60:
                        if y_index < y_pinky:
                            pyautogui.scroll(30)
                        else:
                            pyautogui.scroll(-30)

            cv2.imshow("Virtual Mouse", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

# ---------------- Button 4: Eye Mouse ---------------- #
def button4_click():
    print("Eye-Controlled Mouse Activated")
    cam = cv2.VideoCapture(0)
    mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = mesh.process(rgb)
            points = result.multi_face_landmarks
            h, w, _ = frame.shape

            if points:
                lm = points[0].landmark
                for id, pt in enumerate(lm[474:478]):
                    x = int(pt.x * w)
                    y = int(pt.y * h)
                    if id == 1:
                        pyautogui.moveTo(screen_w / w * x, screen_h / h * y)
                if (lm[145].y - lm[159].y) < 0.008:
                    pyautogui.click()
                    pyautogui.sleep(1)

            cv2.imshow("Eye Mouse", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cam.release()
        cv2.destroyAllWindows()

# ---------------- Button 5: Open Notepad + Virtual Keyboard ---------------- #
def button5_click():
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

            draw_keyboard(frame)

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

                index_finger = hand_landmarks.landmark[8]
                x = int(index_finger.x * 1280)
                y = int(index_finger.y * 720)
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

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

            cv2.imshow("Notepad + Virtual Keyboard", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# ---------------- Button 6: Open Paint + Virtual Drawing ---------------- #
def button6_click():
    print("Open Palm to Launch Paint & Draw in Paint")
    cap = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
    draw_utils = mp.solutions.drawing_utils
    paint_opened = False
    drawing = False
    click_down = False
    screen_w, screen_h = pyautogui.size()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            draw_utils.draw_landmarks(frame, hand_landmarks)

            index_finger = hand_landmarks.landmark[8]
            thumb_finger = hand_landmarks.landmark[4]

            index_x = int(index_finger.x * screen_w)
            index_y = int(index_finger.y * screen_h)
            thumb_x = int(thumb_finger.x * screen_w)
            thumb_y = int(thumb_finger.y * screen_h)

            pyautogui.moveTo(index_x, index_y)

            distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2)**0.5
            if distance < 40:
                if not click_down:
                    pyautogui.mouseDown()
                    click_down = True
            else:
                if click_down:
                    pyautogui.mouseUp()
                    click_down = False

            if not paint_opened:
                tip_ids = [4, 8, 12, 16, 20]
                fingers_up = 0
                for tip_id in tip_ids:
                    if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                        fingers_up += 1

                if fingers_up == 5:
                    print("Open Palm Detected - Opening Paint")
                    subprocess.Popen(['mspaint'])
                    time.sleep(2)
                    paint_opened = True

        cv2.imshow("Paint Drawing Mode", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    pyautogui.mouseUp()

# ---------------- GUI Layout Display(Main)---------------- #
window = tk.Tk()
window.title("Gesture Control Hub")
window.geometry("500x500")

tk.Button(window, text="1 Volume Control", command=button1_click).pack(pady=5)
tk.Button(window, text="2 Brightness Control", command=button2_click).pack(pady=5)
tk.Button(window, text="3 Virtual Mouse", command=button3_click).pack(pady=5)
tk.Button(window, text="4 Eye Mouse", command=button4_click).pack(pady=5)
tk.Button(window, text="5 Open Notepad", command=button5_click).pack(pady=5)
tk.Button(window, text="6 Air Drawing Canvas", command=button6_click).pack(pady=5)

window.mainloop()
