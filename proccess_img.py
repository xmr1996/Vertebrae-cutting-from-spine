import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D

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



######################################################################
# 3D curive from spine

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

#convert cordinates to integer pixel value
x_sample_p = x_sample_c/pix_spacing[0]
x_sample_p = np.round(x_sample_p)
x_sample_p = x_sample_p.astype(int)

y_sample_p = y_sample_c/pix_spacing[1]
y_sample_p = np.round(y_sample_p)
y_sample_p = y_sample_p.astype(int)

z_sample_p = z_sample_c/1.5
z_sample_p = np.round(z_sample_p)
z_sample_p = z_sample_p.astype(int)



intensity= []
for i in range(36):
    intensity.append(data_set[y_sample_p[i]][x_sample_p[i]][z_sample_p[i]])

intensity = np.array(intensity)
print(intensity)


tck, u = interpolate.splprep([x_sample_c,y_sample_c,z_sample_c], s=2)
u_fine = np.linspace(0,1,200)
x_c, y_c, z_c = interpolate.splev(u_fine, tck)




x_p = x_c / pix_spacing[0]
y_p = y_c / pix_spacing[1]
z_p = z_c /1.5

for i in range(10):
    print("cordinates: ", x_c[i], y_c[i], z_c[i])
    print("point ",x_p[i], y_p[i], z_p[i])
print(pix_spacing)





fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
ax3d.plot(x_c, y_c, z_c, 'go')
fig2.show()
plt.show()



# 50 * 50 we want 200*200