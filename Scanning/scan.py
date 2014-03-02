"""
# Captures a picture and calculates the brightests pixel on each y-axis
# pixel row. Returns the result of the calculation to the user.
"""
import cv2.cv as cv
from math import pi as PI

# Currently only takes a pictures and saves it in output.jpg (NO ERROR HANDLING etc)
def take_picture():
    capture = cv.CaptureFromCAM(0)
    img = cv.QueryFrame(capture)
    cv.SaveImage('output.jpg', img)
    
if __name__=='__main__':
    take_picture()
    