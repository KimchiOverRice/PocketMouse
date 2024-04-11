#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:36:07 2024

@author: kimiasattary
"""

import pyautogui as p
from pynput import keyboard
from pynput.keyboard import Key
'''
while True:
    c_x, c_y = p.position()
    x = int(input('x'))
    y = int(input('y'))
    p.moveRel(x + c_x, y + c_y, duration = 1)

'''
def on_key_release(key):

    if key == Key.right:
        print("Right key clicked")
        p.moveRel(50, 0, duration = 1)
    elif key == Key.left:
        print("Left key clicked")
        p.moveRel(-50, 0, duration = 1)
    elif key == Key.up:
        print("Up key clicked")
        p.moveRel(0, -50, duration = 1)
    elif key == Key.down:
        print("Down key clicked")
        p.moveRel(0, 50, duration = 1)
    elif key == Key.esc:
        exit()


with keyboard.Listener(on_release=on_key_release) as listener:
    listener.join()



