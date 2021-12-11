import cv2
import mediapipe as mp
import pyautogui
i=0
def f(s, a=0,):
    pos = 0
    x_sum = 0.0
    y_sum = 0.0
    z_sum = 0.0
    global i
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
        size_x=pyautogui.size()[0]
        size_y = pyautogui.size()[1]
        if (y1[11] < y1[16] and y1[11] < y1[20] and y1[7] < y1[16] and y1[7] < y1[20]and abs(x1[7] - x1[11])<=0.05 and y1[8]<y1[5]and y1[12]<y1[9]):
            #print(i)
            i=i+1
            pyautogui.click(x=size_x*x1[8], y=size_y*y1[8], clicks=1, button='left')

        pyautogui.moveTo(size_x*x1[8], size_y*y1[8])
        yk = False
        delta = abs(x1[0] - x1[8]) + abs(y1[0] - y1[8]) + abs(z1[0] - z1[8]) + abs(x1[0] - x1[12]) + abs(
            y1[0] - y1[12]) + abs(z1[0] - z1[12]) + abs(x1[0] - x1[16]) + abs(y1[0] - y1[16]) + abs(z1[0] - z1[16])
        std = abs(x1[0] - x1[5]) + abs(y1[0] - y1[5]) + abs(z1[0] - z1[5])

        for m in (x1, y1):
            if (m[11] > m[9] and m[15] > m[13] and m[19] > m[17] and m[7] > m[8] and m[8] < m[5]):
                yk = True
            if (m[11] < m[9] and m[15] < m[13] and m[19] < m[17] and m[7] < m[8] and m[5] < m[8]):
                yk = True
        if (delta < 4.5 * std):
            pos = 1
        if (y1[11] < y1[16] and y1[11] < y1[20] and y1[7] < y1[16] and y1[7] < y1[20] and abs(
                x1[7] - x1[11]) <= 0.05 and y1[8] < y1[5]):
            pos = 4
        if (x1[12] - x1[0] > 0 and x1[12] - x1[0] > abs(y1[12] - y1[0])):
            pos = 2
        if (x1[12] - x1[0] < 0 and abs(x1[12] - x1[0]) > abs(y1[12] - y1[0])):
            pos = 3
        if (yk == True):
            if (y1[6] < y1[17]):
                pos = 7

            if (y1[8] > y1[5]):
                pos = 8
            if (x1[6] < x1[2] and y1[6] > y1[17]):
                pos = 5
            if (x1[8] > x1[17] and y1[8] < y1[17]):
                pos = 6
        print(y1[8])
        if (y1[8] < 0.2):
            pyautogui.typewrite(['up'])
        if (y1[8] > 0.6):
            pyautogui.typewrite(['down'])

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
                        if (timer >= 0):
                            if pos == 2:
                                zn += 0.003
                            elif pos == 3:
                                zn -= 0.003
                            if zn >= 1:
                                zn = 1
                            elif zn < 0:
                                zn = 0
                        if pos == 1:
                            if timer >= 0:
                                timer += 1
                            else:
                                x_a[timer] = x
                                y_a[timer] = y
                                z_a[timer] = z
                                timer += 1

                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                image = cv2.resize(image, (1200, 850), cv2.INTER_NEAREST)
                if results.multi_hand_landmarks:
                    color_yellow = (0, 0, 0)
                    s = "X(left-right): " + str(x)
                    s1 = "Y(down-up): " + str(y)
                    s2 = "Z(back-front): " + str(zn)
                    if pos == 0:
                        s3 = "unclenching"
                    elif pos == 1:
                        s3 = "clenching"
                    elif pos == 2:
                        if st == 'r':
                            s3 = "Front"
                        if st == 'l':
                            s3 = "Back"
                    elif pos == 3:
                        if st == 'r':
                            s3 = "Back"
                        if st == 'l':
                            s3 = "Front"
                    elif pos == 4:
                        s3 = "Click"
                    elif pos == 5:
                        s3 = "run LEFT"
                    elif pos == 6:
                        s3 = "run RIGHT"
                    elif pos == 7:
                        s3 = "run UP"
                    elif pos == 8:
                        s3 = "run DOWN"
                    cv2.putText(image, s3, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
                cv2.imshow('Image', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
cap.release()
