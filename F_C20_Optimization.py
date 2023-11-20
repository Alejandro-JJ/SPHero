# C20_rotation
# this function takes an input angles = (rot_x, rot_y) 
# it rotates a BeadSurface.tif with a rotation matrix with the defined angles
# afterwards, returns the component C20 of the expansion in Spherical Harmonics
# This function is to be maximized (or its opposite minimized)
# For its optimization, the function must work with a single argument
# The data used is directly called self.BeadSurface
import scipy.optimize
import numpy as np
#import F_INITIALIZATION
from F_INITIALIZATION import cart2sph, sphereFit, SH2NP, Rotate
import pyshtools as sh

# This function is only used for optimization, and that is why it only has
# one output. For plotting and recovering the SH table, we have another function 
# at the bottom of the script
# This function rotates the bead and outputs the corresponding C20 coeff

def C20_rotation(angles, TIFF, ExpDegree, px, pz):
    rot_x=angles[0]
    rot_y=angles[1]
    
    BeadSurface = TIFF
    
    # The transformations necessary to plot properly the bead
#    x = np.where(BeadSurface==1)[0]
#    y = np.where(BeadSurface==1)[1]
#    z = np.where(BeadSurface==1)[2]
    y=np.where(BeadSurface==1)[0] * pz
    z=-np.where(BeadSurface==1)[1] * px
    x=np.where(BeadSurface==1)[2] * px
      
    # Fit a sphere to the cloud, find center and displace cloud to the origin
    radius,C = sphereFit(x, y, z)
    x_c = C[0]
    y_c = C[1]
    z_c = C[2]
    x = x-x_c
    y = y-y_c
    z = z-z_c
    
    # The Rotate function is written such that rotation is first in X and then in Y
    x_new, y_new, z_new = Rotate (x, y, z, rot_x, rot_y, 0)
    
    # Transform to spherical coordinates, re-format for SHTools
    lat, lon, d = cart2sph(x_new, y_new, z_new)
    lat=np.rad2deg(lat)
    lon=np.rad2deg(lon)
    lat_sh=lon
    lon_sh=lat+180
    d_sh=d
    
    # Expansion with SHTools
    SHExpansion = sh.expand.SHExpandLSQ(d_sh,lat_sh,lon_sh,ExpDegree)
    #residuo = SHExpansion[1]
    coeffs = sh.SHCoeffs.from_array(SHExpansion[0])
    table = coeffs.coeffs
    C20 = table[0,2,0]
    
    # Looking for the minimum value of C20 (squeezed bead)
    # This returns the value as it is, and optimize.minimize with look for the smallest
    return +C20
#=============================================================================#


# C20_rotation_maximization 
    
def C20_optimization(TIFF, ExpDegree, px, pz, rot_y_guess=0, rot_x_guess=0):
    
    guess=np.array([rot_x_guess, rot_y_guess])
    output=scipy.optimize.fmin(C20_rotation, guess, args=(TIFF, ExpDegree, px, pz))
    
    optimal_rot_x=output[0]
    optimal_rot_y=output[1]
    
    print('Optimal rotation for maximum C20 projection')
    print('rot_x= %.2f° ; rot_y= %.2f°' % (optimal_rot_x, optimal_rot_y)) 
    
    return output


#=============================================================================#
# C20 function with more outputs, not used for optimization, but for plotting
# and to extract the rest of the data. Once the optimal rotation has been found
    
# The "angles" will be the output of the optimization part, with the two 
# previous functions
    
def C20_rotation_outputs(angles, TIFF, ExpDegree, Voxel_XY, Voxel_Z):
    
    rot_x, rot_y = angles    
    BeadSurface = TIFF
    
    # The transformations necessary to plot properly the bead
    y=np.where(BeadSurface==1)[0] * Voxel_Z
    z=-np.where(BeadSurface==1)[1]  * Voxel_XY 
    x=np.where(BeadSurface==1)[2] * Voxel_XY 
    

    # From here on, everything is micrometers!!
    
    # Fit a sphere to the cloud, find center and displace cloud to the origin
    radius,C = sphereFit(x, y, z)
    x_c = C[0]
    y_c = C[1]
    z_c = C[2]
    
    # NON-ROTATED COORDINATES
    x = x-x_c
    y = y-y_c
    z = z-z_c
    coord_original = [x, y, z]
    
    # The Rotate function is written such that rotation is first in X and then in Y
    # and it is expressed in degrees
    x_new, y_new, z_new = Rotate (x, y, z, rot_x, rot_y, 0)
    coord = [x_new, y_new, z_new]
        
    
    # Transform to spherical coordinates, re-format for SHTools
    lat, lon, d = cart2sph(x_new, y_new, z_new)
    lat=np.rad2deg(lat)
    lon=np.rad2deg(lon)
    lat_sh=lon
    lon_sh=lat+180
    d_sh=d
    
    
    # Include orthonormalization norm=1=4pi
    SHExpansion=sh.expand.SHExpandLSQ(d_sh,lat_sh,lon_sh,ExpDegree)
    #residuo=SHExpansion[1]
    # I run the algorithm in 4pi normalization, and then transform the 
    # coefficient table to be in orthogonal
    coeffs = sh.SHCoeffs.from_array(SHExpansion[0])
    coeffs_ortho = sh.SHCoeffs.convert(coeffs, normalization='ortho') # works!
    
    table = coeffs_ortho.coeffs
    #C20=table[0,2,0]
 
    # Recover also the coordinates of the expansion
    # In the following functions inside SH2NP
    # the normalization is conserved
    FitCoordinates = SH2NP(coeffs_ortho)
    
#    fig=plt.figure()
#    ax=fig.add_subplot(111, projection='3d')
#    ax.scatter(FitCoordinates[0], FitCoordinates[1], FitCoordinates[2])
    # The minus sign is not necessary anymore
    # Gives me the SH table and the point cloud
    
    return coord, coord_original , table, FitCoordinates

         