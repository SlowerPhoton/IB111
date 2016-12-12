import WAVFile as wav
import byte as b
import numpy as np

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

'''
    Change the volume of a given wave song by a factor k

    using byte module (slow)
'''
def changeVolumeSlow(wavFile = "snow.wav", k = 1.2, outputFile = "louder.wav"):
    inp = open(wavFile, 'rb')
    allChunks = inp.read(wf.allChunksSize)
    out = open(outputFile, 'wb')
    out.write(allChunks)
    
    # read all data from input file into array (each index represents one sample)
    for sampleIndex in range (0, wf.numSamples):      
        sample = inp.read(wf.bytesPerSample)
        sample = byte.Byte(byteArray = sample)
        sample.multiplyBy(k)
        out.write(sample.toBytearray())
        
    inp.close()
    out.close()

'''
    Change the volume of a given wave song by a factor k

    using numpy (fast)
'''
def changeVolume(wavFile = 'snow.wav', k = 2.0, outFile = 'louder.wav'):
    wf = wav.WAVFile(wavFile, 'r')
    wf.dataRaw = b.multiply(wf.dataRaw, k, wf.bitsPerSample, wf.signed)
    wf.writeData(outFile)
    
'''
    Obsolete function
'''
def changeDataFormat(bitsPerSample, wavFile = "snow.wav", outputFile = "worse.wav"):
    wfi = WAVFile.WAVFile(wavFile, 'r')
    wfo = WAVFile.WAVFile(outputFile, 'w')
    # 16 -> 8 bit samples
    wfo.data = from16to8bit()
    wfo.numChannels = wfi.numChannels
    wfo.blockAlign = 1*wfi.numChannels
    wfo.sampleRate = wfi.sampleRate
    wfo.fillAttrs()
    wfo.writeData()

'''
    Changes wavefile data format from 16 to 8 bit
'''
def from16to8bit(wavFile = "snow.wav", outputFile = "16to8bit.wav"):
    wfi = wav.WAVFile(wavFile, 'r')
    wfo = wav.WAVFile(outputFile, 'w')
    dtype = 'int16'    
    data = np.frombuffer(wfi.dataRaw, dtype=dtype)
    processed = np.clip((data+32768)//256, 0, 255)
    wfo.dataRaw = bytes(processed.astype('uint8'))
    wfo.numChannels = wfi.numChannels
    wfo.blockAlign = 1*wfi.numChannels
    wfo.sampleRate = wfi.sampleRate
    wfo.fillAttrs()
    wfo.writeData()

'''
    Changes wavefile data format from 32 to 16 bit
'''
def from32to16bit(wavFile = "snow.wav", outputFile = "32to16bit.wav"):
    wfi = wav.WAVFile(wavFile, 'r')
    wfo = wav.WAVFile(outputFile, 'w')
    dtype = 'float32'
    data = np.frombuffer(wfi.dataRaw, dtype=dtype)
    processed = np.clip((data*32768)-1.0, -32768.0, 32767.0)
    wfo.dataRaw = bytes(processed.astype('int16'))
    wfo.numChannels = wfi.numChannels
    wfo.blockAlign = 2*wfi.numChannels
    wfo.sampleRate = wfi.sampleRate
    wfo.fillAttrs()
    wfo.writeData()

'''
    Changes wavefile data format from 32 to 8 bit
'''
def from32to8bit(wavFile = "snow.wav", outputFile = "32to8bit.wav"):
    wfi = wav.WAVFile(wavFile, 'r')
    wfo = wav.WAVFile(outputFile, 'w')
    dtype = 'float32'
    data = np.frombuffer(wfi.dataRaw, dtype=dtype)
    processed = np.clip((data+1.0)*128.5, 0, 255)
    wfo.dataRaw = bytes(processed.astype('uint8'))
    wfo.numChannels = wfi.numChannels
    wfo.blockAlign = 1*wfi.numChannels
    wfo.sampleRate = wfi.sampleRate
    wfo.fillAttrs()
    wfo.writeData()
