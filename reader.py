# -*- coding: utf-8 -*-
import numpy as np
from PIL import ImageGrab
from PIL import ImageOps
import pytesseract
from pytesseract import Output
import cv2.cv2 as cv2
import scipy.ndimage as ndi

class Area:
    
    
    def __init__(self, coordinate):
        
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'      
        self.tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"' 

        self.coordinate = coordinate

    def getText(self):
        screen = np.array(ImageOps.invert(ImageGrab.grab(bbox=(self.coordinate)).convert('L')))  
        resized_image = cv2.resize(screen, (int(3000), int(3000)), interpolation=cv2.INTER_CUBIC )
        return pytesseract.image_to_string(resized_image, lang="eng", config=self.tessdata_dir_config) 
    
    def getTextZoomed(self, multiply):
        screen = np.array(ImageOps.invert(ImageGrab.grab(bbox=(self.coordinate)).convert('L')))  
        width = int((self.coordinate[2] - self.coordinate[0]) * multiply)
        height = int((self.coordinate[3] - self.coordinate[1]) * multiply)
        resized_image = cv2.resize(screen, (width, height) , interpolation=cv2.INTER_CUBIC )
        return pytesseract.image_to_string(resized_image, lang="eng", config=self.tessdata_dir_config)   
    
    def getTextAndBorders(self, multiply = 20):
        screen = np.array(ImageOps.invert(ImageGrab.grab(bbox=(self.coordinate)).convert('L'))) 
        width = int((self.coordinate[2] - self.coordinate[0]) * multiply)
        height = int((self.coordinate[3] - self.coordinate[1]) * multiply)
        resized_image = cv2.resize(screen, (width, height), interpolation=cv2.INTER_CUBIC )
        return pytesseract.image_to_data(resized_image, lang="eng", config=self.tessdata_dir_config)
    
    def getImg(self):
        return np.array(ImageOps.invert(ImageGrab.grab(bbox=(self.coordinate)).convert('L')))
    
    def getBorders(self):
        screen = np.array(ImageGrab.grab(bbox=(self.coordinate))) 
        cv2.imshow("Line Detection", screen)
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        smooth = ndi.filters.median_filter(gray, size=2)
        edges = smooth > 180
        lines = cv2.HoughLines(edges.astype(np.uint8), 0.5, np.pi/180, 120)
        print(len(lines))
        for rho,theta in lines[0]:
            print(rho, theta)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(screen,(x1,y1),(x2,y2),(0,0,255),2)
            
        return cv2.imshow("Line Detection", screen)
