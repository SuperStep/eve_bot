# -*- coding: utf-8 -*-
import pyautogui
from zones import Actions
import pickle
from reader import Area
from PIL import ImageGrab
from PIL import ImageOps
import numpy as np

import time
import math

def locate(imgPath, region = None):
    if region != None:
        coords = pyautogui.locateOnScreen(imgPath, region = region, grayscale=True)
    else:
        coords = pyautogui.locateOnScreen(imgPath, grayscale=True)
    if coords != None:
        return pyautogui.center(coords)
    else:
        return None

def SaveState(classObj):
    with open('name.pickle','wb') as f:
        pickle.dump(classObj, f)
        f.close()

class Laser:

    def __init__(self, num):
        
        self.coordinates = None
        self.yeld = 173.0
        self.num = num
        self.runs_remain = 0
        self.startedTime = None
        self.remainTime = None
        self.cycleTime = 60
           
        for i, coords in enumerate(pyautogui.locateAllOnScreen("screens/laser.jpg", region = Actions(), grayscale=True)):
            if num == i:
                self.coordinates = pyautogui.center(coords)
                if self.coordinates != None:
                    print('laser ready')
                    
    def Engage(self, asteroid):
        self.runs_remain = math.ceil(asteroid.volume / self.yeld)
        group_coords = asteroid.group_coordinates
        coords = asteroid.coordinates
        pyautogui.moveTo((group_coords[0] + 5, group_coords[1] + 5))
        pyautogui.click()
        pyautogui.moveTo((coords[0] + 5, coords[1] + 5))   
        pyautogui.keyDown('ctrl')
        pyautogui.click()
        pyautogui.keyUp('ctrl')
        time.sleep(3)
        pyautogui.click()
        time.sleep(1)
        if self.coordinates != None:          
            pyautogui.moveTo(self.coordinates[0], self.coordinates[1], duration=0.5)
            pyautogui.click()
            self.startedTime = time.time()
            self.remainTime = self.startedTime + (self.runs_remain * self.cycleTime)
            print('Laser %s starts mining asteroid: %s, %s seconds remain, (%s cycles)' % (self.num, asteroid, self.remainTime, self.runs_remain))
                    
class Scanner:
    
    def __init__(self):        
        self.coordinates = locate("screens/scanner.jpg", Actions())
        if self.coordinates != None:
            print('scanner ready')
            
    def Engage(self):
        if self.coordinates != None:          
            pyautogui.moveTo(self.coordinates[0], self.coordinates[1], duration=0.5)
            pyautogui.click()             
            
class Shield:

    def __init__(self):
        self.coordinates = locate("screens/shield.jpg", Actions())    

    def Engage(self):
        if self.coordinates != None:
            pyautogui.moveTo(self.coordinates[0], self.coordinates[1], duration=0.5)
            pyautogui.click()

class Drones:

    def Engage(self):
        pyautogui.press('f')

    def Disengage(self):
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')     

class OreHold:

    def __init__(self, capacity):
        self.coordinates = (50,506,431,765) #default
        self.capacity_coordinates = (53,526,436,535)
        self.closed = True
        self.overall_capacity = int(capacity)
        self.current_capacity = .0
        self.items = []

    def OpenClose(self):
        pyautogui.keyDown('alt')
        pyautogui.press('o')
        self.closed = not self.closed
        
    def GetItems(self):
        self.items.clear()

        hold_area = Area(self.coordinates)    
        data = hold_area.getTextAndBorders()           
        for row in data.split('\n'):
            item_data = dict(zip(["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"], row.split('\t')))
            if item_data['text'] == 'Kernite':               
                self.items.append(item_data)

    def IsFull(self):
        self.OpenClose()
        screen = np.array(ImageOps.invert(ImageGrab.grab()))
        self.OpenClose()
        px_end = screen[300,560]
        return px_end[2] > 220