import tensorflow
import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import pyglet
import os
import time
from scipy.io import wavfile

waveout = 'output.wav' # Defining the output wave file
step = 0.05 # Step size
M = 50 # Number of filter taps in adaptive filter

# Read the audio files of sender and listener
sfs, u = wavfile.read('sender.wav')
lfs, v = wavfile.read('listener.wav')

u = np.fromstring(u, np.int16)
u = np.float64(u)

v = np.fromstring(v, np.int16)
v = np.float64(v)

# Generate the fedback signal d(n) by a) convolving the sender's voice with randomly chosen coefficients assumed to emulate the listener's room 
# characteristic, and b) mixing the result with listener's voice, so that the sender hears a mix of noise and echo in the reply.

coeffs = np.concatenate(([0.8], np.zeros(8), [-0.7], np.zeros(9), [0.5], np.zeros(11), [-0.3], np.zeros(3),[0.1], np.zeros(20), [-0.05]))
d = np.convolve(u, coeffs)
d = d/20.0
v = v/20.0
d = d[:len(v)] # Trims sender's audio to the same length as that of the listener's in order to mix them
d = d + v - (d*v)/256.0   # Mix with listener's voice.
d = np.round(d,0)

# Hear how the mixed signal sounds before proceeding with the filtering.
dsound = d.astype('int16')
wavfile.write(waveout, lfs, dsound)

music = pyglet.resource.media('output.wav')
music.play()
time.sleep(len(dsound)/lfs)
# Apply adaptive filter
y, e, w = adf.nlms(u[:len(d)], d, M, step, returnCoeffs=True)

# The algorithm stores the processed result in the variable 'e', which is the mix of the error signal and the listener's voice.
# Hear how e sounds now.  Ideally we on behalf of the sender, should hear only the listener's voice.  Practically, some echo would still be present.

e = e.astype('int16')
wavfile.write('adapt.wav', lfs, e)
music = pyglet.resource.media('adapt.wav')
music.play()
time.sleep(len(e)/lfs)

# Calculate and plot the mean square weight error
mswe = adf.mswe(w, coeffs)
plt.figure()
plt.title('Mean squared weight error')
plt.plot(mswe)
plt.grid()
plt.xlabel('Samples')

plt.show()

# **** PROGRAM END ****

# Copyright (c) 2016 by Varun Chandramohan
