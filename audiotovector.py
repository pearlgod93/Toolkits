#Libraries-to-import

import soundfile as sf
import pyplotlib as plot

# Reading audio file
path = 'abcd'
def aud_read(path):
	  data, srate = sf.read(path + '.wav') #If it is present in the existing directory
	  return data, srate

#Convert file to mono
def aud_mono(d):
	  mon_aud = (d[:,0] + d[:,1]) / 2
	  return mon_aud

#Audio write function
def aud_write(file, wdata, wsrate):
	  sf.write(file, wdata, wsrate)
	  print(file + ' -> Audio file created')

#End of program
