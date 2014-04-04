import numpy as np
from math import tan, fabs, asin, degrees, cos, radians
import cv2
import cv2.cv as cv
import json

MIN_DUTY = 3
MAX_DUTY = 14.5
DUTY_SPAN = MAX_DUTY - MIN_DUTY
THRESHOLD_MIN_PWR = 25
SCAN_RESOLUTION = 1.125 # 180 / 160
IMG_WIDTH = 640
IMG_HEIGHT = 480
IMG_X_CENTER = (IMG_WIDTH / 2) - 1
IMG_Y_CENTER = (IMG_HEIGHT / 2) - 1
IMG_OFFSET = 20
PIXEL_TO_CM = 0.0264583333

def calcDistanceByPos(x, imgWidth):
    if x < 0: return -1
    OFFSET = -0.02510375038  #-0.5609729362 #-0.03460372108
    GAIN = 0.001135535017 #0.001575387042  #0.014967  #0.0015772
    pfc = fabs(x - (imgWidth / 2))
    distance = 6.1 / tan( pfc * GAIN + OFFSET )
    return abs(distance)

def findLaserCenterByRow(imgRow=None):
    if max(imgRow) < THRESHOLD_MIN_PWR or imgRow == None: return -1
    else: return np.argmax(imgRow)

def extract_distances():
    f = open("scan.xyz", "w")
    for i in range(IMG_OFFSET, 181):
        print "Processing... %s" % i
        imgFrame = cv2.imread('Pictures/res-%s.jpg' % i, 0)
        
        brightestPoints = np.apply_along_axis(findLaserCenterByRow, axis=1, arr=imgFrame)

        scanOutput = []
        for y in range(len(brightestPoints)):
            distance = calcDistanceByPos(brightestPoints[y], IMG_WIDTH)
            scanEntry = {
                'x': brightestPoints[y] - IMG_X_CENTER,
                'y': IMG_Y_CENTER - y,
                'distance': distance,
                'thetaX': (i - IMG_OFFSET) * SCAN_RESOLUTION
            }
            scanOutput.append(scanEntry)
            if not distance < 0 and not distance > 50:
                xVal = cos(radians(scanEntry['thetaX'])) * distance
                xyzVector = str(xVal) + " " + str((float(scanEntry["y"]) * PIXEL_TO_CM)) + " " + str(distance) + "\n"
                f.write(xyzVector)
    
        with open("Output/out-move-%s.txt" % i, "w") as outfile:
            json.dump(scanOutput, outfile, indent=4)
    f.close()

def mask():
    for i in range(181):
        print "Masking... %s" % i
        imgTest = cv2.imread('Pictures/frame-%s.jpg' % i, 0)
        # pfc range for laser
        mask2 = np.zeros(imgTest.shape[:2],np.uint8)
        mask2[0:640,430:570] = 255
        res2 = cv2.bitwise_and(imgTest,imgTest,mask = mask2)
        cv2.imwrite('Pictures/test-%s.jpg' % i,res2)

if __name__ == "__main__":
    print "openCV Methods"
    extract_distances()
    