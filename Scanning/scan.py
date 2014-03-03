"""
# Captures a picture and calculates the brightests pixel on each y-axis
# pixel row. Returns the result of the calculation to the user.
"""
import cv2.cv as cv
from math import pi as PI
from math import tan, fabs, asin

class CloudPoint():
    PointData = None
    
    def __init__(self, args=None):
        if not args == None:
            self.PointData = args
    
    def printAttribs(self):
        print self.PointData
        
def findLaserCenterByRow(imgRow, rowWidth):
    THRESHOLD_MIN_PWR = 25
    THRESHOLD_BLOB_DIFF = 10
    THRESHOLD_ALLOWED_BLOB_SZ = 20
    centerPos = 0
    maxPwr = 0
    
    for pos in range(rowWidth):
        if maxPwr < imgRow[pos]:
            centerPos = pos
            maxPwr = imgRow[pos]
    
    if maxPwr < THRESHOLD_MIN_PWR: return -1

    logicPwr, totalPwr = 0.0, 0.0
    for pos in range(centerPos-10,centerPos+11):
        currentPwr = 0.0
        if pos >= 0 and pos < rowWidth:
            currentPwr = imgRow[pos]
        logicPwr += currentPwr
        totalPwr += currentPwr * pos
    
    return totalPwr / logicPwr

def calcDistanceByPos(x, y, imgWidth):
    OFFSET = -0.03460372108
    GAIN = 0.0015772
    pixels_from_center = x - (imgWidth / 2)
    
    distance = 6.1 / tan( pixels_from_center * GAIN * OFFSET )
    
    CENTER_Y = 239
    if not y == CENTER_Y:
        y = fabs(y - CENTER_Y)
        y *= 0.02645833333
        theta = asin(y / distance)
        distance = y / tan( theta )
    
    return distance
        
# Currently only takes a pictures and saves it in output.jpg (NO ERROR HANDLING etc)
def take_picture():
    capture = cv.CaptureFromCAM(0)
    img = cv.QueryFrame(capture)
    
    imgGray = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
    cv.Smooth( imgGray, imgGray, cv.CV_GAUSSIAN, 3, 3 )
    
    cv.SaveImage('output.jpg', img)
    cv.SaveImage('outputG.jpg', imgGray)
    
    cp = CloudPoint({"X":1,"Y":2,"Z":3,"H":4,"Row":5,"Col":6})
    cp.printAttribs()
    
    brightestPoints = []
    for row in range(imgGray.height):
        rowPoints = []
        for col in range(imgGray.width):
            rowPoints.append(imgGray[row, col])
        brightestPoints.append(findLaserCenterByRow(rowPoints, imgGray.width))
    
    distances = []
    for y in range(len(brightestPoints)):
        distances.append(calcDistanceByPos(brightestPoints[y], y, imgGray.width))
        
    for i in range(3):
        print "X:", brightestPoints[i], "Y:", i, "D:", distances[i]
    
if __name__=='__main__':
    take_picture()
    