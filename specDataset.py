#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:03:14 2022

@author: luke.abram
"""

# import matplotlib.pyplot as plt
from matplotlib import image
import librosa
from scipy.io import wavfile
from scipy import signal
# from scipy import signal
import numpy as np
from PIL import Image
import unittest

# sample_rate, samples = wavfile.read('sinewavslower.wav')
# frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
# plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), shading='auto')
# plt.title('Audio to Spec Image')
# # plt.ylabel('Frequency [Hz]')
# # plt.xlabel('Time [sec]')
# plt.axis('off')

# plt.xlim(0,times.max())
# plt.show()


# plt.savefig('spec.png', format='png',bbox_inches='tight', pad_inches=0)

class audioSpecs:
    def makeSpec(self, fn, folder):
        # Load audio file as 1D array
        sig2, fs = librosa.load(fn, sr=44100)
        
        # Create spectrogram from 1D array
        spec = librosa.stft(sig2)
        
        hexspec = np.empty((len(spec), len(spec[0]) * 2, 3), dtype='uint8')
        for i in range(len(spec)):
            for j in range(len(spec[0])):
                #Negative indicators
                s = 0
                s2 = 0
                            
        
                #Scaling normal and "complex" components
                n = spec[i, j].real * 382
                c = spec[i, j].imag * 382

                
                
                #Set negative indicators
                if n < 0:
                    s = 1
                
                if c < 0:
                    s2 = 1
                    
                    
                #Take the absolute value and cast components to ints
                n = int(abs(n))
                c = int(abs(c))
                
                #n shifting
                
                hexspec[i, 2 * j, 0] = n & 0xFF
                n = n >> 8
                hexspec[i, 2 * j, 1] = n & 0xFF
                n = n >> 8
                hexspec[i, 2 * j, 2] = s
          
                
                
                #c shifting
                
                hexspec[i, 2 * j + 1, 0] = c & 0xFF
                c = c >> 8
                hexspec[i, 2 * j + 1, 1] = c & 0xFF
                c = c >> 8
                hexspec[i, 2 * j + 1, 2] = s2
                

             
                # print(hexspec[i,j,0])
        print(hexspec[:,:,0].max())
        print(hexspec[:,:,1].max())
        print(np.shape(hexspec))
        
        
        #Slice spectrogram into squares of row length * row length
        for i in range(int(len(hexspec[0]) / len(hexspec))):
            
           
            arr = hexspec[:256, i * 256: (i + 1)* 256, :]
            img = Image.fromarray(arr)
            img.save('./' + folder + '/' + str(i) + '.png')
            print('made ' + folder + '/'+ str(i)+'.png')
            # if count > 0:
            #     break
    
    def storePhase(self, spec, fn):
        phase = np.empty((len(spec), len(spec[0])))
        for i in range(len(spec)):
            for j in range(len(spec[0])):
                if spec[i, j].real < 0:
                    phase[i, j] = 10
                if spec[i, j].imag < 0:
                    phase[i, j] += 1
        np.savetxt(fn, phase)
                
    def imageToAudio(self, outputfn, folder, index):
        #Open image as array
        spec2 = np.array(Image.open('./' + folder + '/' + str(index) + '.png'))
        # spec2 = np.vstack((spec2, np.zeros((768,256,3),dtype=int)))
        
        #Create an empty array the same size as the image
        spec = np.empty((len(spec2), int((len(spec2[0]) - 1) / 2)), dtype='complex64')
        
        
        for i in range(len(spec)):
            for j in range(len(spec[0])):
                n = 0
                c1 = str(format(spec2[i, j * 2, 0], '02x'))
                c2 = str(format(spec2[i, j * 2, 1], '02x'))
                num = c2 + c1
                n = int(num, 16) / 382
                if spec2[i, j * 2, 2] == 1:
                    n = n * -1
                
                c = 0
                c1 = str(format(spec2[i, j * 2 + 1, 0], '02x'))
                c2 = str(format(spec2[i, j * 2 + 1, 1], '02x'))
                num = c2 + c1
                c = int(num, 16) / 382
                if spec2[i, j * 2 + 1, 2] == 1:
                    c = c * -1
                spec[i, j] = complex(n, c)
                

               
        #Print the max value of spec // helpful for verifying accuracy
        print(spec.max())
        
        #Covnert the spectrogram back into a 1D audio signal
        audio_signal = librosa.istft(spec)
        
        #Write the array to a wave file
        wavfile.write(outputfn, 44100, audio_signal)
        print('Wrote ' + outputfn)




a = audioSpecs()



sig2, fs = librosa.load('disco.wav', sr=44100)

# # Create spectrogram from 1D array
spec = librosa.stft(sig2)
# 
# a.makeSpec('disco.wav', 'trainA')
# a.makeSpec('major.wav', 'piano/trainA')
# a.makeSpec('minor.wav', 'piano/trainB')
a.storePhase(spec, 'phase.txt')
# a.makeSpec('electric.wav', 'electric')
# a.imageToAudio('traina.wav', 'trainA', 0)


# bad = np.array(Image.open('./trainA/0.png'))
# good = np.array(Image.open('./disco/0.png'))
# dif = bad - good
# a.imageToAudio('trainb.wav', 'trainB', 0)
# print('test')
# 