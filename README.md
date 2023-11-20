# SPHero
In order to use this code you might need to install some necessary python packages like

    PyQt5
    scikit-skimage
    pyclesperanto
    colorcet

This is a Graphical User Interface (GUI) though to be used in combination with MasterSegmenter. SPHero takes labelled pictures as an input, and calculates a decomposition of each particle into spherical harmonics, 
storing the data into .npy python structures. The only required parameter input is the pixel size (in xy and z) of the pictures. 
The software has two main uses:

- Load a labelled picture, and click on the desired particle you want to analyze. A cropped version of the  particle will be shown, as well as a 3D reconstruction of the shape, and the Spherical Harmonic decomposition
  will be saved with an unique name in the origin folder.

- Load a labelled picture and click on "Analyze all". The software will iterate through all the available particles and save all the results in separate .npy tables inside a folder. 

To facilitate the analysis of crowded pictures, some post-processing functions are provided in  "SH_utils.py", to iterate through the previously created folders and present some statistics and plots summarizing the volume distribution and 
the coefficient distribution of the particles.
