import movement as mv
from movement import executeMovement as em
from time import sleep

mv.enable()
sleep(5)
for i in range(3):
	print "FORWARD!", i
	em(["FORWARD", 1])
	sleep(10)

#print "FORWARD AGAIN!"
#em(["FORWARD", 1])
sleep(2)
mv.disable()

