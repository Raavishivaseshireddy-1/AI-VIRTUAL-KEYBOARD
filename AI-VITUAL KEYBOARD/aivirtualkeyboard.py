import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1000)
cap.set(4, 450)


detector = HandDetector(detectionCon=0.8)
keys = [["1","2","3","4","5","6","7","8","9","0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        [">", "<"]]
finalText = []

keyboard = Controller()
keyboard.press(Key.space)
keyboard.release(Key.space)

keyboard.press(Key.backspace)
keyboard.release(Key.backspace)


def drawAll(img, buttonlist):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 15, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (34, 139, 34), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    return img


def transparent_layout(img, buttonList):
    img = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0],button.size[0]), 15, rt=0)
        cv2.rectangle(img, button.pos, (x + button.size[0], y + button.size[1]), (34, 139, 34), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    out = img.copy()
    alpaha = 0.5
    mask = img.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, img, 1-alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [50, 50]
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([75 * x + 30, 75 * i + 30], key))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (38, 178, 247), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 60:
                    if "<" in button.text:
                        finalText.pop()
                        keyboard.press(Key.backspace)
                    if ">" in button.text:
                        finalText.append(" ")
                        keyboard.press(Key.space)
                    else:
                        keyboard.press(button.text)
                        finalText.append(button.text)
                    sleep(0.25)

    cv2.imshow("Keyboard", img)
    cv2.waitKey(1)
