import matplotlib.pyplot as plt
import numpy as np 

x=[]
y=[]

#if the file not in the dir u have to give the whole dir !
readFile= open("sampleData.txt","r") # 'r' read file from the same dir


sepFile = readFile.read().split("\n")

readFile.close() # u have to close the file 

fig= plt.figure()
rect=fig.patch
rect.set_facecolor('black') # background of the window 


for plotPair in sepFile:
	xAndy = plotPair.split(',')
	x.append(int (xAndy[0])) # append add something to the end
	y.append(int (xAndy[1]))

# grey background of the figure 
ax1 = fig.add_subplot(1,1,1,axisbg='grey') # first 2 num is 1 by 1 and chart # 1 
ax1.plot(x,y,'c', linewidth=3.3)

plt.show()

"""
print "x: ", x 
print "y: ", y 




plt.plot (x,y) # x and y have to be the same number

plt.title('matplotlib example')
plt.xlabel("x coordnat")
plt.ylabel("y coordnat")


plt.show()
"""