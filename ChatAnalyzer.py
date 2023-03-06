from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
import pyautogui
import pytesseract
import win32gui
import re
from termcolor import colored

window_title = "Dofus Chat - Thegoodguy-[Ilz]"

chatColor = {
    "(/b)": "green",
    "(/r)": "light_magenta",
    "(/c": "dark_grey",
    "de": "light_blue",
    "(/g)": "magenta",
    "(/a)": "yellow",
    "(/p)": "blue",
    "(/s)": "white",
    "": "white"
}


def is_window_on_foreground(window_title):
    # Get handle of the currently active window
    foreground_window = win32gui.GetForegroundWindow()

    # Get handle of the window you're interested in
    window_handle = win32gui.FindWindow(None, window_title)

    # Compare the handles
    return foreground_window == window_handle


def update_screen():

    text = ""
    window = pyautogui.getWindowsWithTitle(window_title)[0]
    window.activate()
    while True:
        left, top, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(
            region=(left+10, top+65, width-20, height-80))
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # Perform OCR on the screenshot
        if is_window_on_foreground:
            text1 = pytesseract.image_to_string(Image.fromarray(screenshot))

            # Print the recognized text

            if text != text1:
                print("---------------------")

                tab = re.sub("[\[]\d\d.\d\d.\d\d[\]]",
                             "\n", text.replace("\n", "")).split("\n")
                for line in tab:
                    print(colored(line, chatColor.get(
                        line.lstrip().split(" ", 1)[0])))
                text = text1

        # Show area
        cv.imshow("Computer Vision", screenshot)
        key = cv.waitKey(10)
        if key == ord('q'):
            break


if __name__ == "__main__":
    update_screen()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
