"""
# Captures a picture and calculates the brightests pixel on each y-axis
# pixel row. Returns the result of the calculation to the user.
"""
import numpy as np
import cv2.cv as cv
import cv2
from time import sleep
from math import tan, fabs, asin
import json

THRESHOLD_MIN_PWR = 25

def calcDistanceByPos(x, y, imgWidth):
    OFFSET = -0.5609729362 #-0.03460372108
    GAIN = 0.001575387042  #0.014967  #0.0015772
    print imgWidth, x[0]
    pfc = fabs(x[0] - (imgWidth / 2))
    
    distance = 6.1 / tan( pfc * GAIN + OFFSET )
    
    CENTER_Y, thetaZ = 0, 0
    
    y = abs(239 - y)
    
    if not y == CENTER_Y and distance > y:
        print distance, y
        y = fabs(y - CENTER_Y)
        y *= 0.02645833333
        thetaZ = asin(y / distance)
        distance = y / tan( thetaZ )
    
    return abs(distance), thetaZ

def findLaserCenterByRow(imgRow=None):
    if max(imgRow) < THRESHOLD_MIN_PWR or imgRow == None: return -1
    else: return np.argmax(imgRow)
    
def take_picture2():
    import Adafruit_BBIO.GPIO as GPIO
    
    LASER_PIN = "P8_10"
    
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.output(LASER_PIN, GPIO.HIGH)
    
    cap = cv2.VideoCapture(-1)
    ret, frame = cap.read()
    
    for i in range(20):
        ret, frame = cap.read()
        #grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        """img = cv.CreateImageHeader((frame.shape[1], frame.shape[0]), cv.IPL_DEPTH_8U, 3)
        cv.SetData(img, frame.tostring(), frame.dtype.itemsize * 3 * frame.shape[1])
        
        imgGray = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
        
        #cv2.imwrite('Pictures/img-Gray-%s.jpg' % i, grayFrame)
        cv.SaveImage('Pictures/img-Image-%s.jpg' % i, imgGray)"""
    
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # define range of red color in HSV
        lower_red = np.array([155,50,50])
        upper_red = np.array([185,255,255])
    
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
    
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        # pfc range for laser
        mask2 = np.zeros(res.shape[:2],np.uint8)
        mask2[0:640,430:550] = 255
        res2 = cv2.bitwise_and(res,res,mask = mask2)
    
        cv2.imwrite('frame.jpg',frame)
        cv2.imwrite('mask.jpg',mask)
        cv2.imwrite('res.jpg',res)
        cv2.imwrite('imask.jpg', res2)
    
    brightestPoints = np.apply_along_axis(findLaserCenterByRow, axis=1, arr=res2)
    
    thetaX = 0
    
    scanOutput = []
    for y in range(len(brightestPoints)):
        distance, thetaZ = calcDistanceByPos(brightestPoints[y], y, 640)
        scanOutput.append({
            'x': brightestPoints[y][0],
            'y': y,
            'distance': distance,
            'thetaZ': thetaZ,
            'thetaX': thetaX
        })
    
    with open("out-%s.txt" % thetaX, "w") as outfile:
        json.dump(scanOutput, outfile, indent=4)
    
    cap.release()
    
    GPIO.output(LASER_PIN, GPIO.LOW)
    GPIO.cleanup()
        
def take_picture(camIndex=-1, thetaX=0):
    capture = cv.CaptureFromCAM(camIndex)
    if not capture:
        print "Camera not found"
        return -1
    img = cv.QueryFrame(capture)
    if img == None:
        print "Frame not captured."
        return -1
    
    imgGray = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
    
    cv.SaveImage('output.jpg', img)
    cv.SaveImage('outputG.jpg', imgGray)
    
    pixel = img[250, 250]
    print pixel
    
    openCV2npArr = np.asarray( imgGray[:,:] )
    brightestPoints = np.apply_along_axis(findLaserCenterByRow, axis=1, arr=openCV2npArr)
    
    thetaX = 0
    
    scanOutput = []
    for y in range(len(brightestPoints)):
        distance, thetaZ = calcDistanceByPos(brightestPoints[y], y, 640)
        scanOutput.append({
            'x': brightestPoints[y],
            'y': y,
            'distance': distance,
            'thetaZ': thetaZ,
            'thetaX': thetaX
        })
    
    with open("out-%s.txt" % thetaX, "w") as outfile:
        json.dump(scanOutput, outfile, indent=4)
 
    del(capture)
    
if __name__=='__main__':
    take_picture2()
