#! /usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui
import win32api
import win32con
import keyinput
import time
from cWindow import cWindow

def get_all_windows():
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    return hWndList

def get_child_windows(parent):
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, okl,  None)
    return hwndChildList

def okl(*args, **kwargs):
    print(args)

def get_one_window(title):
    for w in get_all_windows():
        if title==win32gui.GetWindowText(w):
            return w

hg =["微信","WeChatMainWndForPC"]

if __name__ == "__main__":

    cW = cWindow()
    cwnd=cW.getWeiXin()
    cW.SetAsForegroundWindow()
    keyinput.key_input("反倒是官方")
    keyinput.input_enter()