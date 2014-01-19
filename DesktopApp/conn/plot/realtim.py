import time
import numpy as np
import matplotlib.pyplot as plt


run = True 

readFile= open("sampleData.txt","r") # 'r' read file from the same dir
sepFile = readFile.read().split("\n")
readFile.close() # u have to close the file 



x=[0,0,0,0,0,0,0,1,0.5,1,1,1,1,1.5,2,2.5,3,3.5,4,4,4,4,4,4.5,5,5,5,5,5,5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,0,2,2.5,3,3,3,2.5,2,2,2]
y=[0,0.5,1,1.5,2,2.5,3,3,3,3.5,4,4.5,5,5,5,5,5,5,5,4.5,4,3.5,3,3,3,2.5,2,1.5,1,0.5,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1.5,1,1,1,1.5,2]

z=list()
q=list()


while x:
	z.append(x.pop())
	q.append(y.pop())

plt.ion()
plt.show()

while z:
	x=z.pop()
	y=q.pop()
	plt.scatter(x,y)
	plt.draw()
	time.sleep(0.5)
	
	
while 1	:
	d=1
#time.sleep(100)

