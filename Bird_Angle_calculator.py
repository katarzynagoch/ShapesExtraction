"""
Created on Wed Jun 19 2019

@author: jan seemann, felix niebl

NOTE:   Please make sure the input file that is referred to in the variable
        filePath contains the coordinates of the polygon-vertices in the
        following format: [(x0,y0),(x1,y1), ... ,(x11,y11)].
        For sake of the project, a polygon should only contain 12 vertices.
        The script will save the output file into the same folder it ran in.
        
"""
#filePath alter this file to the location of your input file
filePath_ShapeToAngle = "birdShapes.txt"

import re
import numpy as np


def processBirdFile(argument):
    print(readFile(argument)) #call readFile-function with the filePath data

def readFile(path):  
    file = open(path, "rt")
    fileData = file.read()

    #first, read the file and fetch all the arrays.
    coordArrays = re.findall("\[(.*?)\]" ,fileData)
    coordArrays2 = []
    for coords in coordArrays:
        coords = "[["+coords+"]]"
        coordArrays2.append(coords)

    #create an array for each bird that contains it's angles for each vertex
    angles = []
    for coords in coordArrays2:
        coords = np.array(eval(coords))
        bird = create_angleArray(coords)
        angles.append(bird)

    #now we create the new file
    newFile = open("birdAngles.txt", "w+")

    #replace the angles with the new coordinates...
    for bird in angles:
        fileData = re.sub("\[\((.*?)\]", str(bird), fileData, 1)
    
    #write the new coordinates into the new file
    newFile.write(fileData)

"""
function calc_angle and create_AngleArray created by Jan Seemann
"""
def calc_angle (vertex1, vertex2, vertex3):
    #print(vertex1)
    #print(vertex2)
    #print(vertex3)
    """Calculates the angles between 3 vertices."""
    ray1 = vertex1 - vertex2
    ray2 = vertex3 - vertex2
    cosine_angle = np.dot(ray1, ray2) / (np.linalg.norm(ray1) * np.linalg.norm(ray2))
    #print (cosine_angle)
    arccos_angle = np.arccos(cosine_angle)

    return np.degrees(arccos_angle)

def create_angleArray(verticeArray):
    """Creates an array of angles form an array of vertices."""
    array2 = verticeArray[0]
    angleArray = []
    i = len(array2)
    for j in range(i):
        angle = calc_angle(array2[j-3], array2[j-2], array2[j-1])
        angleArray.append(angle) 
 
    return angleArray

if __name__ == "__main__":
    processBirdFile(filePath_ShapeToAngle)