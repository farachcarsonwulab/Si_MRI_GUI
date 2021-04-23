#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
from datetime import datetime

from GUI_Window import Ui_MainWindow

import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import os
import re
import pandas as pd
import platform
from view_files import InteractivePlot


def get_H_image(filepath,Study,MatSizeX, MatSizeY, ReMatX, ReMatY, NoSlices,ScanNoSetLenH,ScanNoSetH,SliceNoSetH,ProcNo):
    """
    This function grabs an anatomical H-MRI image. It processes the raw image data
    and resizes the image for viewing. The chosen H-MRI image is a single slice
    from a specific scan No.
    """

    #These values are left over from old versions of the code. The variable
    #reassignments have no meaning other than renaming values.
    ScanNo = ScanNoSetH
    SliceNo = SliceNoSetH

    #This if/else branch prevents a previously broken study from being examined.
    if Study == '120522.Q22':
        return "Broken"

    else:
        #Grab the raw image in binary form
        f = open(os.path.join(filepath,Study,str(ScanNo),'pdata',str(ProcNo),'2dseq'), 'r')
        img_raw = np.fromfile(f, dtype=np.int16)


        img_raw = np.reshape(img_raw,(MatSizeX, MatSizeY,NoSlices),order='F') #wow! need to do fortran reshape to mimic matlab
        img_proc = img_raw[:,:,SliceNo - 1].T

        #Equivalent of mat2gray (just normalizing values to between 0 and 1)
        #Since img_proc starts as an array with all positive values, this
        #simple fix works
        img_proc = img_proc / np.amax(img_proc)


        #Reshape using the pillow library
        img_proc = Image.fromarray(img_proc,mode=None)
        img_proc = img_proc.resize((ReMatX,ReMatY),resample=Image.BILINEAR)

        #Return to numpy after resizing
        img_proc = np.asarray(img_proc)

        #Making front-end variable naming consisent by returning a "proton img"
        img_1H = np.copy(img_proc)


    return img_1H

def get_Si_image(filepath,Study,MatSizeX,MatSizeY,ReMatX, ReMatY, ScanNoSetLenSi,ScanNoSetSi,ProcNo):
    """
    This function grabs an Si-MRI image. It processes the raw image data
    and resizes the image for viewing. An important function of this code is to
    interactively crop the Si image. The chosen Si-MRI image is a single slice
    from a specific scan No.
    """

    #This for loop isn't actually needed! It is a remnant of previous versions.
    #The loop is left intentionally for consistency with these old versions.
    for idx in range(0,ScanNoSetLenSi):

        #Variable reassignment purely for renaming purposes.
        ScanNo = ScanNoSetSi

        #Read the raw image in as binary.
        f = open(os.path.join(filepath,Study,str(ScanNo),'pdata',str(ProcNo),'2dseq'),'r')
        img_raw = np.fromfile(f, dtype=np.int16)

        img_raw = np.reshape(img_raw, (MatSizeX, MatSizeY),order ='F')

        img_raw = img_raw.T
        img_proc = img_raw

        #######################################################################
        #The following lines perform the interactive cropping function. This is
        #achieved through interactive matplotlib plots that accept mouse click
        #inputs

        #Display Image with instruction title
        fig, ax = plt.subplots(1,1)
        plt.title('Crop = Hourglass, Startover = Home -- Close Window When Finished')
        ax.imshow(img_proc)


        def tellme(s):
            """
            A small helper function that quickly changes the matplotlib title to
            update user instructions.
            """
            print(s)
            plt.title(s, fontsize=16)
            plt.draw()

        tellme('You will define a Quadrangle, click to begin')

        plt.waitforbuttonpress()

        while True:
            pts = []
            while len(pts) < 4:
                tellme('Select 4 corners with mouse')
                pts = np.asarray(plt.ginput(4))
                if len(pts) < 4:
                    tellme('Too few points, starting over')
                    time.sleep(1)  # Wait a second

            ph = plt.fill(pts[:, 0], pts[:, 1], 'r', lw=2)

            tellme('Happy? Key click for yes, mouse click for no')

            if plt.waitforbuttonpress():
                break

            # Get rid of fill
            for p in ph:
                p.remove()


        plt.close()

        def QuadrangleCorners(pts):
            xlim = [np.min(pts[:,0]),np.max(pts[:,0])]
            ylim = [np.max(pts[:,1]),np.min(pts[:,1])]
            #print(xlim,ylim)
            return (xlim,ylim)





        xlim, ylim = QuadrangleCorners(pts)

        croprect = np.ceil(np.array([xlim[0],ylim[1],xlim[1],ylim[0]])).astype(np.int16)
        #######################################################################
        #These lines help estimate the noise within the Si Image. We look at the
        #average signal value in the empty corners of the image. From these values,
        #we determine thresholding values for the image. For usability, the final
        #image display allows users to change the noise estimation on the fly.
        regsize = 32
        #SNR = 5
        avgreg1 = img_raw[:regsize,:regsize]
        avgreg2 = img_raw[-regsize:,-regsize:]
        avgreg3 = img_raw[:regsize,-regsize:]
        avgreg4 = img_raw[-regsize:,:regsize]

        totavg = np.mean(avgreg1 + avgreg2 + avgreg3 + avgreg4) / 4

        #Setting values outside cropped area to 0
        tmp = np.zeros(img_proc.shape)
        tmp[croprect[1]:croprect[3],croprect[0]:croprect[2]] = 1
        img_proc = img_proc * tmp #python does not use .* for elementwise mult.

        maxValue = np.amax(img_proc)
        #autoTh = totavg * SNR / maxValue

        #Equivalent of mat2gray again
        #(see a description of why this works in 1H)
        img_proc = img_proc / np.amax(img_proc)
        #img_proc[img_proc <= autoTh] = 0

        #Reshape again using the pillow library
        img_proc = Image.fromarray(img_proc,mode=None)
        img_proc = img_proc.resize((ReMatX,ReMatY),resample=Image.BILINEAR)

        #Return to numpy after resizing
        img_proc = np.asarray(img_proc)

        #I just save under this variable name to make the front-
        #end variable calls consistent
        img_29Si = np.copy(img_proc)


    return (img_29Si, totavg, maxValue)


def FrontEnd(folderpath,list_1H, list_29Si,StudyNames,normFacts,normFlag,savepath,totavg, maxValue):
    """
    This function saves and displays all images for a specific session. It grabs all
    saved pkl files saved within the BackEnd script, loads them, and displays them
    as separate processes using the view_files.py script.
    """

    #The following lines allow for the images to be enhaced with additional
    #normalization factors called "normFacts". These factors can be specified
    #in the program's Excel file.
    img_shape = list_1H[0].shape

    N = len(list_1H)

    procSi = np.zeros((img_shape[0],img_shape[1],N))
    procH = np.zeros((img_shape[0],img_shape[1],N))

    for k in range(0,N):
        if normFlag:
            procSi[:,:,k] = list_29Si[k] / normFacts[k]
            procH[:,:,k] = list_1H[k]
        else:
            procSi[:,:,k] = list_29Si[k]
            procH[:,:,k] = list_1H[k]




    #This is where I do scaling for the Silicon Images...
    #My method is as follows:
    #1. Calculate minimum nonzero value over all images being compared (the "overall_nonzero_min")
    #2. Scale every image according to this value (ie multiply every image by overall_nonzero_min/given_min
    #3. return the scaled image. Now, the nonzero minimum for every image will be the overall_nonzero_min.
    #I don't worry about clipping because I'm always multiplying by a ratio <1.
    try:
        overall_nonzero_min = np.amin(procSi[procSi > 0])
    except:
        overall_nonzero_min = 0

    for k in range(0,N):
        image = procSi[:,:,k]
        try:
            image_nonzero_min = np.amin(image[image > 0])
        except:
            image_nonzero_min = float('inf')
        procSi[:,:,k] = image * overall_nonzero_min / image_nonzero_min

    overall_max = np.amax(procSi)

    #Create a timestamped folder and save each image for viewing.
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(os.path.join(savepath,timestamp))




    for k in range(0,N):

        grayimg = procH[:,:,k]
        tmpim = procSi[:,:,k]


        with open(os.path.join(savepath,timestamp,StudyNames[k]+'.pkl'),'wb') as f:
            pickle.dump([grayimg, tmpim, overall_max, overall_nonzero_min, StudyNames[k], totavg, maxValue],f)

    #Display images using the view_files.py script. I've included functionality
    #for both Linux (including Mac OS) and Windows functionality. When starting
    #a releasing process through the terminal, the Linux and Windows commands differ
    #slightly.
    if platform.system() == 'Linux':
        try: #the "&" symbol allows the terminal to release the process
            os.system('python3 view_files.py ' + os.path.join(savepath,timestamp) + ' & ')
        except:
            os.system('python view_files.py ' + os.path.join(savepath,timestamp) + ' & ')

    elif platform.system() == 'Windows':
        try: #the "/B" symbol allows the terminal to release the process
            os.system('start /B python view_files.py ' + '"' + os.path.abspath(savepath + '\\' + timestamp) + '"')
        except:
            os.system('start /B python3 view_files.py ' + '"' + os.path.abspath(savepath + '\\' + timestamp) + '"')
    else:
        try:
            os.system('python3 view_files.py ' + os.path.join(savepath,timestamp) + ' & ')
        except:
            os.system('python view_files.py ' + os.path.join(savepath,timestamp) + ' & ')

    return os.path.join(savepath,timestamp)






def BackEnd(filepath,StudyName, HScanNo, HSliceNo, SiScanNo):
    """
    The BackEnd script grabs the H and Si images specified by the Excel file.
    """

    #Again, variable reassignment purely for renaming purposes.
    Study = StudyName

    ####################################################
    #This portion of the code grabs the 1H image.

    #Input size from raw data
    MatSizeX = 256
    MatSizeY = 256

    ReMatX = 256
    ReMatY = 256

    ScanNoSetH = HScanNo
    ScanNoSetLenH = 1
    SliceNoSetH = HSliceNo


    #No of slices acquired for each Hydrogen scan
    NoSlices = 22
    ProcNo = 1

    #Call the get_H_image func...
    img_1H = get_H_image(filepath,Study,MatSizeX, MatSizeY, ReMatX, ReMatY, NoSlices,ScanNoSetLenH,ScanNoSetH,SliceNoSetH,ProcNo)
    ####################################################
    #This portion of the code grabs the 29Si image.

    MatSizeX = 128
    MatSizeY = 128

    ReMatX = 256
    ReMatY = 256


    ScanNoSetSi = SiScanNo
    ScanNoSetLenSi = 1 #Remnant from old code; the lenght is always 1 now.
    ProcNo = 2

    #Call the get_Si_image func
    img_29Si, totavg, maxValue = get_Si_image(filepath,Study,MatSizeX,MatSizeY,ReMatX, ReMatY, ScanNoSetLenSi,ScanNoSetSi,ProcNo)



    return (img_1H,img_29Si,totavg,maxValue)


def RunBackEnd(filepath,StudyNames, HScanNos, HSliceNos, SiScanNos):
    """
    This function acts as an intermediate between the GUI and the BackEnd function.
    Essentially, it passes and calls the BackEnd function for every image specified
    by the Excel file.
    """
    list_1H = []
    list_29Si = []

    for StudyName, HScanNo, HSliceNo, SiScanNo in zip(StudyNames,HScanNos, HSliceNos, SiScanNos):
        img_1H, img_29Si, totavg, maxValue = BackEnd(filepath,StudyName= StudyName, HScanNo = HScanNo, HSliceNo = HSliceNo,SiScanNo=SiScanNo)

        list_1H.append(img_1H)
        list_29Si.append(img_29Si)

    return ((list_1H,list_29Si),totavg, maxValue)


def RunFrontEnd(folderpath,img_tuple,StudyNames,normFacts,normFlag,savepath, totavg, maxValue):
    """
    This function acts as an intermediate between the GUI and the FrontEnd function.
    Essentially, it passes and calls the FrontEnd function for every image specified
    by the Excel file.
    """
    timestamp_folder = FrontEnd(folderpath,img_tuple[0],img_tuple[1], StudyNames,normFacts,normFlag = normFlag,savepath = savepath,totavg = totavg, maxValue = maxValue)
    return timestamp_folder





































class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    This class creates the GUI created by PyQt. It reads the contents of the user
    specified Excel file and pushes its data to the FrontEnd/BackEnd functions.
    Furthermore, this function includes failsafe functionality. It can account
    for errors made by the users.
    """
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

    #Function to choose the data folder interactively
    def browse_folder(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder:', '', QtWidgets.QFileDialog.ShowDirsOnly)
        self.folder_label.setText(self.folderpath)

    #Function to choose the Excel file interactively
    def browse_file(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Excel Files (*.xlsx *.xls)")
        self.file_label.setText(re.split('/',self.filepath[0])[-1])

    #Function to grab contents of the Excel file. Includes failsafe functionality
    #in case the user made an incorrect choice.
    def Process(self):
        try:
            file_contents = pd.read_excel(self.filepath[0])
            StudyNames = list(file_contents.iloc[:,0])
            HScanNos = list(file_contents.iloc[:,1])
            HScanNos = [int(elem) for elem in HScanNos]
            HSliceNos = list(file_contents.iloc[:,2])
            HSliceNos = [int(elem) for elem in HSliceNos]
            SiScanNos = list(file_contents.iloc[:,3])
            SiScanNos = [int(elem) for elem in SiScanNos]
            normFacts = list(file_contents.iloc[:,4])
            normFacts = [float(elem) for elem in normFacts]
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle('Excel Error')
            msg.setText('Failed Reading Excel File - Refer to Docs for Formatting')
            msg.exec_()
            return None


        try:
            img_tuple, totavg, maxValue = RunBackEnd(self.folderpath, StudyNames = StudyNames, HScanNos = HScanNos, HSliceNos = HSliceNos, SiScanNos = SiScanNos)
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle('Processing Error')
            msg.setText('Error in processing. See details below.')
            if type(e) == FileNotFoundError:
                msg.setDetailedText("Couldn't find a file. Make sure you choose the correct folder")
            elif type(e) == AttributeError:
                msg.setDetailedText("No Data Folder Chosen\nExact Error is:\n" + str(e))
            else:
                msg.setDetailedText("Unknown error occured\nExact Error is:\n" + str(e))
            msg.exec_()
            return None



        save_msg = QtWidgets.QMessageBox()
        save_msg.setIcon(QtWidgets.QMessageBox.Information)
        save_msg.setWindowTitle('Choose Save Folder')
        save_msg.setText("Image Processing Complete. Now, you need to choose where to save your images. Press OK to continue.")

        save_msg.exec_()
        savepath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder to save in:', '', QtWidgets.QFileDialog.ShowDirsOnly)

        if savepath == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle('Processing Error')
            msg.setText('Processing Error. See details below.')
            msg.setDetailedText("No Save Folder Chosen!")
            msg.exec_()
            return None



        try:
            timestamp_folder = RunFrontEnd(self.folderpath,img_tuple, StudyNames = StudyNames,normFacts = normFacts,normFlag = self.NormFactors.isChecked(),savepath = savepath, totavg = totavg, maxValue = maxValue)
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle('Processing Error')
            msg.setText('Processing Error. See details below.')
            msg.setDetailedText("Unknown error occured\nExact Error is:\n" + str(e))
            msg.exec_()
            return None


        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle('Processing Complete')
        msg.setText("Your files were successfully saved to a timestamped folder! To continue, press okay to close the application.")

        text = 'Save Folder:\n'
        text = text + timestamp_folder + '\n\n'

        text = text + 'Files Created:\n'
        for study in StudyNames:
            text = text + study + '.pkl\n'
        msg.setDetailedText(text)

        msg.buttonClicked.connect(self.close)

        msg.exec_()


        return None

#Generate the app
def appExec():
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


def main():
    sys.exit(appExec())

main()
