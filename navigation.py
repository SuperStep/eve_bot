# -*- coding: utf-8 -*-

import numpy as np
import cv2.cv2 as cv2
import pyautogui
import keyboard
import prettytable
from PIL import ImageGrab
from PIL import ImageOps

from reader import Area
import zones
import actions
import equipment
from screen_debugger import ScreenDebugger

import pandas as pd
import time

wasKeyPressedTheLastTimeWeChecked = False
while True:
    if keyboard.is_pressed('a') and not wasKeyPressedTheLastTimeWeChecked:
    
        print('go')



    