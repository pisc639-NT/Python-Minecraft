import win32gui
import win32ui
import pyautogui
from ctypes import windll
from PIL import Image
import numpy as np
import re
import os
from fuzzywuzzy import process
import PIL
import utils
import time

def get_size():
    # return np.dtype(np.array(list(os.get_terminal_size())) * 0.9, int)
    return os.get_terminal_size()

def first_element(l, default=None, depth=1):
    for _ in range(depth):
        l = l[0] if len(l) > 0 else default
    return l

def ascii(image, set_size:tuple[int, int]):
    width, height = image.size
    # set minimum size
    new_width, new_height = set_size
    new_height = int(min(new_height, new_width / width * height))
    # end set minimum size
    ratio = height/width/2
    new_width = int(new_height/ratio)    
    color_data = np.array(image.resize((new_width, new_height)).convert("RGB")).reshape(-1, 3)
    # print(new_height, new_width)
    resized_image = image.resize((new_width, new_height))
    gray_image = resized_image.convert("L")
    # ascii_chars = ["@", "#", "S", "%","?", "*", "+", ";", ":", ",", "."]
    ascii_chars = str((r""" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""))
    pixel_data = gray_image.getdata()
    # get = pixel_data[0]
    # print(get, dir(get))
    div = int(280 / len(ascii_chars))
    # print(f"{ascii_chars}")
    # string = np.array([utils.color_text(ascii_chars[pixel_data[i]//div], color=color_data[i]) for i in range(len(pixel_data))])
    string = np.array([utils.color_text("█", color=color_data[i]) for i in range(len(pixel_data))])
    string = string.reshape(new_height, new_width)
    # ascii_string = "\n".join([string[i:(i+new_width)] for i in range(0, length, new_width)])
    ascii_string = "\n".join(["".join([str(j) for j in i]) for i in string])
    return ascii_string


def save_print_win(window_name:str, fpath):

    win_list = [str(i.title).lower() for i in pyautogui.getAllWindows() if len(i.title) > 0]
    # print(win_list)
    window_name = process.extract(window_name, win_list)
    # window_name = [i for i in win_list if window_name in i]
    window_name = first_element(window_name, default="", depth=2)
    # print(window_name)
    hwnd = win32gui.FindWindow(None, window_name)
    
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    left, top, right, bot = np.array([left, top, right, bot]) + [0, 0, -16, -39]
    w = right - left
    h = bot - top
    w, h = int(w), int(h)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    output = "\n"
    output += f"result: {result}\n"

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        output += 'PrintWindow Succeeded\n'
        # output += ascii(im, os.get_terminal_size())
        output = "\n"
        output += ascii(im, get_size())
        print(output, end="")
        #PrintWindow Succeeded
        # im = im.resize((os.get_terminal_size()[0], os.get_terminal_size()[1]))
        im = im.resize(get_size())
        im.save(fpath)
    else:
        output += 'PrintWindow Failed\n'
        print(output, end="")

if __name__ == '__main__':
    while True:
        save_print_win('Tlauncher', 'out.png')
        # exit()
        time.sleep(0.5)