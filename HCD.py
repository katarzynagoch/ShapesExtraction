# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:32:56 2019

@author: Katarzyna Goch
modified by Felix Niebl
"""
import cv2
import numpy as np
import os
import Bird_Angle_calculator as computeAngles
#import csv

birdData = 'BirdSilhouettes'
birdShapeOutputFile = "birdShapes.txt"

#helping function to write the coordinates as tuples (https://stackoverflow.com/questions/10016352/convert-numpy-array-to-tuple)
def toTuple(a):
    try:
        return tuple(toTuple(i) for i in a)
    except TypeError:
        return a

def getTheCoordinateArray(file):
    img = cv2.imread(os.path.join(os.getcwd(),birdData,file))
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
    
    #NOTE: Felix here, removed following lines as they were causing my system to freeze up. seems to work without. I am not entirely sure what they do.
    #if cv2.waitKey(0) & 0xff == 27:
        #cv2.destroyAllWindows()
    #print(cv2.waitKey(0))
    cv2.destroyAllWindows()
    
    #Felix: changed this up so the coordinates get returned as a tuple (x,y) instead of a list [x,y] so it can work with the angle-calculation-script
    theCoordinates = toTuple(corners.tolist())
    
    return theCoordinates

#### Run files ####

wd = os.getcwd()   
files = os.listdir(os.path.join(wd,birdData))

#Felix: created own file-writing procedure to make the file easier readable to the angle-calculator
birdShapeOutput = open(birdShapeOutputFile, "w+")
for file in files:
    
    #thrown-together code to make the output strings readable for the angle-calculator
    lines = getTheCoordinateArray(file)
    lines = str(lines)
    lines = lines[1:-1]
    
    #it is not as elegant, but i couldn't get it done properly with csv.writer()
    birdShapeOutput.write("[")
    birdShapeOutput.write(lines)
    birdShapeOutput.write("]\n")
    

computeAngles.processBirdFile(birdShapeOutputFile)

"""
with open('shapes.txt', 'w') as writeFile:
    writer = csv.writer(writeFile, quoting=csv.QUOTE_NONE, escapechar=' ')
    for file in files:
        print(file)
        lines = getTheCoordinateArray(file)
        writer.writerow(lines)
"""