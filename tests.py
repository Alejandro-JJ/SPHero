import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import colorcet as cc
#self.mycmap = [[0,255,128]]*256 # greenish
mycmap = cc.glasbey_bw_minc_20_minl_30
mycmap[0]=[0,0,0] # add black as first value
my_cmap=LinearSegmentedColormap.from_list('mycmap', mycmap)

"""
Test for finding the cropping limits of a poixel value in a 3D tiff
"""
im = io.imread('./Segmentations/S3_P1_1_original.tif')
#%%
pixel_value = 2
buffer = 10
coords = np.where(im==pixel_value)
lim_z = [np.min(coords[0])-buffer, np.max(coords[0])+buffer]
lim_y = [np.min(coords[1])-buffer, np.max(coords[1])+buffer]
lim_x = [np.min(coords[2])-buffer, np.max(coords[2])+buffer]

crop = im[lim_z[0]:lim_z[1], lim_y[0]:lim_y[1], lim_x[0]:lim_x[1]]

plt.close('all')
plt.imshow(crop[80,:,:], cmap=my_cmap)
io.imsave('Cropped.tiff', crop)

