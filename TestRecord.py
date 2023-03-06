from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
import pyautogui
import win32gui
import win32api


def update_screen():
    t0 = time.time()
    while True:
        window_title = "Dofus Chat - Thegoodguy-[Ilz]"
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            monitor = win32api.MonitorFromWindow(hwnd)
            monitor_info = win32api.GetMonitorInfo(monitor)
            left, top, right, bottom = monitor_info["Monitor"]
            screenshot = pyautogui.screenshot(region=(left+100, top, right, bottom))
            window_rect = win32gui.GetWindowRect(hwnd)
            window_left, window_top, window_right, window_bottom = window_rect
            window_width = window_right - window_left
            window_height = window_bottom - window_top
            crop_left = window_left - left
            crop_top = window_top - top
            crop_right = crop_left + window_width
            crop_bottom = crop_top + window_height
            screenshot = screenshot.crop((crop_left, crop_top, crop_right, crop_bottom))
            screenshot = np.array(screenshot)
            screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

            cv.imshow("Computer Vision", screenshot)
            key = cv.waitKey(10)
            if key == ord('q'):
                break
            ex_time = time.time() - t0
            print("FPS: " + str(1 / (ex_time)))
            t0 = time.time()


if __name__ == "__main__":
    update_screen()