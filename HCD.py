# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:32:56 2019

@author: Katarzyna Goch
"""
import cv2
import numpy as np
import os
import csv


def getTheCoordinateArray(file):
    img = cv2.imread(os.path.join(os.getcwd(),'BirdData',file))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,1,0.04) ## ksize – Aperture parameter for the Sobel() operator had to be set to '1' (that is, no Gaussian smoothing is done while calculating the local maximums (so the derivatives of th 1 or 2 order) )
    
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]
    
    #cv2.imshow('dst',img)
    
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    
    
    
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    #print('width, heigth')
    #print(corners)    #here u can get corners check for more information follow the link...........http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
    
    theCoordinates = corners.tolist()
    
    return theCoordinates

#### Run files ####
    
wd = os.getcwd()   
files = os.listdir(os.path.join(wd,'BirdData'))

with open('shapes.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile, quoting=csv.QUOTE_NONE, escapechar=' ')
    for file in files:
        lines = getTheCoordinateArray(file)
        writer.writerow(lines)


