import sys
import byte

class InvalidFileFormat(Exception):
    def __init__(self, message):
        self.message = message

class FileCorrupted(Exception):
    def __init__(self, message):
        self.message = message


'''
Source: http://soundfile.sapp.org/doc/WaveFormat/

+--------+---------------------+---------------+--------------------+
| Endian | File offset (bytes) | Field name    | Field Size (bytes) |
+--------+---------------------+---------------+--------------------+
| big    |                   0 | ChunkID       |                  4 |
| little |                   4 | ChunkSize     |                  4 |
| big    |                   8 | Format        |                  4 |
+--------+---------------------+---------------+--------------------+
| big    |                  12 | Subchunk1ID   |                  4 |
| little |                  16 | Subchunk1Size |                  4 |
| little |                  20 | AudioFormat   |                  2 |
| little |                  22 | NumChannels   |                  2 |
| little |                  24 | SampleRate    |                  4 |
| little |                  28 | ByteRate      |                  4 |
| little |                  32 | BlockAlign    |                  2 |
| little |                  34 | BitsPerSample |                  2 |
+--------+---------------------+---------------+--------------------+
| big    |                  36 | Subchunk2ID   |                  4 |
| little |                  40 | Subchunk2Size |                  4 |
| little |                  44 | data          |                  ? |
+--------+---------------------+---------------+--------------------+
'''

class WAVFile:

    def inform(self):    
        print ("File size is " + str(self.fileByteSize) + " bytes")
        if self.audioFormat == 1:
            print ("File is not compressed.\n")
        else:
            print ("File is compressed.\n")
        if self.numChannels == 1:
            print ("Mono")
        elif self.numChannels == 2:
            print ("Stereo")
        else:
            print (str(self.numChannels) + " channels")
        print ("Sample rate is " + str(self.sampleRate))
        print ("Byte rate is " + str(self.byteRate))
        print ("Bits per sample = " + str(self.bitsPerSample))
        print("Size of the data chunk: " + str(self.dataSize) + " bytes")
        print("Number of samples: " + str(self.numSamples))
        print("Duration od the track is " + str(self.numSamples//self.sampleRate) + " seconds.")
        

    def __init__(self, wavFile, fileMode):
        self.fileName = wavFile
        if fileMode == 'r':
            self.readData()
        elif fileMode == 'w':
            pass
        else:
            AttributeError('Invalid file mode')

    def readData(self):
        wf = open(self.fileName, 'rb')

        ''' RIFF chunk '''
        # read ChunkID (should be 'RIFF')
        chunkID = wf.read(4)
        if chunkID.decode('ASCII') != 'RIFF':
            raise InvalidFileFormat('is not RIFF')
        self.chunkID = chunkID.decode('ASCII')
        
        # read ChunkSize and count the size of the file (in bytes)
        chunkSize = wf.read(4)
        chunkSize = int.from_bytes(chunkSize, byteorder='little', signed=False)
        fileByteSize = 8 # 8 bytes for ChunkID and ChunkSize
        fileByteSize += chunkSize
        self.fileByteSize = fileByteSize
        self.chunkSize = chunkSize
        
        # read Format (should be 'WAVE')
        frmt = wf.read(4)
        if frmt.decode('ASCII') != 'WAVE':
            raise InvalidFileFormat('is not WAVE')
        self.frmt = frmt.decode('ASCII')

        ''' fmt subchunk '''
        # read Subchunk1ID (should be "fmt ")
        subchunk1ID = wf.read(4)
        if subchunk1ID.decode('ASCII') != 'fmt ':
            raise InvalidFileFormat('no fmt subchunk')
        self.subchunk1ID = subchunk1ID.decode('ASCII')

        # read Subchunk1Size (16 for PCM)
        subchunk1Size = wf.read(4)
        subchunk1Size = int.from_bytes(subchunk1Size, byteorder='little', signed=False)
        self.subchunk1Size = subchunk1Size

        # read AudioFormat (if not 1 there is some kind of compression)
        audioFormat = int.from_bytes(wf.read(2), byteorder='little', signed=True)
        self.audioFormat = audioFormat

        # read NumChannels (Mono = 1, Stereo = 2, ...)
        numChannels = int.from_bytes(wf.read(2), byteorder='little', signed=False)
        self.numChannels = numChannels

        # read SampleRate - samples per second
        sampleRate = int.from_bytes(wf.read(4), byteorder='little', signed=False)
        self.sampleRate = sampleRate

        # read ByteRate (= SampleRate * NumChannels * BitsPerSample/8)
        byteRate = int.from_bytes(wf.read(4), byteorder='little', signed=False)
        self.byteRate = byteRate

        # read BlockAlign (= NumChannels * BitsPerSample/8)
        # The number of bytes for one sample including all channels.
        blockAlign = int.from_bytes(wf.read(2), byteorder='little', signed=False)
        self.blockAlign = blockAlign
        self.bytesPerSample = blockAlign # alias for blockAlign
        
        # read BitsPerSample
        bitsPerSample = int.from_bytes(wf.read(2), byteorder='little', signed=False)
        self.bitsPerSample = bitsPerSample
        if bitsPerSample == 8:
            self.signed = False
        if bitsPerSample == 16 or bitsPerSample == 32:
            self.signed = True
        else:
            raise InvalidFileFormat('samples not 8, 16 or 32bit')
        
        # perform value checks on the subchunk
        if byteRate != sampleRate * numChannels * bitsPerSample//8:
            raise FileCorrupted("ByteRate != SampleRate * NumChannels * BitsPerSample//8")
        if blockAlign != numChannels * bitsPerSample//8:
            raise FileCorrupted ('BlockAlign != NumChannels * BitsPerSample//8')

        # if subchunk's size is more than 16, we need to read the rest of the data
        # which is of no importance to us and thus skip it
        wf.read(self.subchunk1Size-16)

        '''
        get through all optional metadata chunks until you get to 'data'
        '''
        # read chunk's ID, if it's not "data", read its length and skip it
        chunkID = bytes()
        chunkSize = 0
        while chunkID.decode('ASCII') != 'data':
            wf.read(chunkSize)
            chunkID = wf.read(4)
            chunkSize = int.from_bytes(wf.read(4), byteorder='little', signed=False)

        ''' data subchunk '''
        # set Subchunk2ID
        self.subchunk2ID = chunkID.decode('ASCII')
        
        # read Subchunk2Size and get the number of bytes in Data (dataSize)
        # = NumSamples * NumChannels * BitsPerSample/8 + 8 (get NumSamples)
        dataSize = chunkSize
        self.dataSize = dataSize
        self.subchunk2Size = dataSize
        self.numSamples = dataSize // (numChannels*bitsPerSample//8)       

        # to store all the data we need to skip in order to get to the data
        self.allChunksSize = fileByteSize - dataSize

        # read all data from input file into array (each index represents one sample)
        self.dataRaw = wf.read(self.dataSize)
        #self.data = []
        #for sampleIndex in range (0, self.numSamples):
            #sample = self.dataRaw[sampleIndex:sampleIndex+2]
            #sampleInt = int.from_bytes(sample, byteorder='little', signed=True)
            #self.data.append(sampleInt)
            #self.data.append(sample)
        
        wf.close()
        self.set_dtype()

    # write wavfile into a file
    def writeData(self, outputFileName = ""):
        if outputFileName == "":
            outputFileName = self.fileName
        out = open(outputFileName, 'wb')

        if not hasattr(self, 'chunkID'):
            self.chunkID = 'RIFF'
        out.write(bytearray(self.chunkID, 'ASCII'))
        if not hasattr(self, 'chunkSize'):
            self.chunkSize = self.fileByteSize - 8
        chunkSize = byte.Byte(dec = self.chunkSize, barrLen = 4, signed=False) 
        out.write(chunkSize.toBytearray())
        if not hasattr(self, 'format'):
            self.format = 'WAVE'
        out.write(bytearray(self.format, 'ASCII'))

        if not hasattr(self, 'subchunk1ID'):
            self.subchunk1ID = 'fmt '
        out.write(bytearray(self.subchunk1ID, 'ASCII'))
        if not hasattr(self, 'subchunk1Size'):
            self.subchunk1Size = self.chunkSize - 12
        subchunk1Size = byte.Byte(dec = self.subchunk1Size, barrLen = 4, signed=False) 
        out.write(subchunk1Size.toBytearray())
        if not hasattr(self, 'audioFormat'):
            self.audioFormat = 1
        audioFormat = byte.Byte(dec = self.audioFormat, barrLen = 2) 
        out.write(audioFormat.toBytearray())
        numChannels = byte.Byte(dec = self.numChannels, barrLen = 2, signed=False) 
        out.write(numChannels.toBytearray())
        sampleRate = byte.Byte(dec = self.sampleRate, barrLen = 4, signed=False) 
        out.write(sampleRate.toBytearray())
        byteRate = byte.Byte(dec = self.byteRate, barrLen = 4, signed=False) 
        out.write(byteRate.toBytearray())
        blockAlign = byte.Byte(dec = self.blockAlign, barrLen = 2, signed=False) 
        out.write(blockAlign.toBytearray())
        bitsPerSample = byte.Byte(dec = self.bitsPerSample, barrLen = 2, signed=False) 
        out.write(bitsPerSample.toBytearray())

        if not hasattr(self, 'subchunk2ID'):
            self.subchunk2ID = 'data'
        out.write(bytearray(self.subchunk2ID, 'ASCII'))
        if not hasattr(self, 'subchunk2Size'):
            self.subchunk2Size = self.subchunk1Size - 24
        subchunk2Size = byte.Byte(dec = self.subchunk2Size, barrLen = 4, signed=False) 
        out.write(subchunk2Size.toBytearray())
        #for sampleIndex in range(self.numSamples):
        #    out.write(self.data[sampleIndex])
        out.write(self.dataRaw)

        out.close()

    # existence of numChannels, blockAlign (bytesPerSample), sampleRate is enforced
    # if fileByteSize doesn't exist, assumes there are only the 3 obligatory chunks
    # if subchunk1Size is not provided, it is set to 16 (PCM)
    def fillAttrs(self):
        if not hasattr(self, 'dataSize'):
            if not hasattr(self, 'data'):
                self.dataSize = self.dataRaw.__len__()
            else:
                self.dataSize = self.data.__len__()*self.blockAlign
        if not hasattr(self, 'bitsPerSample'):
            self.bitsPerSample = self.blockAlign*8 // self.numChannels
        if not hasattr(self, 'byteRate'):
            self.byteRate = self.sampleRate*self.numChannels*self.bitsPerSample//8
        if not hasattr(self, 'fileByteSize'):
            self.fileByteSize = 44 + self.dataSize
        if not hasattr(self, 'chunkSize'):
            self.chunkSize = self.fileByteSize - 8
        if not hasattr(self, 'subchunk1Size'):
            self.subchunk1Size = 16
        if not hasattr(self, 'subchunk2Size'):
            self.subchunk2Size = self.dataSize
        if not hasattr(self, 'numSamples'): # to facilitate writing data in writeData
            self.numSamples = self.dataSize // (self.numChannels*self.bitsPerSample//8)

    # sets corresponding dtype according to blockAlign
    # WARNING: doesn't cover all possible dtypes
    def set_dtype(self):
        if self.blockAlign == 1:
            self.dtype = 'uint8'
        elif self.blockAlign == 2:
            self.dtype = 'int16'
        elif self.blockAlign == 4:
            self.dtype = 'float32'
