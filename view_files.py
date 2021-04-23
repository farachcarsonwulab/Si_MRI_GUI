#!/usr/bin/env python3

import pickle
import matplotlib.pyplot as plt
from multiprocessing import Process
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import os
import glob




def InteractivePlot(grayimg=None,tmpim=None,overall_max=None,overall_nonzero_min=None,StudyName=None,totavg=None,maxValue=None):
    """
    This function displays superimposed H and Si images in interactive matplotlib
    plots. These plots contain scroll bars and radio buttons to allow the user to
    view the images as they see fit.
    """
    fig, ax = plt.subplots(1,1)
    fig.canvas.set_window_title(StudyName)
    plt.subplots_adjust(left=0, bottom=0.25)

    #Display only the H image if the Si image is too dim to view.
    if (overall_max == 0) and (overall_nonzero_min == 0):
        l = ax.imshow(1 - grayimg, cmap='Greys',interpolation='bilinear')


        plt.title(StudyName + ': This Specific Plot is Unalterable - All Values are Zero')
        return None





    l = ax.imshow(grayimg, cmap='Greys',interpolation='bilinear',alpha=1)

    maxval = np.amax(grayimg)
    minval = np.amin(grayimg)

    if overall_nonzero_min !=0:
        Si = ax.imshow(SNRadjust(tmpim,5,totavg, maxValue),cmap='hot',interpolation='bilinear',alpha=0.5,vmin=0,vmax=overall_max)
        fig.colorbar(Si)

    plt.suptitle(StudyName)

    contrast_0 = 1
    delta_contrast = 0.1

    snr_0 = 5
    delta_snr = 0.1


    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axsnr = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

    contrast = Slider(axfreq, 'Contrast', 0.1, 7, valinit=contrast_0, valstep=delta_contrast)
    snr = Slider(axsnr,'SNR',1,10,valinit=snr_0,valstep=delta_snr)



    def update(val):
        """
        This function provides the on the fly interactivity for the matplotlib plot.
        It updates the plot whenever a scroll bar or radio button changes.
        """
        new_contrast = contrast.val
        SNR = snr.val
        img_type = radio.value_selected


        adjusted_tmpim = SNRadjust(tmpim, SNR, totavg, maxValue)

        ax.clear()

        if img_type == 'Both':
            ax.imshow(imadjust(grayimg,maxval,minval,0,1,gamma=new_contrast),cmap='Greys',interpolation='bilinear',alpha=1)
            if overall_nonzero_min !=0:
                Si = ax.imshow(adjusted_tmpim,cmap='hot',interpolation='bilinear',alpha=0.5,vmin=0,vmax=overall_max)


        elif img_type == 'H Only':
            ax.imshow(imadjust(grayimg,maxval,minval,0,1,gamma=new_contrast),cmap='Greys',interpolation='bilinear',alpha=1)

        elif img_type == 'Si Only':
            if overall_nonzero_min !=0:
                Si = ax.imshow(adjusted_tmpim,cmap='hot',interpolation='bilinear',alpha=1,vmin=0,vmax=overall_max)
            else:
                Si = ax.imshow(np.zeros(tmpim.shape),cmap='hot',interpolation='bilinear',alpha=1,vmin=0,vmax=overall_max)



        fig.canvas.draw()

    contrast.on_changed(update)
    snr.on_changed(update)



    rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
    radio = RadioButtons(rax, ('Both', 'H Only', 'Si Only'), active=0)

    radio.on_clicked(update)

    plt.show(block=True)


    return None

def SNRadjust(tmpim, SNR, totavg, maxValue):
    """
    This function calculates the updated image every time the SNR scroll bar changes.
    """
    tmpim_copy = np.copy(tmpim)
    autoTh = totavg * SNR / maxValue
    tmpim_copy[tmpim_copy <= autoTh] = 0

    return tmpim_copy

def imadjust(x,a,b,c,d,gamma=1):
    """
    This function changes brightness/contrast every time the contrast scroll bar changes.
    """
    # Similar to imadjust in MATLAB.
    # Converts an image range from [a,b] to [c,d].
    # The Equation of a line can be used for this transformation:
    #   y=((d-c)/(b-a))*(x-a)+c
    # However, it is better to use a more generalized equation:
    #   y=((x-a)/(b-a))^gamma*(d-c)+c
    # If gamma is equal to 1, then the line equation is used.
    # When gamma is not equal to 1, then the transformation is not linear.
    y = (((x - a) / (b - a)) ** gamma) * (d - c) + c
    return y


def view():
    """
    To be run on the command line: please
    specify (as an argument) the folder containing
    pickle files of processed images.
    """
    try:
        folder_path = sys.argv[1]
    except:
        print(view.__doc__)
        return None
    if not os.path.isdir(folder_path):
        print(view.__doc__)
        return None

    os.chdir(os.path.join(folder_path))

    files = glob.glob('*.pkl')

    if len(files) == 0:
        print('No Pickle Files Found in this Directory!')

    for file in files:

        with open(os.path.join(folder_path,file),'rb') as f:
            grayimg, tmpim, overall_max, overall_nonzero_min, StudyName, totavg, maxValue = pickle.load(f)


        p = Process(target=InteractivePlot,args=(grayimg,tmpim,overall_max,overall_nonzero_min,StudyName,totavg,maxValue,))
        p.start()

    return None

if __name__ == '__main__':
    view()
