import cv2
import mediapipe as mp
import pyautogui
i=0
import time
tic=time.perf_counter()
tic1=time.perf_counter()
ys=0

def f(s, a=0,):
    pos = 0
    x_sum = 0.0
    y_sum = 0.0
    z_sum = 0.0
    global i,tic,tic1,ys
    # print(s)
    x1 = [0.0 for i in range(40)]
    y1 = [0.0 for i in range(40)]
    z1 = [0.0 for i in range(40)]
    t = s.find("x: ")
    count = 0
    while (t != -1):
        if (t):
            s = s[t + 3:]
            y = s.find("\n")
            r = float(s[0:y])
            x_sum += r
            # print(r)
            x1[count] = r

            t = s.find("y: ")
            s = s[t + 3:]
            y = s.find("\n")
            r = float(s[0:y])
            y_sum += (1 - abs(r))
            # print(r)
            y1[count] = r

            t = s.find("z: ")
            s = s[t + 3:]
            y = s.find("\n")
            r = float(s[0:y])
            z_sum += abs(r)
            # print(r)
            t = s.find("x: ")
            z1[count] = r
            count += 1
    count -= 1

    if (count == 20):
        size_x = pyautogui.size()[0]
        size_y = pyautogui.size()[1]

        print(y1[8])
        y1[8] = round(y1[8], 2)
        print(y1[8])

        tok = time.perf_counter()
        tok1 = time.perf_counter()
        if ys - y1[8] / tok1 - tic1 < 1:
            pyautogui.moveTo(size_x * x1[8], size_y * y1[8])
        ys = y1[8]
        if (y1[8] < 0.2):
            pyautogui.typewrite(['up'])
        if (y1[8] > 0.6):
            pyautogui.typewrite(['down'])
        if (y1[8] < 0.1):
            pyautogui.typewrite(['up', 'up', 'up'])
        if (y1[8] > 0.9):
            pyautogui.typewrite(['down', 'down', 'down'])
        if tok - tic > 1:
            if (y1[11] < y1[16] and y1[11] < y1[20] and y1[7] < y1[16] and y1[7] < y1[20] and abs(
                    x1[7] - x1[11]) <= 0.05 and y1[8] < y1[5] and y1[12] < y1[9]):
                pyautogui.click(x=size_x * x1[8], y=size_y * y1[8], clicks=1, button='left')
            tic = time.perf_counter()
            if (x1[8] < 0.1):
                pyautogui.hotkey('ctrl', 'shift', 'tab')
            if (x1[8] > 0.9):
                pyautogui.hotkey('ctrl', 'tab')
            if (x1[12] - x1[0] < 0 and abs(x1[12] - x1[0]) > abs(y1[12] - y1[0])):
                # i = i + 1
                pyautogui.click(x=size_x * x1[8], y=size_y * y1[8], clicks=1, button='right')
            if (x1[8] > x1[17] and y1[8] < y1[17]):
                pyautogui.typewrite(['prntscrn'])

    if a == 1:
        return x1[0], 1 - abs(y1[0]), abs(z1[16]), pos
    return x1[0], 1 - abs(y1[0]), abs(z1[17]), pos  # 17 точка для оси z наиболе точная


mp_drawing1 = mp.solutions.drawing_utils
mp_pose1 = mp.solutions.pose

size = 200
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

x_a = [0.0 for i in range(size)]
y_a = [0.0 for i in range(size)]
z_a = [0.0 for i in range(size)]
a=0
timer = 0
# For webcam input:
cap = cv2.VideoCapture(0)

zn = 0.5
for i in range(1):

    with mp_pose1.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        with mp_hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image1 = image
                image.flags.writeable = False
                results = hands.process(image)
                res = str(results.multi_handedness)
                if "Left" in res:
                    st = 'l'
                if "Right" in res:
                    st = 'r'
                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        s = str(hand_landmarks)
                        #print(s)
                        x, y, z, pos = f(s)
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                image = cv2.resize(image, (1200, 850), cv2.INTER_NEAREST)
                if results.multi_hand_landmarks:
                    color_yellow = (0, 0, 0)
                cv2.imshow('Image', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
cap.release()
