#import matplotlib.pyplot as plt
#import numpy as np
from math import cos, sin, degrees , radians

NO_ERR, INVALID_ARGS = 0, 1

def findNewXAndY(distance, angle, oldX, oldY):
    RAD_180 = radians(180)
    RAD_360 = radians(360)
    
    if (angle == 0 and angle <= RAD_180):
        return (distance * cos(angle), distance * sin(angle), NO_ERR)
    elif (angle > RAD_180 and angle <= RAD_360):
        return (distance * sin(angle), distance * cos(angle), NO_ERR)
    else: return (x, y, INVALID_ARGS)
	
if __name__ == "__main__":
    x, y = 0, 0
    distance = 4
    angle = radians(300)
    
    x, y, ERR = findNewXAndY(distance, angle, x, y)
    print "x:", x, "y:", y, "ERR:", ERR
