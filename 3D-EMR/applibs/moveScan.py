import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import numpy as np
import cv2
import cv2.cv as cv

pinS = "P8_13"
pinL = "P8_10"
d_min = 3
d_max = 14.5
d_span = d_max - d_min

PWM.start(pinS, (100-d_min), 60.0, 1)
GPIO.setup(pinL, GPIO.OUT)
GPIO.output(pinL, GPIO.HIGH)

cap = cv2.VideoCapture(0)

print "Fake Read..."
ret, frame = cap.read()
print frame

for i in range(181):
	angle_f = float(i)
	duty = 100 - ((angle_f / 180) * d_span + d_min)
	PWM.set_duty_cycle(pinS, duty)

	ret, frame = cap.read()
	#cv2.imwrite('img-%s.jpg' % i, frame)
    
    imgGray = cv.CreateImageHeader((frame.shape[1], frame.shape[0]), cv.IPL_DEPTH_8U, 3)
    cv.SetData(imgGray, frame.tostring(), frame.dtype.itemsize * 3 * frame.shape[1])
    
    cv.SaveImage('img-gray-%s.jpg' % i, imgGray)

cap.release()

PWM.stop(pinS)
PWM.cleanup()

GPIO.output(pinL, GPIO.LOW)
GPIO.cleanup()
