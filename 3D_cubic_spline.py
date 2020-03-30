import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

from mpl_toolkits.mplot3d import Axes3D



x = [104.22, 104.22, 104.22, 104.22, 104.67, 104.67,
     104.67, 104.67, 104.67, 104.67, 104.67, 104.67,
     104.67, 103.32, 102.87, 102.87, 102.87, 102.87,
     101.51, 100.61, 98.81, 97.90, 97.00, 97.00,
     96.55, 96.10, 97.00, 96.65, 96.65, 96.65,
     96.55, 96.55, 96.55, 95.65, 95.65, 95.65]

y = [149.79, 149.79, 149.34, 147.98, 147.53, 147.08,
     145.28, 143.92, 142.57, 142.57, 142.57, 141.67,
     139.41, 138.06, 138.06, 138.06, 136.71, 134.00,
     131.74, 131.74, 131.74, 128.13, 125.88, 124.07,
     124.07, 125.43, 125.88, 124.07, 126.78, 125.43,
     127.68, 135.35, 136.71, 138.96, 140.31, 143.92]



z = [0, 6, 12, 18, 24, 30,
     36, 42, 48, 54, 60, 66,
     72, 78, 84, 90, 96, 102,
     108, 114, 120, 126, 132, 138,
     144, 150, 156, 162, 168, 174,
     180, 186, 192, 198, 204, 210]
print(len(z))

tck, u = interpolate.splprep([x,y,z], s=2)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_fine = np.linspace(0,1,200)
x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)


print(x_fine[10])
fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
ax3d.plot(x_fine, y_fine, z_fine, 'go')
fig2.show()
plt.show()

# import numpy as np
#
# import pydicom
#
# import os
#
# files = "./dicom_dataset/7000004988-20170406"
#
# dcm_store = []
#
# for name in os.listdir(files):
#     dcm_file = pydicom.dcmread(os.path.join(files, name))
#
#     dcm = dcm_file.pixel_array
#
#     dcm_store.append(dcm)
#
# dcm_arr = np.array(dcm_store)
#
# print(dcm_arr[51][270][242])
# print(os.listdir(files))