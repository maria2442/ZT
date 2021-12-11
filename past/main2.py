import cv2
import mediapipe as mp
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def f(s, a=0):
    pos = 0
    x_sum = 0.0
    y_sum = 0.0
    z_sum = 0.0

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
        delta = abs(x1[0] - x1[8]) + abs(y1[0] - y1[8]) + abs(z1[0] - z1[8]) + abs(x1[0] - x1[12]) + abs(
            y1[0] - y1[12]) + abs(z1[0] - z1[12]) + abs(x1[0] - x1[16]) + abs(y1[0] - y1[16]) + abs(z1[0] - z1[16])
        std = abs(x1[0] - x1[5]) + abs(y1[0] - y1[5]) + abs(z1[0] - z1[5])
        if (delta < 4.5 * std):
            pos = 1
        if (y1[11] < y1[16] and y1[11] < y1[20] and y1[7] < y1[16] and y1[7] < y1[20]and abs(x1[7] - x1[11])<=0.05 and y1[8]<y1[5]):
            pos = 4
        if (x1[12] - x1[0] > 0 and x1[12] - x1[0] > abs(y1[12] - y1[0])):
            pos = 2
        if (x1[12] - x1[0] < 0 and abs(x1[12] - x1[0]) > abs(y1[12] - y1[0])):
            pos = 3

        # print(std)
        #print()
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

timer = 0

df=pd.read_excel("Kniga12.xlsx")
#print(df)
#print(list(df.name))
i=0
# For static images:
IMAGE_FILES = ['img1.jpg','img2.jpg','img3.jpg','img4.jpg','img5.jpg','img6.jpg','img7.jpg','img8.jpg','img9.jpg','img10.jpg','img11.jpg','img12.jpg','img13.jpg','img14.jpg','img15.jpg','img16.jpg','img17.jpg','img18.jpg','img19.jpg','img20.jpg','img21.jpg','img22.jpg',]
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
  #for i in range(0,df.shape[0]):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            s = str(hand_landmarks)
            x, y, z, pos = f(s)
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    image = cv2.resize(image, (1200, 850), cv2.INTER_NEAREST)
    if results.multi_hand_landmarks:
        color_yellow = (0, 0, 0)
        s = "X(left-right): " + str(x)
        s1 = "Y(down-up): " + str(y)
        #s2 = "Z(back-front): " + str(zn)
        if pos == 0:
            s3 = "unclenching"
        elif pos == 1:
            s3 = "clenching"
        elif pos == 2:
            s3 = "Front"
        elif pos == 3:
            s3 = "Back"
        elif pos == 4:
            s3 = "Click"
        print(i+1,file,s3,df.pos[i])
    i+=1
    # Print handedness and draw hand landmarks on the image.
    #print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      #print('hand_landmarks:', hand_landmarks)
      #print(
          #f'Index finger tip coordinates: (',
          #f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          #f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      #)
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(str(idx) + '.png', cv2.flip(annotated_image, 1))
