import matplotlib.pyplot as plt
import numpy as np 

x=[0,0,1,1,4,4,5,5,0,2,3,3,2,2]
y=[0,3,3,5,5,3,3,0,0,2,2,1,1,2]


print "x: ", x 
print "y: ", y 




plt.plot (x,y,'bo') # x and y have to be the same number ,,, b=blue and o=dotes 
plt.axis ([-1,6,-1,6])
plt.title('matplotlib example')
plt.xlabel("x coordnat")
plt.ylabel("y coordnat")


plt.show()
