'''
    This file is obsolete
    Not recommended to run
'''

import sys
sys.path.append("C:/Users/HP/Dektop/WAV reader")

import WAVFile
import alter as a

'''
import alsaaudio

card = 'default'
device = alsaaudio.PCM(mode = alsaaudio.PCM_NONBLOCK)
device.setchannels(NumChannels)
device.setrate(SampleRate)


device.setformat(alsaaudio.PCM_FORMAT_S16_LE)

for i in range(0,10000):
    #sample = int.from_bytes(song.read(2), byteorder='little', signed=False)
    #print (sample)
    a = song.read(2)
    songStart = False
    if a != b'\x00\x00':
        songStart = True
    if songStart:
        #print (a)
        device.write(a)
song.close()

def analyse(wavFile = "snow.wav"):
    f = open(wavFile, 'rb')
    maxAmplitude = [(0,0)]
    for i in range(0, numSamples):
        sample = int.from_bytes(f.read(2), byteorder='little', signed=False)
        if sample > maxAmplitude[-1][1]:
            newValue = (i, sample)
            maxAmplitude.append(newValue)
        
    f.close()
    print (maxAmplitude)
'''


wf = WAVFile.WAVFile("snow.wav", 'r')

a.changeDataFormat(8)
test = WAVFile.WAVFile("test.wav", 'r')


    

import byte
'''
maxValue = 2**(wf.bytesPerSample)-1

statB = byte.Byte(dec = 0)

def alternativeMultiplication(sample, k, sampleBytes):
    sample = int.from_bytes(sample, byteorder = 'little', signed=True)
    sample *= k
    neg = False
    if sample < 0:
        neg = True
    
    if sample > maxValue:
        sample = maxValue
    barr = [0 for i in range(sampleBytes)]
    for i in range(sampleBytes):
        barr[-i-1] = sample%256
        sample//=256
    return barr
'''

barr = b'\xff\x00'

b = byte.Byte(byteArray = barr)
#changeVolume(k = 10)

sam = b'\x01\xff'
#print (alternativeMultiplication(sam, 2, 2))

# is byteA > byteB
# behaviour undefined if not the same length
def compareSignedBytearrays(bytearrayA, bytearrayB):
    maxValue = 2**(8*bytearrayA.__len__()-1)-1
    # no idea how to do it efficiently without converting to int
