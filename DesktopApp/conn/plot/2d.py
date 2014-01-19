import matplotlib.pyplot as plt
import numpy as np 
from math import cos, sin, degrees , radians

INVALID_ARGS = "INVALID_ARGS"

def findNewXAndY(distance, angle):
    RAD_180 = radians(180)
    RAD_360 = radians(360)
    
    if (angle == 0 and angle <= RAD_180):
        x, y = leng * cos(angle), distance * sin(angle)
    elif (angle > RAD_180 and angle <= RAD_360):
        x, y = leng * sin(angle), distance * cos(angle)
    else:
        return INVALID_ARGS
    return (x, y)
	
if __name__ == "__main__":
    x, y = 0, 0
    distance = 4
    angle = radians(300)
    
    x, y = findNewXAndY(distance, angle)
    print "x:", x, "y:", y
