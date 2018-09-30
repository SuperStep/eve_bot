# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 20:49:45 2018

@author: Дарья
"""

import cv2.cv2 as cv2
import numpy as np
from PIL import ImageGrab

class ScreenDebugger:

    def __init__(self):
        self.screen = np.array(ImageGrab.grab())

    def Show(self):   
        cv2.imshow('areas on screen', self.screen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def AddArea(self, coords, _color):
        if _color == 'green':
            color = (0, 255, 0)
        elif _color == 'red':
            color = (0, 0, 255)
        elif _color == 'blue':
            color = (255,0,0)

        cv2.rectangle(self.screen, (coords[0],coords[1]), (coords[2], coords[3]), color, 2)    