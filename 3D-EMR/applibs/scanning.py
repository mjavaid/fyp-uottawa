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

def extract_distances():
    print "distances"
    for i in range(20, 181):
        print "Processing... %s" % i
        imgFrame = cv2.imread('Pictures/res-%s.jpg' % i, 0)
        print "test1"
        """imgGray = cv.CreateImageHeader((imgFrame.shape[1], imgFrame.shape[0]), cv.IPL_DEPTH_8U, 3)
        print "test2"
        cv.SetData(imgGray, imgFrame.tostring(), imgFrame.dtype.itemsize * 3 * imgFrame.shape[1])
        print "test3"
        print "---", imgFrame
        print "---", imgGray
        
        openCV2npArr = np.asarray( imgGray[:,:] )"""
        #print "test4", openCV2npArr
        brightestPoints = np.apply_along_axis(findLaserCenterByRow, axis=1, arr=imgFrame)
        print "test5"

        scanOutput = []
        print "test6"
        for y in range(len(brightestPoints)):
            distance, thetaZ = calcDistanceByPos(brightestPoints[y], y, imgGray.width)
            scanOutput.append({
                'x': brightestPoints[y],
                'y': y,
                'distance': distance,
                'thetaZ': thetaZ,
                'thetaX': i
            })
        print "test7"
    
        with open("Output/out-move-%s.txt" % i, "w") as outfile:
            json.dump(scanOutput, outfile, indent=4)

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
        print "Taken %i" % i
        duty = 100 - ((angle_f / 180) * DUTY_SPAN + MIN_DUTY)
        PWM.set_duty_cycle(CAMERA_PIN, duty)

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
    
        cv2.imwrite('Pictures/frame-%s.jpg' % i,frame)
        cv2.imwrite('Pictures/mask-%s.jpg' % i,mask)
        cv2.imwrite('Pictures/res-%s.jpg' % i,res)
        cv2.imwrite('Pictures/outputimg-%s.jpg' % i, res2)
    
    cap.release()
    
    PWM.stop(CAMERA_PIN)
    PWM.cleanup()
    
    GPIO.output(LASER_PIN, GPIO.LOW)
    GPIO.cleanup()
    
    #extract_distances()

if __name__ == "__main__":
    print "scanning.py"
    scan()
    