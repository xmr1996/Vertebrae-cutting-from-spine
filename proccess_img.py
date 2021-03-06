import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.signal import argrelextrema
from mpl_toolkits.mplot3d import Axes3D
import scipy.io as sio

################### helper function #########################

def cor_to_point(x_c, y_c, z_c):
    return int(round(x_c / pix_spacing[0])),  int(round(y_c / pix_spacing[1])), int(round(z_c / 1.5))

def cor_to_point_np(x, y, z):
    x = x / pix_spacing[0]
    x = np.round(x)
    x = x.astype(int)

    y = y / pix_spacing[1]
    y = np.round(y)
    y = y.astype(int)

    z = z / 1.5
    z = np.round(z)
    z = z.astype(int)

    return x, y, z

###################### read in dicom image #####################

path = "./dicom_dataset/66957141_20170406"

dicom_img = []

for dir_name, sub_dir_list, file_list in os.walk(path):
    for file_name in file_list:
        if ".dcm" in file_name.lower():  # check whether the file's DICOM
            dicom_img.append(os.path.join(dir_name,file_name))

# print(dicom_img)

# Get ref file
ref = pydicom.dcmread(dicom_img[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
pix_dim = (int(ref.Rows), int(ref.Columns), len(dicom_img))
print("The demension of the dicom set is ",pix_dim)
# Load spacing values (in mm)
pix_spacing = (float(ref.PixelSpacing[0]), float(ref.PixelSpacing[1]), float(ref.SliceThickness))
print("The pixel spacing between x, y and z is ", pix_spacing)

data_set = np.zeros(pix_dim, dtype=ref.pixel_array.dtype)

# loop through all the DICOM files
for file in dicom_img:
    # read the file
    ds = pydicom.dcmread(file)
    # store the raw image data
    data_set[:, :, dicom_img.index(file)] = ds.pixel_array

print("max intensity in the dataset ", data_set.max())
print("min intensity in the dataset", data_set.min())
print("data set shape is ", data_set.shape)

############### prepare the sample points ###################

#manually pick smaple point along the Spinal canal
x_sample_c = np.array([104.22, 104.22, 104.22, 104.22, 104.67, 104.67,
     104.67, 104.67, 104.67, 104.67, 104.67, 104.67,
     104.67, 103.32, 102.87, 102.87, 102.87, 102.87,
     101.51, 100.61, 98.81, 97.90, 97.00, 97.00,
     96.55, 96.10, 97.00, 96.65, 96.65, 96.65,
     96.55, 96.55, 96.55, 95.65, 95.65, 95.65])

y_sample_c = np.array([149.79, 149.79, 149.34, 147.98, 147.53, 147.08,
     145.28, 143.92, 142.57, 142.57, 142.57, 141.67,
     139.41, 138.06, 138.06, 138.06, 136.71, 134.00,
     131.74, 131.74, 131.74, 128.13, 125.88, 124.07,
     124.07, 125.43, 125.88, 124.07, 126.78, 125.43,
     127.68, 135.35, 136.71, 138.96, 140.31, 143.92])

z_sample_c = np.array([0, 6, 12, 18, 24, 30,
     36, 42, 48, 54, 60, 66,
     72, 78, 84, 90, 96, 102,
     108, 114, 120, 126, 132, 138,
     144, 150, 156, 162, 168, 174,
     180, 186, 192, 198, 204, 210])

#convert cordinates to integer pixel value for all smaple points
x_sample_p, y_sample_p, z_sample_p = cor_to_point_np(x_sample_c, y_sample_c,z_sample_c)

#Get intensity at the location of smaple points
intensity= []
for i in range(len(z_sample_c)):
    intensity.append(data_set[y_sample_p[i]][x_sample_p[i]][z_sample_p[i]])
intensity = np.array(intensity)


########################## draw the cruve of spine and smaple 200 points on the curve ######

sampling_amount = 200

#use 3D interpolation to draw the cruve and sample 200 points on the curve
tck, u = interpolate.splprep([x_sample_c,y_sample_c,z_sample_c, intensity], s=2)
u_fine = np.linspace(0,1,sampling_amount)
x_c, y_c, z_c, i_c= interpolate.splev(u_fine, tck)

#save the 200 points into txt file
# np.savetxt('test.txt', np.column_stack((np.round(x_c, decimals=2), np.round(y_c, decimals=2), np.round(z_c, decimals=2))),
# #            fmt='%.2f',delimiter=', ')

#convert 200 smaple points from cordinates to points
x_p, y_p, z_p = cor_to_point_np(x_c, y_c, z_c,)

#draw the curve
fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
ax3d.plot(x_c, y_c, z_c, 'go')
fig2.show()
plt.show()


######################plane generation and average graph###########################

from create_plane import create_plane

# get tangent lines and planes that is perpendicular to the tangent lines
average =[]
for i in range(1, sampling_amount - 1 ):
    sum, count  = 0,1
    buffer = create_plane(x_c[i], y_c[i], z_c[i], x_c[i+1], y_c[i+1], z_c[i+1])
    print(len(buffer)) #check how many points on the plane

    #get average intensity of all the point on the plane
    for j in buffer:
        j[0], j[1], j[2] = cor_to_point(j[0], j[1], j[2])
        sum += data_set[j[1]][j[0]][j[2]]
        count +=1
    average.append(sum/count)

#draw the graph of average
plt.plot(average)
plt.show()


#find local minimum of the graph to locate the cutting point
average = np.array(average)
local_min_index = argrelextrema(average, np.less)
print(local_min_index)
local_min = []
for i in local_min_index:
    for j in i:
        buffer = [x_c[j], y_c[j], z_c[j]]
        # print("local minimum at cordinates: ", buffer)
        # print("local minimum at point: ", x_p[j], y_p[j], z_p[j])
        # print("this is from calling the function ", cor_to_point(x_c[j], y_c[j], z_c[j]))
        local_min.append(buffer)

    cutting_point = np.array(i)
    # cutting_point = cutting_point.sort()[:9]
    print(cutting_point)




#testing with writing np array to a dicom set
# test_dataset = data_set[:,:,2:7]
# print(test_dataset.shape)
# sio.savemat("patch.mat", {"patch": test_dataset})
# sio.savemat("whole_data.mat", {"whole_data": data_set})