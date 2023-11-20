#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SH_Utils
Functions to work with the output data from MasterSegmenter and SPHero
"""
import pyshtools as sh
import os
import numpy as np
import matplotlib.pyplot as plt

def ReadSHTable(path):
    """
    Coverts a .npy table to a python array
    It takes the path of the .npy file as input
    """
    if not path.endswith('npy'):
        print('This is not a valid path for a SHTable')
        return
    coeff_array = sh.SHCoeffs.from_file(path, format='npy', normalization='ortho')
    coeff_table = coeff_array.coeffs
    return coeff_table

def Ratio_C00_C20(SHTable):
    """
    Calculates the ratio between the c00
    and the c20 components of spherical harmonics
    from a SHTable array
    """
    c00 = SHTable[0,0,0]
    c20 = SHTable[0,2,0]
    return c20/c00

def VolumeBead(SHTable):
    tabla = sh.SHCoeffs.from_array(SHTable, normalization='ortho')
    tabla4pi = tabla.convert(normalization='4pi')
    volume = tabla4pi.volume()
    return volume

def RatioAllBeads(folderpath, threshold=np.inf,minsize=0, maxsize=1e6, plot=True, limit=np.inf):
    """
    Calculates the C20/C00 ratio for all the SHtables
    inside a folder
    """
    plt.close('all')
    ratios = []
    volumes = []
    outliers = 0
    tables = os.listdir(folderpath)
    
    for table in tables:
        tablepath = os.path.join(folderpath, table)
        coefftable = ReadSHTable(tablepath)      
        # add here filtering condition, dont even save outliers
        if (abs(Ratio_C00_C20(coefftable))<=threshold) and (VolumeBead(coefftable)>minsize) and (VolumeBead(coefftable)<maxsize):    
            ratios.append(abs(Ratio_C00_C20(coefftable)))
            volumes.append(VolumeBead(coefftable))
        else:
            outliers = outliers+1
        if len(ratios)>limit:
            break
        
    
    if plot==True:
        fig, axs = plt.subplots(2,1, figsize=(8,6))
        axs[0].plot(ratios, 'ro', markersize=3)
        axs[0].set_title('c20/c00 ratio')
        axs[0].set_ylim([0,threshold])
        axs[0].set_xlim([0,len(ratios)])
        axs[0].axhspan(0, 0.6, facecolor='green', alpha=0.2)
        axs[0].axhspan(0.6, threshold, facecolor='red', alpha=0.2)
        axs[0].set_ylabel('Slightly deformed             Highly deformed', fontsize=7)
        
        # plot volume
        axs[1].plot(volumes, 'bo',markersize=3)
        axs[1].set_ylabel(r'volume [$\mu m^3$]', fontsize=8)
        axs[1].set_xlim([0,len(volumes)])
        
        avg_ratio = np.mean(ratios)
        avg_volume = np.mean(volumes)
        avg_radius = np.cbrt(avg_volume*3/(4*np.pi))
        axs[0].hlines(avg_ratio, 0, len(ratios), colors='black')
        axs[0].text(3,0.3, f'Avg ratio : {round(avg_ratio, 4)} \n'
           f'Avg volume : {round(avg_volume, 2)} um3 \n' 
           f'Outliers : {outliers} \n'
           f'Avg radius: {round(avg_radius,2)} um')
    
    print(f'Average radius: {avg_radius} um')
    return ratios, volumes