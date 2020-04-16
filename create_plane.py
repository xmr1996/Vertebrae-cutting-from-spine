'''
This code is to create a perpendicular to a given line
Author: Mrinal Kanti Dhar
'''

import numpy as np
import matplotlib.pyplot as plt
import math

def perpendicular(x1, y1, x2, y2):
    '''
    This function creates a perpendicular to a given line.
    input parameter:
        x1, y1, x2, y2 --> co-ordinates of the given line
    output parameter:
        xnew, ynew --> co-ordinates of the new point
        rnew --> length of the new line
    '''

    def cal_cord(x1, y1, r1, thetaRad):
        '''
        This function is used to calculate the co-ordinates of a point which is 
        perpendicular of a given line. 
        input parameter:
            x1, y1 --> co-ordinates of a given point
            r --> hypotenuse
            thetaRad --> theta in radian
        output:
            x2, y2 --> co-ordinates of the new point
        '''
        dx = r1*math.cos(thetaRad)
        x2 = x1 + dx
        dy = r1*math.sin(thetaRad)
        y2 = y1 + dy
        r2 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        return x2, y2, r2
        
    # Calculate slopes 
    m1 = (y2-y1)/(x2-x1)    # slope of the first line
    m2 = -1/m1              # slope of the 2nd line
    
    r1 = np.sqrt((x1-x2)**2 + (y1-y2)**2)   # length of the given line
    
    # Check if the angle between two lines is 90 degree or not
    angle1 = math.atan(m1)*180/3.1416   # angle for the first line
    angle2 = math.atan(m2)*180/3.1416   # angle for the 2nd line
    diff = angle2 - angle1              # diff betn two angles
    
    print('Theta1: {:.3f}, Theta2: {:.3f}, diff: {:.3f}'.format(angle1, angle2, diff))
     
    xnew, ynew, rnew = cal_cord(x1, y1, r1, math.atan(m2))
    
    plt.figure()
    plt.plot([x1,x2], [y1,y2])
    plt.plot([x1,xnew], [y1,ynew])
    plt.show()
    
    return xnew, ynew, rnew

# xnew, ynew, rnew = perpendicular(10, 15, -17, 90)
# print('x-cord: {:,.3f}, y-cord{:,.3f}, length: {:,.3f}'.format(xnew, ynew, rnew))