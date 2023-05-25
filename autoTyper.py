from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

left, top, right, bottom = 525, 775, 1380, 800 #TypeRacer
left, top, right, bottom = 350, 450, 1600, 500 #TypeMonkey
pixelMulti = 23 #TypeRacer
pixelMulti = 40 #TypeMonkey
delay = 0
imageArr = []

def captureScreen(left, top, right, bottom):
    return reduceNoise(ImageGrab.grab(bbox=(left, top, right, bottom)))

def convertLinesToText(startLine, endLine):
    text = ""
    for i in range(startLine, endLine):
        imageArr.append(captureScreen(left, top+i*pixelMulti, right, bottom+i*pixelMulti))
        text += pytesseract.image_to_string(imageArr[len(imageArr)-1]) + " "

    return text

def reduceNoise(img):
    original = np.array(img).copy()

    # change all yellow (196,156,28) pixels to black (50,52,55)
    hsv = cv2.cvtColor(np.array(img.convert('RGB'))[:, :, ::-1].copy(), cv2.COLOR_BGR2HSV)

    # Defining lower and upper bound HSV values
    lower = np.array([22, 93, 0], dtype="uint8")
    upper = np.array([45, 255, 255], dtype="uint8")

    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(original, (x, y), (x + w - 2, y + h), (50,52,55), 2)  # 50,52,55 - background

    return original

if __name__ == "__main__":
    time.sleep(3)
    stopper = time.time()
    iter = 0
    start = 0

    while (time.time() - stopper) < 30:
        text = convertLinesToText(start, 3)
        pyautogui.typewrite(text, delay)

        if (iter == 0):
            start += 1
        iter += 1

        if (delay == 0):
            time.sleep(0.25)






