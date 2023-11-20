import warnings
warnings.filterwarnings('ignore')

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from skimage import io
import numpy as np
import pyclesperanto_prototype as cle
from plotcanvas import PlotCanvas
from F_C20_Optimization import C20_optimization, C20_rotation, C20_rotation_outputs
from F_INITIALIZATION import TransparentAxes
from termcolor import colored
import os
import colorcet as cc
import matplotlib.pyplot as plt


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 588)
        MainWindow.setStyleSheet("background-color: rgb(150, 199, 180);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Canvas_1 = PlotCanvas(self.centralwidget)
        self.Canvas_1.setGeometry(QtCore.QRect(30, 10, 400, 400))
        self.Canvas_1.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.Canvas_1.setObjectName("Canvas_1")
        self.Canvas_2 = PlotCanvas(self.centralwidget)
        self.Canvas_2.setGeometry(QtCore.QRect(450, 10, 190, 190))
        self.Canvas_2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.Canvas_2.setObjectName("Canvas_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(80, 460, 101, 81))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_pz = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_pz.setFont(font)
        self.label_pz.setStyleSheet("color: rgb(0,0,0);\n"
"font-weight: bold")
        self.label_pz.setObjectName("label_pz")
        self.gridLayout_2.addWidget(self.label_pz, 1, 0, 1, 1)
        self.INPUT_pxy = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.INPUT_pxy.setStyleSheet("background-color: rgb(255,255,255);")
        self.INPUT_pxy.setObjectName("INPUT_pxy")
        self.gridLayout_2.addWidget(self.INPUT_pxy, 0, 1, 1, 1)
        self.label_pxy = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_pxy.setFont(font)
        self.label_pxy.setStyleSheet("color: rgb(0,0,0);\n"
"font-weight: bold")
        self.label_pxy.setObjectName("label_pxy")
        self.gridLayout_2.addWidget(self.label_pxy, 0, 0, 1, 1)
        self.INPUT_pz = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.INPUT_pz.setStyleSheet("background-color: rgb(255,255,255);")
        self.INPUT_pz.setObjectName("INPUT_pz")
        self.gridLayout_2.addWidget(self.INPUT_pz, 1, 1, 1, 1)
        self.Slider_1 = QtWidgets.QSlider(self.centralwidget)
        self.Slider_1.setGeometry(QtCore.QRect(30, 420, 400, 16))
        self.Slider_1.setStyleSheet("QSlider::handle:horizontal {\n"
"background-color: rgb(135, 203, 203);\n"
"border: 1px solid #5c5c5c;\n"
"width: 10px;\n"
"border-radius: 3px;\n"
"}")
        self.Slider_1.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_1.setObjectName("Slider_1")
        self.BUTTON_AnalyzeBead = QtWidgets.QPushButton(self.centralwidget)
        self.BUTTON_AnalyzeBead.setGeometry(QtCore.QRect(200, 470, 91, 61))
        self.BUTTON_AnalyzeBead.setStyleSheet("color: rgb(255,255,255);\n"
"background-color: rgb(88, 117, 105);\n"
"font-weight: bold\n"
"")
        self.BUTTON_AnalyzeBead.setObjectName("BUTTON_AnalyzeBead")
        self.BUTTON_AnalyzeAll = QtWidgets.QPushButton(self.centralwidget)
        self.BUTTON_AnalyzeAll.setGeometry(QtCore.QRect(310, 470, 91, 61))
        self.BUTTON_AnalyzeAll.setStyleSheet("color: rgb(255,255,255);\n"
"background-color: rgb(88, 117, 105);\n"
"font-weight: bold")
        self.BUTTON_AnalyzeAll.setObjectName("BUTTON_AnalyzeAll")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(490, 500, 118, 23))
        self.progressBar.setStyleSheet("selection-background-color: rgb(88,117,105);\n"
"color:rgb(0,0,0)")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.Canvas_3 = PlotCanvas(self.centralwidget)
        self.Canvas_3.setGeometry(QtCore.QRect(450, 220, 190, 190))
        self.Canvas_3.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.Canvas_3.setObjectName("Canvas_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 460, 141, 20))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 669, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Button_Open = QtWidgets.QAction(MainWindow)
        self.Button_Open.setObjectName("Button_Open")
        self.menuFile.addAction(self.Button_Open)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SPHero"))
        self.label_pz.setText(_translate("MainWindow", "pz (um)"))
        self.INPUT_pxy.setText(_translate("MainWindow", "1"))
        self.label_pxy.setText(_translate("MainWindow", "pxy (um)"))
        self.INPUT_pz.setText(_translate("MainWindow", "1"))
        self.BUTTON_AnalyzeBead.setText(_translate("MainWindow", "Analyze \n"
" BEAD"))
        self.BUTTON_AnalyzeAll.setText(_translate("MainWindow", "Analyze \n"
" ALL"))
        self.label.setText(_translate("MainWindow", "No beads detected"))
        self.menuFile.setTitle(_translate("MainWindow", "File..."))
        self.Button_Open.setText(_translate("MainWindow", "Open TIFF"))
              
        ##############################
        # INITIALIZE GPU
        ##############################
        GPUs = cle.available_device_names()
        cle.select_device(GPUs[0])
        print('-'*60)
        print(colored('The GPU ' + GPUs[0] + ' has been selected for SPHero', 'cyan'))
        print('-'*60)      
        
        ##############################
        # GADGET DISABLING
        ##############################
        self.Slider_1.setEnabled(False)
        self.BUTTON_AnalyzeBead.setEnabled(False)
        self.BUTTON_AnalyzeAll.setEnabled(False)
        
        ##############################
        # BUTTON CONNECTION
        ##############################
        self.Button_Open.triggered.connect(self.OpenDialogTIFF)
        self.Slider_1.valueChanged.connect(self.Explore_ZStack)
        self.BUTTON_AnalyzeBead.clicked.connect(self.AnalyzeBead)
        self.BUTTON_AnalyzeAll.clicked.connect(self.AnalyzeAllBeads)
   
        # custom colormap (same as in MasterSegmenter)       
        from matplotlib.colors import LinearSegmentedColormap
        #self.mycmap = [[0,255,128]]*256 # greenish
        self.mycmap = cc.glasbey_bw_minc_20_minl_30
        self.mycmap[0]=[0,0,0] # add black as first value
        self.my_cmap=LinearSegmentedColormap.from_list('mycmap', self.mycmap)
        
        # Dummy list to keep track of selected bead
        self.clicked_pos=[0,0]        
###############################################################################
        # My functions, in order of usage in the program
###############################################################################
    
# FUNCTION TO OPEN FILE DIALOG AND IMPORT TIFF          	 
    def OpenDialogTIFF(self):
        fileNameTIFF = QFileDialog.getOpenFileName(self, 'Open File', '/media/alejandro/Coding/Test_TIFFS/Pauls_Data/', 
                                                   ('Image Files(*.tiff, *.tif)') )   
        # avoid crash, else pick name
        if fileNameTIFF[0] == '':
            return None
        else:    
            self.fileNameTIFF = fileNameTIFF[0]
            self.FolderName = os.path.dirname(fileNameTIFF[0])
            print(self.fileNameTIFF)
        # load (the slow operation)
        self.LoadedTIFF = io.imread(self.fileNameTIFF)    
        # show first frame
        self.ax_1 = self.Canvas_1.figure.add_subplot(111)
        self.ax_1.imshow(self.LoadedTIFF[0,:,:], cmap=self.my_cmap, interpolation='nearest')
        self.ax_1.axis('off')
        self.Canvas_1.draw()
#        # show frame number
        self.NumberOfLayers = np.shape(self.LoadedTIFF)[0]        
        
        # activate and update range of z slider, segment button
        self.Slider_1.setEnabled(True)
        self.Slider_1.setMinimum(0)
        self.Slider_1.setMaximum(self.NumberOfLayers-1)
        self.BUTTON_AnalyzeBead.setEnabled(True)
        self.BUTTON_AnalyzeAll.setEnabled(True)
        # Echo
        print(colored('Image loaded', 'green'))
        print(colored('Which bead do you want? Click on it!', 'green'))
        # Update number of detected beads
        self.label.setText(str(np.amax(self.LoadedTIFF))+' beads detected')
        # Call the clicker function
        self.Canvas_1.mpl_connect('button_press_event', self.onclick)
         
# EXPLORE Z STACK
    def Explore_ZStack(self):
        self.ZPositionSlider = self.Slider_1.value()
        self.Canvas_1.axes.cla()
        self.ax_1.imshow(self.LoadedTIFF[self.ZPositionSlider, :, :],cmap=self.my_cmap, interpolation='nearest') 
        self.Canvas_1.draw()

# EVENT MANAGER FOR MOUSE CLICK
    def onclick(self, event):
        x, y = int(event.xdata), int(event.ydata)
        self.clicked_pos = [y,x]
        self.my_pixelvalue = self.LoadedTIFF[self.ZPositionSlider, self.clicked_pos[0],self.clicked_pos[1]]
        #print(f'You clicked on a pixel value = {self.my_pixelvalue}')


# FUNCTION TO ANALYZE A SINGLE BEAD
# Can be called in two different fashions to:
        # Analyze one bead and plot result on the GUI
        # Loop through all the beads without plotting
    def AnalyzeAllBeads(self):
        for pixel_value in range(1,np.amax(self.LoadedTIFF)+1):
            try:
                buffer=20
                coords = np.where(self.LoadedTIFF==pixel_value)
                lim_z = [np.min(coords[0])-buffer, np.max(coords[0])+buffer]
                lim_y = [np.min(coords[1])-buffer, np.max(coords[1])+buffer]
                lim_x = [np.min(coords[2])-buffer, np.max(coords[2])+buffer]
                
                # cropped, masked, segmented and binary versions 
                crop = self.LoadedTIFF[lim_z[0]:lim_z[1], lim_y[0]:lim_y[1], lim_x[0]:lim_x[1]]
                masked = crop==pixel_value
                surface = cle.detect_label_edges(masked)
                im_binary = cle.pull(surface).astype(bool)
                
                # Run our c20 maximization algorithm. SH order hard-coded
                SHord = 4            
                px, pz = float(self.INPUT_pxy.text()), float(self.INPUT_pz.text())
                self.OptimalRotation = C20_optimization(im_binary, SHord, px, pz=pz)
                self.Coord, self.Coord_orig, self.SHTable, self.FitCoord = C20_rotation_outputs(self.OptimalRotation, im_binary, 
                                                                                            SHord, px, pz)
                # Export the SH table
                self.FolderSaveName = self.FolderName + '/SH_Analysis_'+os.path.basename(self.fileNameTIFF)[:-4]+'/'
                if not os.path.exists(self.FolderSaveName):
                    os.mkdir(self.FolderSaveName)
                self.ArraySaveName = self.FolderSaveName+'/'+'SH_Array_Bead_'+str(pixel_value).zfill(4)+'.npy'
                np.save(self.ArraySaveName, self.SHTable)
                print(f'Analyzed bead {pixel_value}')
                # Update progress bar
                self.progressBar.setValue(int((pixel_value+1)*100/np.amax(self.LoadedTIFF)))
            except:
                print(colored('Bead too small', 'red'))
                
        print(colored('SEGMENTATION COMPLETE', 'green'))
            
        
    def AnalyzeBead(self):
        # It will take the last pixel value in which one clicked
        if self.my_pixelvalue==0:
            print(colored('You have not clicked on a bead yet!', 'red'))
        else:
            # crop picture to only contain our desired bead
            buffer=20
            coords = np.where(self.LoadedTIFF==self.my_pixelvalue)
            lim_z = [np.min(coords[0])-buffer, np.max(coords[0])+buffer]
            lim_y = [np.min(coords[1])-buffer, np.max(coords[1])+buffer]
            lim_x = [np.min(coords[2])-buffer, np.max(coords[2])+buffer]
            
            # cropped, masked, segmented and binary versions 
            crop = self.LoadedTIFF[lim_z[0]:lim_z[1], lim_y[0]:lim_y[1], lim_x[0]:lim_x[1]]
            masked = crop==self.my_pixelvalue
            surface = cle.detect_label_edges(masked)
            im_binary = cle.pull(surface).astype(bool)
            
            # show central slice
            self.Canvas_2.axes.cla()
            self.ax_2 = self.Canvas_2.figure.add_subplot(111)
            self.ax_2.imshow(surface[int(np.shape(surface)[0]/2),:,:], cmap=self.my_cmap, interpolation='nearest')
            self.ax_2.axis('off')
            self.Canvas_2.draw()
            print(f'You have chosen the bead with pixel value {self.my_pixelvalue}')
            print('Analyzing...\n')
            
            # Run our c20 maximization algorithm
            # Find optimal rotation. SH order hard-coded
            px, pz = float(self.INPUT_pxy.text()), float(self.INPUT_pz.text())
            SHord = 4
            self.OptimalRotation = C20_optimization(im_binary, SHord, px, pz=pz)
            # Use this rotation to run analysis
            self.Coord, self.Coord_orig, self.SHTable, self.FitCoord = C20_rotation_outputs(self.OptimalRotation, im_binary, 
                                                                                        SHord, px, pz)
           
            # plot in 3D, forcing equally scaled plot
            plt.style.use('dark_background')
            self.Canvas_2.axes.cla()
            self.ax_3 = self.Canvas_3.figure.add_subplot(111, projection='3d')
            self.ax_3.set_box_aspect((np.ptp(self.Coord[0]), np.ptp(self.Coord[1]), np.ptp(self.Coord[2])))
            TransparentAxes(self.ax_3)
            self.ax_3.set_xlabel('X axis [μm]', fontsize = 6)
            self.ax_3.set_ylabel('Z axis [μm]', fontsize = 6)   
            self.ax_3.set_zlabel('Y axis [μm]', fontsize = 6)  
            self.ax_3.tick_params(labelsize = 4)

            self.ax_3.scatter(self.FitCoord[0], self.FitCoord[1], self.FitCoord[2], c='orange', marker='*', s=0.5)
            self.Canvas_3.draw()
            
            # Export the SH table
            self.FolderSaveName = self.FolderName + '/SH_Analysis/'
            if not os.path.exists(self.FolderSaveName):
                os.mkdir(self.FolderSaveName)
            
            self.ArraySaveName = self.FolderSaveName+'/'+'SH_Array_Bead_'+str(self.my_pixelvalue).zfill(4)+'.npy'
            np.save(self.ArraySaveName, self.SHTable)
            
            
            
        
            



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
