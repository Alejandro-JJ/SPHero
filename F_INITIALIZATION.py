# INITIALIZATION SCRIPT FOR ALL THE SMALL FUNCTIONS THAT 
# THE BEAD ANALYSIS NEEDS
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyshtools as sh

#============================================================================#
# SIMPLE TRANSFORMATIONS BETWEEN CARTESIAN AND SPHERICAL COORDINATES
def cart2sph(x, y, z):
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(z, hxy)         # Elevation     [-pi/2, +pi/2]
    az = np.arctan2(y, x)           # Azimuth       [-pi, +pi]
    return az, el, r


def sph2cart(az, el, r):
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z

#============================================================================#
# FIT A CLOUD OF POINTS TO A SPHERE; RETURNING ITS RADIUS AND CENTER
def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = np.sqrt(t)

    return radius, C


#============================================================================#
# THREE DIMENSIONAL PLOT OF A CLOUD OF POINTS; 
# Secondary functions help creating a proper dimensioned plot
def SpherePlot(x,y,z):
    fig = plt.figure(figsize=(1,1))
    ax = fig.add_subplot(111, projection='3d')
    #ax.set_aspect('equal')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')   
    ax.set_zlabel('Z axis')  
    
    ax.scatter(x, y, z, c='r', marker='.')   

    #plt.title('Bead surface')
    
#    set_axes_equal(ax)
    plt.show()


def set_axes_radius(ax, origin, radius):
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])
    
def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    set_axes_radius(ax, origin, radius)



#============================================================================#
# ANIMATED SLICE PLOT OF A 3D MATRIX (e.g.)
def StackPlotter(stack):
    import numpy as np
    import matplotlib.pyplot as plt
    
    #stack=BeadCutout
    depth=np.shape(stack)[0]
    max_color=np.amax(stack)
    min_color=np.amin(stack)
    for i in range(0,depth):
        plt.imshow(stack[i,:,:], vmin=min_color, vmax=max_color)
        plt.title('BEAD CUTOUT \n Slice %d out of %d' %(i, depth-1))
        plt.show()
        plt.pause(0.1)
        
        
#============================================================================#
# SH2NP
# This function takes a Spherical Harmonics coefficient table from SHTools
# and it gives you back a 3-column matrix with the cartesian coordinates of
# the volume that they define.
# This allows an easier later manipulation of the data
# Aditionally, it can plot the 3D shape as a cloud of points
# The input is a SHGrid table, just like the internal variable coeff obtained
# after running sh.expand.SHExpandLSQ(d,lat,lon,lmax)

def SH2NP(coefficient_table):

    grid=coefficient_table.expand() # Evaluation in grid
    np_grid=grid.to_array()
    
    latitudes=grid.lats()   # [-90°, 90°]
    longitudes=grid.lons()  # [ 0°, 360°]
    N_lats=np.size(latitudes)
    N_lons=np.size(longitudes)
    
    a_latitudes=np.repeat(latitudes, N_lons)    # [-90°, 90°]
    a_longitudes=np.tile(longitudes, N_lats)    # [ 0°, 360°]
    a_radius=np.ndarray.flatten(np_grid) 
    spher_coord=np.vstack((a_latitudes, a_longitudes, a_radius))
    
    # Back to cartessian coordinates and plot
#    r_offset=0
    x,y,z=sph2cart(np.radians(a_longitudes-180), np.radians(a_latitudes), a_radius)#+r_offset)
#    SpherePlot(x,y,z)
#    plt.title('Spherical Harmonics expansion')
    
    return x,y,z

#============================================================================#
# Rotate a set of (x,y,z) cartesian coordinates around the origin
# The proper input are vertical arrays for the coordinates
# The rotation angles will be given in degrees
# The order of the rotation series is defined as X, then Y, then Z
from scipy.spatial.transform import Rotation as R

def Rotate(x,y,z,rot_x,rot_y,rot_z):
    
    x=x.reshape(np.size(x),1)    
    y=y.reshape(np.size(y),1)
    z=z.reshape(np.size(z),1)
    
    coord=np.concatenate((x,y,z), axis=1)
    rotation=R.from_euler('xyz', [rot_x,rot_y,rot_z], degrees='True')
    coord_rot=rotation.apply(coord)

    x_rot=coord_rot[:,0]
    x_rot=x_rot.reshape(np.size(x_rot),1)
    
    y_rot=coord_rot[:,1]
    y_rot=y_rot.reshape(np.size(y_rot),1)

    z_rot=coord_rot[:,2]
    z_rot=z_rot.reshape(np.size(z_rot),1)
    
    return x_rot, y_rot, z_rot
    
def RotateForceLine(x,y,z,rot_x,rot_y,rot_z):
    
    x=x.reshape(np.size(x),1)    
    y=y.reshape(np.size(y),1)
    z=z.reshape(np.size(z),1)
    
    coord=np.concatenate((x,y,z), axis=1)
    rotation=R.from_euler('yxz', [rot_x,rot_y,rot_z], degrees='True')
    coord_rot=rotation.apply(coord)

    x_rot=coord_rot[:,0]
    x_rot=x_rot.reshape(np.size(x_rot),1)
    
    y_rot=coord_rot[:,1]
    y_rot=y_rot.reshape(np.size(y_rot),1)

    z_rot=coord_rot[:,2]
    z_rot=z_rot.reshape(np.size(z_rot),1)
    
    return x_rot, y_rot, z_rot  


def TransparentAxes(ax):
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        