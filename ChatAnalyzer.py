from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
import pyautogui
import pytesseract

def update_screen():

    t0 = time.time()
    window_title = "Dofus Chat - Thegoodguy-[Ilz]"
    window = pyautogui.getWindowsWithTitle(window_title)[0]
    window.activate()
    while True:
        left, top, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(region=(left+10, top+70, width-20, height-80))
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # Perform OCR on the screenshot
        text = pytesseract.image_to_string(Image.fromarray(screenshot))

        # Print the recognized text
        print("---------------------")
        print(text)
        print("---------------------")

        cv.imshow("Computer Vision", screenshot)
        key = cv.waitKey(10)
        if key == ord('q'):
            break


if __name__ == "__main__":
    update_screen()
