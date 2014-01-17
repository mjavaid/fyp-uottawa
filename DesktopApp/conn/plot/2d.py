import matplotlib.pyplot as plt
import numpy as np 
from math import cos, sin, degrees , radians


xo=0
yo=0

def xAy (leng,ang):
	global xo, yo
	
	n=radians(90) 
	o=radians(180)
	t=radians(270)
	th=radians(360)
	
	
	x=0
	y=0
	#if (ang<=n):
	#	 x= leng * cos(ang)
	#	 y= leng * sin(ang)
		 
		 
	if (ang==0 and ang<= o):
		 #ang = o-ang
		 x= leng * cos(ang)
		 y= leng * sin(ang)

	if (ang>o and ang <= th):
		 #ang = t - ang
		 x= leng * sin(ang)
		 y= leng * cos(ang)

	#if (ang>t and ang <= th):
		# ang = th - ang
	#	 x= leng * cos(ang)
	#	 y= leng * sin(ang)
	
	xo+=x 
	yo=yo+y
		 
	
	
if __name__ == "__main__":
	print "xo= ",xo ,"yo= ", yo
	leng = 4
	ang = radians(300)
	 
	xAy(leng,ang)
	print "xo= ",xo ,"yo= ", yo