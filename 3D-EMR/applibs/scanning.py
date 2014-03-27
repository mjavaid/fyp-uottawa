import numpy as np
from math import tan, fabs, asin, degrees
import cv2
import cv2.cv as cv
import json

MIN_DUTY = 3
MAX_DUTY = 14.5
DUTY_SPAN = MAX_DUTY - MIN_DUTY
THRESHOLD_MIN_PWR = 25

def calcDistanceByPos(x, y, imgWidth):
    OFFSET = -1.554904 #-0.03460372108
    GAIN = 0.014967  #0.0015772
    pfc = fabs(x - (imgWidth / 2))
    
    distance = 6.1 / tan( pfc * GAIN + OFFSET )
    
    CENTER_Y, thetaZ = 239, 0
    if not y == CENTER_Y:
        y = fabs(y - CENTER_Y)
        y *= 0.02645833333
        if distance > y:
            thetaZ = degrees(asin(y / distance))
            distance = y / tan( thetaZ )
        else:
            thetaZ = -1
    
    return distance, thetaZ

def findLaserCenterByRow(imgRow=None):
    if max(imgRow) < THRESHOLD_MIN_PWR or imgRow == None: return -1
    else: return np.argmax(imgRow)

def scan():
    import Adafruit_BBIO.PWM as PWM
    import Adafruit_BBIO.GPIO as GPIO
    
    CAMERA_PIN = "P8_13"
    LASER_PIN = "P8_10"
    
    PWM.start(CAMERA_PIN, (100-MIN_DUTY), 60.0, 1)
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.output(LASER_PIN, GPIO.HIGH)
    
    cap = cv2.VideoCapture(-1)
    ret, frame = cap.read()
    
    for i in range(181):
        angle_f = float(i)
        duty = 100 - ((angle_f / 180) * DUTY_SPAN + MIN_DUTY)
        PWM.set_duty_cycle(CAMERA_PIN, duty)

        ret, frame = cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        img = cv.CreateImageHeader((frame.shape[1], frame.shape[0]), cv.IPL_DEPTH_8U, 3)
        cv.SetData(img, frame.tostring(), frame.dtype.itemsize * 3 * frame.shape[1])
        
        imgGray = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
        
        cv2.imwrite('img-Gray-%s.jpg' % i, grayFrame)
        cv.SaveImage("img-Image-%s.jpg" % i, imgGray)
        
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
                'thetaX': i
            })
        
        with open("out-move-%s.txt" % i, "w") as outfile:
            json.dump(scanOutput, outfile, indent=4)
    
    cap.release()
    
    PWM.stop(CAMERA_PIN)
    PWM.cleanup()
    
    GPIO.output(LASER_PIN, GPIO.LOW)
    GPIO.cleanup()  

if __name__ == "__main__":
    print "scanning.py"
    scan()
    