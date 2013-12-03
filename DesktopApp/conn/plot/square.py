import matplotlib.pyplot as plt
import numpy as np 

x=[0,0,0,0,0,0,0,1,0.5,1,1,1,1,1.5,2,2.5,3,3.5,4,4,4,4,4,4.5,5,5,5,5,5,5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,0,2,2.5,3,3,3,2.5,2,2,2]
y=[0,0.5,1,1.5,2,2.5,3,3,3,3.5,4,4.5,5,5,5,5,5,5,5,4.5,4,3.5,3,3,3,2.5,2,1.5,1,0.5,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1.5,1,1,1,1.5,2]

print "x: ", x 
print "y: ", y 




plt.plot (x,y,'bo') # x and y have to be the same number ,,, b=blue and o=dotes 
plt.axis ([-1,6,-1,6])
plt.title('matplotlib example')
plt.xlabel("x coordnat")
plt.ylabel("y coordnat")

plt.show()


z=[1,2,3,4,5]
j=[1,2,3,4,5]
plt.scatter(z,j,'ro')

