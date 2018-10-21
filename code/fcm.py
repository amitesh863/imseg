# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:52:05 2018

@author: durgesh singh
"""

import numpy as np
from matplotlib import pyplot as plt
from imgrs import get_image 


input_dir = '../data/'
output_dir = '../result/'

def init_membership_mat(pixel_range,cls_range):
    mat = np.random.random((pixel_range,cls_range))
    mat = np.sum(mat,axis=1)
    np.divide()

def fcm(pix_range,count):
    print(init_membership_mat(pix_range.shape[0],2))


arr_img=get_image(input_dir+"cameraman.tif")
count,bins = np.histogram(arr_img,256,[0,256])
fcm(bins,count)



    