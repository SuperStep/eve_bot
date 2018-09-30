# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 23:28:04 2018

@author: Дарья
"""

from enum import Enum
import pyautogui
import prettytable
from zones import Actions
from reader import Area
import numpy as np
from PIL import ImageGrab
from PIL import ImageOps
import cv2.cv2 as cv2


import equipment
from entities import Asteroid

import time

def Inventory():
    if locate("screens/undock.jpg") != None:
        if locate("screens/inventory_panel.png") == None:
            pyautogui.keyDown('alt')
            pyautogui.press('g')

def Undock():
    point = locate("screens/undock.jpg")
    if point != None:       
        pyautogui.moveTo(point[0], point[1], duration=0.5)
        pyautogui.click()  

def locate(imgPath, region = None):
    if region != None:
        coords = pyautogui.locateOnScreen(imgPath, region = region, grayscale=True)
    else:
        coords = pyautogui.locateOnScreen(imgPath, grayscale=True)
    if coords != None:
        return pyautogui.center(coords)
    else:
        return None
    
def GetOreNearby(oreName, need_quantity = 2, max_distance = 11000, min_volume = 100, current_asteroids = []):

    asteroids = []
    
    if pyautogui.locateOnScreen("screens/scanpanel.png", grayscale=True) == None:
        scanner = equipment.Scanner()
        scanner.Engage()
        time.sleep(6)
           
    scan_data, panel_coords = ReadMiningScaner()
    
    oreslist = SearchOreOnScan(scan_data, panel_coords, oreName, 0, False)

    panel_start = (panel_coords[0], panel_coords[1])

    for i, asteroid in enumerate(oreslist):
        target_ore = (int(asteroid.get('left'))/20, int(asteroid.get('top'))/20)
        group_coordinates = tuple(map(sum, zip(panel_start, target_ore)))    

        pyautogui.moveTo(group_coordinates)
        pyautogui.click()

        time.sleep(1)

        for coords in pyautogui.locateAllOnScreen("screens/scan_info_sign.png", grayscale=True, region = panel_coords):          
            detail_coords = (panel_coords[0], coords[1], panel_coords[2], coords[1] + coords[3])
            
            area = Area(detail_coords)
            text = area.getTextZoomed(20).replace('%', '0')
            text = oreName + text.split(oreName, 1)[1]
            print(detail_coords,text)
            ore_parameters = dict(zip(["ore_type","quantity","volume","vol_units","distance","dis_units"], text.split(' ')))
            ore_parameters['group_coordinates'] = group_coordinates
            ore_parameters['coordinates'] = detail_coords
            asteroid = Asteroid(**ore_parameters)
            #Check if this asteroid already being mined
            for current_asteroid in current_asteroids:
                if asteroid.coordinates == current_asteroid.coordinates:
                    continue
            #Check if it meets requirements
            if asteroid.distance < max_distance and asteroid.volume > min_volume:
                asteroids.append(asteroid)
            if len(asteroids) == need_quantity:
                pyautogui.click()
                return asteroids

        #close current group if got not enough roids
        pyautogui.click()
    
def ReadMiningScaner():
    
    panel_coords = LocateScanPanel() 
    scanDataArea = Area(panel_coords)    
    CloseScannerTabs(panel_coords)
    data = scanDataArea.getTextAndBorders()

    return (data, panel_coords)

def LocateScanPanel():
    coordinates = pyautogui.locateOnScreen("screens/scanpanel.png", grayscale=True)
    coordinates_bottom = pyautogui.locateOnScreen("screens/scanpanel_bottom.png", grayscale=True)  
    return (coordinates[0], coordinates[1], coordinates_bottom[0] + coordinates_bottom[2], coordinates_bottom[1] + coordinates_bottom[3])

def CloseScanPanel():
    coordinates_bottom = pyautogui.locateOnScreen("screens/scanpanel_bottom.png", grayscale=True) 
    if coordinates_bottom != None:
        pyautogui.moveTo(pyautogui.center(coordinates_bottom), duration=0.5)
        pyautogui.click()   

def CloseScannerTabs(panel_coords = None):
    if panel_coords == None:
        panel_coords = LocateScanPanel()
    open_groups_list = []
    for group_opened in pyautogui.locateAllOnScreen("screens/scanpanel_group_opened.jpg", grayscale=True, region = panel_coords):
        open_groups_list.append(group_opened)

    for group_opened in reversed(open_groups_list):
        if group_opened != None:
            pyautogui.moveTo(pyautogui.center(group_opened), duration=0.5)  
            pyautogui.click()

def ReadMiningScanerDetails(panel_coords):
    
    scanDataArea = Area(panel_coords)    
    return (scanDataArea.getTextAndBorders(), panel_coords)

def SearchOreOnScan(scan_data, panel_coords, oreName, minimum, test = False):
    
    oreslist = []
    
    if test:       
        x = prettytable.PrettyTable(["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"]) 
                
    for row in scan_data.split('\n')[1:]:
        if test:
            x.add_row(row.split('\t'))
        oreslist.append(dict(zip(["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"], row.split('\t'))))
        
    if test:
        print(x)
        
    if len(oreslist) > 0:       
        return list(filter(lambda ore: ore['text'] == oreName, oreslist))
    else:
        return oreslist
    
def GetDataFromRows(data, panel_coords, oreName):
    data_list = []
    for row in data.split('\n'):
        data_list.append(dict(zip(["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"], row.split('\t'))))
    if len(data_list) > 0:       
        return list(filter(lambda ore: ore['text'] == oreName, data_list))
    else:
        return data_list       
    
def WarpToPoint(pointName):
    zoom = 10
        
    screen_size = pyautogui.size()
    screen_center = (screen_size[0]/2, screen_size[1]/2 - 250)
    pyautogui.moveTo(screen_center)
    pyautogui.rightClick()

    menu_area = Area((screen_center[0]+10, screen_center[1], screen_center[0] + 230, screen_center[1] + 215))
    data = menu_area.getTextAndBorders(zoom)
    
    results = []
    for row in data.split('\n')[1:]:
        results.append(dict(zip(["level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"], row.split('\t'))))   
    
    try:
        result = list(filter(lambda ore: ore['text'] == pointName, results))
        button_coords = (int(int(result[0].get('left'))/zoom), int(int(result[0].get('top'))/zoom))
        pyautogui.moveRel(button_coords[0]+10, button_coords[1], duration = 0.5)
        pyautogui.click()
        pyautogui.moveRel(250, duration = 0.5)
        pyautogui.click()
    except:
        cv2.imwrite('messigray.png',menu_area.getImg())  
        raise

class actionType(Enum):
    PRESS = 1
    UNDOCK = 2

class Action:
    
    def __init__(self, actionType, target):
        self.type = actionType
        self.target = target
        
    