"""
# Captures a picture and calculates the brightests pixel on each y-axis
# pixel row. Returns the result of the calculation to the user.
"""
import numpy as np
import cv2.cv as cv
from math import tan, fabs, asin
import json

THRESHOLD_MIN_PWR = 25

def calcDistanceByPos(x, y, imgWidth):
    OFFSET = -0.03460372108
    GAIN = 0.0015772
    pfc = fabs(x - (imgWidth / 2))
    
    distance = 6.1 / tan( pfc * GAIN * OFFSET )
    
    CENTER_Y, thetaZ = 239, 0
    if not y == CENTER_Y:
        y = fabs(y - CENTER_Y)
        y *= 0.02645833333
        thetaZ = asin(y / distance)
        distance = y / tan( thetaZ )
    
    return distance, thetaZ

def findLaserCenterByRow(imgRow=None):
    if max(imgRow) < THRESHOLD_MIN_PWR or imgRow == None: return -1
    else: return np.argmax(imgRow)
        
def take_picture(camIndex=0, thetaX=0):
    capture = cv.CaptureFromCAM(camIndex)
    img = cv.QueryFrame(capture)
    
    imgGray = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
    cv.Smooth(imgGray, imgGray, cv.CV_GAUSSIAN, 3, 3)
    
    cv.SaveImage('output.jpg', img)
    cv.SaveImage('outputG.jpg', imgGray)
    
    openCV2npArr = np.asarray( imgGray[:,:] )
    brightestPoints = np.apply_along_axis(findLaserCenterByRow, axis=1, arr=openCV2npArr)
    
    scanOutput = []
    for y in range(len(brightestPoints)):
        distance, thetaZ = calcDistanceByPos(brightestPoints[y], y, imgGray.width)
        scanOutput.append({
            'x': brightestPoints[y],
            'y': y,
            'distance': distance,
            'thetaZ': thetaZ,
            'thetaX': thetaX
        })
    
    with open("scan-%s.txt" % thetaX, "w") as outfile:
        json.dump(scanOutput, outfile, indent=4)
 
if __name__=='__main__':
    take_picture()
    