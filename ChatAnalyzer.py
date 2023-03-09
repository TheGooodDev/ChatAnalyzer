from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
import pyautogui
import pytesseract
import win32gui
import re
import win32gui
import win32ui
import win32.lib.win32con as win32con
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

class Message:
    def __init__(self, User, Time, Content, Type):
        self.User = User
        self.Time = Time
        self.Content = Content
        self.Type = Type
    
    def toString(self):
        return "{self.Time} {self.User} {self.Content}"


def update_screen():

    text = ""
    window = pyautogui.getWindowsWithTitle(window_title)[0]
    hwnd = win32gui.FindWindow(None, "Dofus Chat - Thegoodguy-[Ilz]")

    while True:
        left, top, width, height = window.left, window.top, window.width-20, window.height-20
        screenshot = background_screenshot(hwnd, width, height)

        bitmap_image = Image.fromarray(screenshot)

        # Convert to grayscale
        grayscale_image = bitmap_image.convert('RGB')
        text1 = pytesseract.image_to_string(grayscale_image)
        # Print the recognized text
        if text != text1:
            print("---------------------")
            text = text1
            tab = list_to_message(text.split("\n"))
            for line in tab:
                print(line)
            # tab = re.sub("[\[]\d\d.\d\d.\d\d[\]]",
            #              "\n", text.replace("\n", "")).split("\n")
            # for line in tab:
            #     print(colored(line, chatColor.get(
            #         line.lstrip().split(" ", 1)[0])))


        # Show area
        # cv.imshow("Computer Vision", screenshot)
        key = cv.waitKey(10)
        if key == ord('q'):
            break

def return_categorie(s):
    s.lstrip().split(" ", 1)[0]
    if "(/t)"in s:
        return "equipe"
    elif "(/g)"in s:
        return "guilde"
    elif "(/a)" in s:
        return "alliance"
    elif "(/p)" in s:
        return "groupe"
    elif "(/b)" in s:
        return "commerce"
    elif "(/r)" in s:
        return "recrutement"
    elif "de" in s:
        return "prive"
    elif "(/c" in s:
        return "communaute"
    elif "(info)" in s:
        return "info"
    elif "(combat)" in s:
        return "combat"
    else:
        return "general"


def list_to_message(s):
    messages = []
    for line in s:
        if re.compile("[\[]\d\d.\d\d.\d\d[\]]").search(line):
            time = line[:10]
            line = re.sub("[\[]\d\d.\d\d.\d\d[\]]","", line)
            pattern = line.lstrip().split(" ", 1)[0]
            categorie = return_categorie(pattern)
            if categorie == "communaute":
                for _ in range(2):
                    line = line.replace(line.lstrip().split(" ", 1)[0], "")
            else:
                line = line.replace(line.lstrip().split(" ", 1)[0], "")
            
            print(line)

    return messages




            

def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((-10,-65),(width, height) , dcObj, (0,0), win32con.SRCCOPY)

    # Get the bitmap data as a numpy array
    data = dataBitMap.GetBitmapBits(True)
    bitmap_array = np.frombuffer(data, dtype=np.uint8)
    bitmap_array = np.reshape(bitmap_array, (height, width, 4))[:,:,2::-1]
    return bitmap_array

if __name__ == "__main__":
    update_screen()

