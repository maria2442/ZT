import cv2
import mediapipe as mp
import pyautogui
import time

tic = time.perf_counter()
tic1 = time.perf_counter()
tic2 = time.perf_counter()
tok2 = 20
ch = 0
activ = False
ys = 0

def command(k,x,y):
    if k==1:
        pyautogui.click(x=x, y=y, clicks=1, button='left')
    if k==2:
        pyautogui.click(x=x, y=y, clicks=1, button='right')
    if k==3:
        pyautogui.typewrite(['prntscrn'])

def f(s,us1,us2,us3):
    global tic, tik1, ys, ch, tok2, activ
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
            x1[count] = r
            t = s.find("y: ")
            s = s[t + 3:]
            y = s.find("\n")
            r = float(s[0:y])
            y1[count] = r
            t = s.find("z: ")
            s = s[t + 3:]
            y = s.find("\n")
            r = float(s[0:y])
            t = s.find("x: ")
            z1[count] = r
            count += 1
    count -= 1
    if tic2 - tok2 >= 10:
        activ = False

    if (count > 5):
        yk = False
        for m in (x1, y1):
            if (m[11] > m[9] and m[15] > m[13] and m[19] > m[17] and m[7] > m[8] and m[8] < m[5]):
                yk = True
            if (m[11] < m[9] and m[15] < m[13] and m[19] < m[17] and m[7] < m[8] and m[5] < m[8]):
                yk = True
        if (y1[8] < y1[7] and y1[7] < y1[5] and x1[17] > x1[7] and y1[12] < y1[9] and y1[16] < x1[13]):
            ch = ch + 1
        else:
            ch = 0
        if ch >= 50:
            activ = True
        tok2 = time.perf_counter()
        size_x = pyautogui.size()[0]
        size_y = pyautogui.size()[1]
        y1[8] = round(y1[8], 2)
        if activ == True:
            tok = time.perf_counter()
            tok1 = time.perf_counter()
            if ys - y1[8] / tok1 - tic1 < 1:
                pyautogui.moveTo(size_x * x1[8], size_y * y1[8])
            ys = y1[8]
            if (y1[8] > 0.2 and y1[8] < 0.3):
                pyautogui.typewrite(['up'])
            if (y1[8] > 0.8) and (y1[8] < 0.9):
                pyautogui.typewrite(['down'])
            if (y1[8] < 0.2) and (y1[8] > 0.1):
                pyautogui.typewrite(['up', 'up', 'up'])
            if (y1[8] > 0.9):
                pyautogui.typewrite(['down', 'down', 'down'])
            if tok - tic > 1:
                if (y1[11] < y1[16] and y1[11] < y1[20] and y1[7] < y1[16] and y1[7] < y1[20] and abs(
                        x1[7] - x1[11]) <= 0.05 and y1[8] < y1[5] and y1[12] < y1[9]):
                    command(us1,size_x * x1[8],size_y * y1[8])
                tic = time.perf_counter()
                if (x1[8] < 0.1):
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                if (x1[8] > 0.9):
                    pyautogui.hotkey('ctrl', 'tab')
                if (x1[12] - x1[0] < 0 and abs(x1[12] - x1[0]) > abs(y1[12] - y1[0])):
                    # i = i + 1
                    command(us2,size_x * x1[8],size_y * y1[8])
                if (x1[8] > x1[17] and y1[8] < y1[17] and yk == True):
                    command(us3,size_x * x1[8],size_y * y1[8])

def hand(us1,us2,us3):
    print(us1,us2,us3)
    mp_drawing1 = mp.solutions.drawing_utils
    mp_pose1 = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(0)
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
                    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            s = str(hand_landmarks)
                            f(s,us1,us2,us3)


import webbrowser
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow,QComboBox, QVBoxLayout, QPushButton,QMainWindow, QApplication, QWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(400, 300))
        button = QPushButton("Инструкция")
        button1 = QPushButton("Начать")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button1.setCheckable(True)
        button1.clicked.connect(self.the_button_was_clicked1)
        combobox1 = QComboBox()
        combobox1.addItems(['','1.One', '1.Two', '1.Three', '1.Four'])
        combobox1.activated.connect(self.activated1)
        combobox1.currentTextChanged.connect(self.text_changed)
        combobox1.currentIndexChanged.connect(self.index_changed)

        combobox2 = QComboBox()
        combobox2.addItems(['','2.One', '2.Two', '2.Three', '2.Four'])
        combobox2.activated.connect(self.activated2)
        combobox2.currentTextChanged.connect(self.text_changed)
        combobox2.currentIndexChanged.connect(self.index_changed)

        combobox3 = QComboBox()
        combobox3.addItems(['','3.One', '3.Two', '3.Three', '3.Four'])
        combobox3.activated.connect(self.activated3)
        combobox3.currentTextChanged.connect(self.text_changed)
        combobox3.currentIndexChanged.connect(self.index_changed)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(button1)
        layout.addWidget(combobox1)
        layout.addWidget(combobox2)
        layout.addWidget(combobox3)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def activated1(Self, index):
        global us1, us2, us3
        print("Activated index:", index)
        us1=index

    def activated2(Self, index):
        global us1, us2, us3
        print("Activated index:", index)
        us2 = index
    def activated3(Self, index):
        print("Activated index:", index)
        global us1, us2, us3
        us3=index

    def text_changed(self, s):
        print("Text changed:", s)

    def index_changed(self, index):
        print("Index changed", index)

    def the_button_was_clicked(self):
        print("Clicked!")
        webbrowser.open("https://zayez261.wixsite.com/zhest")

    def the_button_was_clicked1(self):
        global us1,us2,us3
        print("Clicked1!")
        print(us1,us2,us3)
        hand(us1,us2,us3)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

