# -*- coding: utf-8 -*-

import sys
import time
import tkinter
import traceback

import cv2.cv2 as cv2
import keyboard
import numpy as np
#import pandas as pd
import prettytable
import pyautogui
from PIL import ImageGrab, ImageOps

import actions
import equipment
#import win32gui
import zones
from reader import Area
from screen_debugger import ScreenDebugger


def WarpDriveActive():
    area = Area((10,989,873,1014))
    text = area.getTextZoomed(10)
    print('speed text =', text)
    return 'arp' in text 

def LasersNeedToRepeat(lasers):
    lasersToRun = []
    for laser in lasers:
        if laser.remainTime == None or laser.remainTime <= time.time():
            lasersToRun.append(laser)
    
    return lasersToRun


def StartMining():
    '''
    actions.Undock()   
    time.sleep(15)
    actions.WarpToPoint('Mine')          
    time.sleep(15)
    while WarpDriveActive():
        time.sleep(5)          
    '''
    #Came to mining site -------------
    #Init equipment
    shield = equipment.Shield()
    scanner = equipment.Scanner()
    drones = equipment.Drones()
    lasers = []
    lasers.append(equipment.Laser(0))
    lasers.append(equipment.Laser(1))
    ore_hold = equipment.OreHold(5000)
    current_asteroids = []
    #---------------------------------
    '''
    shield.Engage()
    drones.Engage()
    '''
    while True: #not ore_hold.IsFull():

        lasers = LasersNeedToRepeat(lasers)
        lasersCount = len(lasers)
        if lasersCount > 0:
            try:
                current_asteroids = actions.GetOreNearby('Kernite', 2, 10000, 100, current_asteroids)

                for i, asteroid in enumerate(current_asteroids[:lasersCount]):   
                    actions.CloseScannerTabs() 
                    lasers[i].Engage(asteroid)

                #actions.CloseScanPanel()   
                time.sleep(10)
            except Exception as err:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tbe = traceback.TracebackException(
                    exc_type, exc_value, exc_tb,
                )
                print(''.join(tbe.format()))

                print('\nexception only:')
                print(''.join(tbe.format_exception_only()))
            finally:
                print('stop here')


'''1366 x 768'''

wasKeyPressedTheLastTimeWeChecked = False
print('ready...')
while True:
    if keyboard.is_pressed('a') and not wasKeyPressedTheLastTimeWeChecked:
        StartMining()
        break
