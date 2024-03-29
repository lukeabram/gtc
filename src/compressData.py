#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:53:47 2022

@author: luke.abram
"""


# example of preparing the horses and zebra dataset
from os import listdir
from numpy import asarray
from numpy import vstack
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import load_img
from numpy import savez_compressed
 
# load all images in a directory into memory
def load_images(path, size=(256,256)):
    data_list = list()
	# enumerate filenames in directory, assume all are images
    print(listdir(path))
    for filename in listdir(path):
		# load and resize the image
        pixels = load_img(path + filename, target_size=size)
        #convert to numpy array
        pixels = img_to_array(pixels)
		# store
        data_list.append(pixels)
    return asarray(data_list)
 
# dataset path
path = './5x12/'
# load dataset A
dataA1 = load_images(path + 'trainA/')
dataAB = load_images(path + 'testA/')
dataA = vstack((dataA1, dataAB))
print('Loaded dataA: ', dataA.shape)
# load dataset B
dataB1 = load_images(path + 'trainB/')
dataB2 = load_images(path + 'testB/')
dataB = vstack((dataB1, dataB2))
print('Loaded dataB: ', dataB.shape)
# save as compressed numpy array
filename = './60.npz'
savez_compressed(filename, dataA, dataB)
print('Saved dataset: ', filename)