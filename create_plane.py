'''
This code is to create a plane perpendicular to a given line. It will generate
lines that are perpendicular to the line. If the length of the perpendicular is
less than or equal to a threshold value, it will store the coordinates of the
perpendicular.
Author: Mrinal Kanti Dhar
Formula:
    I will indicate the vector terms using ('). For instance, vector x will be x'
    Let, vector equation of a line is r' = (xs,ys,zs) + t(dx,dy,dz)
    Here,   xs,ys,zs are the coordinates of the starting point
            t = determines how far the point will be. You can set it to any value
            (dx,dy,dz) is the direction vector or the travels from the starting
            point along x,y,z axes respectively.

            If (xe,ye,ze) are the coordinates of the end point of the line, then
            dx = xe-xs, dy = ye-ys, dz = ze-zs

    Equation of the line perpendicular to r' is
            p' = (xs,ys,zs) + s(da,db,dc) ........... (I)
    Here, direction vector, m' = (da,db,dc)
    's' is nothing but like 't'.

    Now two vectors are perpendicular if their dot product is zero
    So, (dx,dy,dz).(da,db,dc) = 0
    => dx.da + dy.db + dz.dc = 0
    => dc = -(dx.da + dy.db)/dz ............ (II)

    Here, dx,dy,dz are known. We will generate random values for da and db.
    Then using equ(II) we will calculate dc so that the dot product is zero.

    Using different combinations of (da,db,dc), we can generate as many perpendicular
    as we want. These perpendicular points will generate a plane.
'''

import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import random

######################## FUNCTIONS ###################################

# Create a function to calculate dc
def third_cord(dx,dy,dz,da,db):
    dc = -(dx*da + dy*db)/dz
    return dc

# Create a function to calculate angle between to vectors
def angle(A,B):
    '''
    Formula:
        A'.B' = |A||B|cos(theta)
        => theta = acos(A'.B'/|A||B|)
        Here, A'.B' = AxBx + AyBy + AzBz
        |A| = sqrt(Ax^2 + Ay^2 + Az^2)
        |B| = sqrt(Bx^2 + By^2 + Bz^2)

    '''
    dotAB = A[0]*B[0] + A[1]*B[1] + A[2]*B[2]       # Dot product of A' and B'
    scA = math.sqrt(A[0]**2 + A[1]**2 + A[2]**2)    # Scalar A
    scB = math.sqrt(B[0]**2 + B[1]**2 + B[2]**2)    # Scalar B
    thetadeg = math.acos(dotAB/(scA*scB))*(180/3.1416)
    return round(thetadeg)

# Create random numbers
def gen_random(ra,rb,rc):
    '''
    random_num_in_range_(a,b) = a + (b-a)*random.uniform
    '''
    random.seed(10)
    m = [[ra + (rb-ra)*random.uniform(0,1), ra + (rb-ra)*random.uniform(0,1)] for i in range(rc)]
    return m

########################## ENDS ##################################
def create_plane(x1,y1,z1,x2,y2,z2):
    no_point = 100  # No. of points you want to generate
    store_xyz = []  # Coordinates of the new perpendicular will be stored
    threshold = 30  # New coordinates will be stored if the length is less than threshold

    # Two coordinates of the given vector
    # x1, y1, z1 = 104.22, 149.79, 0.00
    # x2, y2, z2 =

    # Length across x,y, and z axis
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    vec1 = [dx, dy, dz]  # Travel along x,y,z axes

    ra, rb = -20, 20  # lower limit, upper limit
    m = gen_random(ra, rb, no_point)  # Here m contains da and db. Now we will calculate dc.

    # fig = plt.figure()
    # ax = plt.axes(projection='3d')

    x12, y12, z12 = [x1, x2], [y1, y2], [z1, z2]
    # ax.plot3D(x12, y12, z12, 'r')  # Plot the given line

    s = 1  # scaling factor
    for da, db in m:
        # Calculate dc
        dc = third_cord(dx, dy, dz, da, db)

        # Calculate coordinates of the perpendicular
        x3, y3, z3 = x1 + s * da, y1 + s * db, z1 + s * dc
        dx3, dy3, dz3 = x3 - x1, y3 - y1, z3 - z1
        vec2 = [dx3, dy3, dz3]  # Travel along x,y,z axes

        # Check angle between two vectors
        angleDeg = angle(vec1, vec2)
        # print('Angle between two vectors: {}'.format(angleDeg))

        x13, y13, z13 = [x1, x3], [y1, y3], [z1, z3]

        length = math.sqrt(dx3 ** 2 + dy3 ** 2 + dz3 ** 2)  # Length of the new line

        # Store the coordinates if the length is <= threshold
        if (length <= threshold):
            store_xyz.append([round(x3, 2), round(y3, 2), round(z3, 2)])  # Store new coordinates

        # ax.plot3D(x13, y13, z13)
        # ax.set_xlabel('xlabel')
        # ax.set_ylabel('ylabel')
        # ax.set_zlabel('zlabel')

    # plt.show()

    # print('Stored coordinates are ========================>\n', len(store_xyz))
    return store_xyz


