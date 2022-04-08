# read_light_field

R. Sharma, S. Perry, and E. Cheng, "Noise-Resilient Depth Estimation for Light Field Images Using Focal Stack and FFT Analysis," Sensors, vol. 22, no. 5, p. 1993, 2022.

Light field refocusing algorithm that can generated focal stack with slope difference of 0.01

# imports
import os
import numpy as np
from matplotlib import pyplot as plt
import imageio
import cv2

#run
Debag
Execute Project in python interactive

var = Light_field_refocus  %initialise Light_field_refocus

var.get_loc()              % run to give folder location containing individual sub-aperture .png files
                           % you might need to check sub-aperture image names and
                           % the code will give an error if other .png files are in the same folder as the sub-aperture image folder
                           % the light field has to have the same angular resolution in both hor and vertical direction else code will throw error
                           
var.refocus(slope)         % this will generate and save the refocused image project folder  
                           % slope is the disparity value you need to refocus at. 
                           
var.sub_view()             % creates a image with all sub-aperture images put together

var.central_view()         % creates the central view according to the number of sub-aperture image


 
