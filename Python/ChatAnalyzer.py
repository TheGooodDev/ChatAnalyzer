from PIL import Image as Pilimage, ImageGrab
import numpy as np
import cv2 as cv
import time
import pyautogui
import pytesseract
import re
import win32gui
import win32ui
import win32.lib.win32con as win32con
from termcolor import colored
from datetime import datetime
from tkinter import *
import json

window_title = "Dofus Chat - Thegoodguy-[Ilz]"

class Message:

    def __init__(self, User, Time, Content, Type):
        self.user = User
        self.time = Time
        self.content = Content
        self.type = Type

    def toString(self):
        return f"[{self.time}] {self.user} {self.content}"

    def to_dict(self):
        return {
            "user": self.user,
            "time": str(self.time),
            "content": self.content,
            "type": self.type
        }


ChatLog = []


def update_screen():

    text = ""
    window = pyautogui.getWindowsWithTitle(window_title)[0]
    hwnd = win32gui.FindWindow(None, "Dofus Chat - Thegoodguy-[Ilz]")
    while True:
        left, top, width, height = window.left, window.top, window.width-20, window.height-20
        screenshot = background_screenshot(hwnd, width, height)

        bitmap_image = Pilimage.fromarray(screenshot)

        # Convert to grayscale
        grayscale_image = bitmap_image.convert('RGB')
        text1 = pytesseract.image_to_string(grayscale_image)
        # Print the recognized text
        if text != text1:
            text = text1
            list_to_message(text.split("\n"))
            chat_log_json = json.dumps(
                [msg.to_dict() for msg in ChatLog])
            with open('chatLog.json', 'w') as f:
                f.write(chat_log_json)

            # Show area
            # cv.imshow("Computer Vision", screenshot)


def return_categorie(s):
    s.lstrip().split(" ", 1)[0]
    if "(/t)" in s:
        return "equipe"
    elif "(/g)" in s:
        return "guilde"
    elif "(/a)" in s:
        return "alliance"
    elif "(/p)" in s:
        return "groupe"
    elif "(/b)" in s:
        return "commerce"
    elif "(/r)" in s:
        return "recrutement"
    elif "(/c" in s:
        return "communaute"
    elif "(Info)" in s:
        return "info"
    elif "(Combat)" in s:
        return "combat"
    elif "de " in s:
        print(s)
        return "prive"
    elif "a " in s:
        print(s)
        return "prive"
    else:
        return "general"


def list_to_message(s):

    for line in s:
        if re.compile("[\[]\d\d.\d\d.\d\d[\]]").search(line):
            try:
                time = datetime.strptime(line[:10], "[%H:%M:%S]").time()
            except:
                return
            if ChatLog:
                if (time < ChatLog[len(ChatLog)-1].time):
                    continue
            line = re.sub("[\[]\d\d.\d\d.\d\d[\]]", "", line)
            pattern = line.lstrip().split(" ", 1)[0]
            categorie = return_categorie(pattern)
            if categorie == "communaute":
                for _ in range(2):
                    line = line.replace(line.lstrip().split(" ", 1)[0], "")
            else:
                line = line.replace(line.lstrip().split(" ", 1)[0], "")
            if isUser(categorie):
                name = line.lstrip().split(":", 1)[0]
            else:
                name = ""

            name = ' '.join(name.split())
            valide = True
            if ChatLog:
                for checkMessage in reversed(ChatLog):
                    if time < checkMessage.time:
                        break
                    if len(ChatLog) > 2:
                        if (name == checkMessage.user and categorie == checkMessage.type):
                            valide = False
                            break
            line = line.replace(line.lstrip().split(" ", 1)[0], "")
            content = ' '.join(line.split())
            message = Message(name, time, content, categorie)
            if content and valide:
                ChatLog.append(message)


def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((-10, -65), (width, height), dcObj, (0, 0), win32con.SRCCOPY)

    # Get the bitmap data as a numpy array
    data = dataBitMap.GetBitmapBits(True)
    bitmap_array = np.frombuffer(data, dtype=np.uint8)
    bitmap_array = np.reshape(bitmap_array, (height, width, 4))[:, :, 2::-1]
    return bitmap_array

def isUser(categorie):
    return categorie != "combat" and categorie != "info"

if __name__ == "__main__":
    update_screen()


