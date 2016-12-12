import WAVFile as wav
import alter as al
import visualize as vs
import analyse as an


#wf = wav.WAVFile('snow.wav', 'r')
#al.from16to8bit()
#al.from32to16bit(wavFile='snow32f.wav')
#al.from32to8bit(wavFile='snow32f.wav')
#data = an.AdditiveHash(wf)
#data = an.difference(2400, wf)
#data = an.amplitude(30500, wf)
#data = cleanData(data)
    
#data = an.curvature(10, wf, 50)

#wf = wav.WAVFile('iseefire.wav', 'r')
#data = an.amplitude(28000, wf) # fire
#data = an.curvature(20, wf, 100) # fire


#wf = wav.WAVFile('badkarma.wav', 'r')
#data = an.amplitude(10500, wf)
#data = an.curvature(23, wf, 100)
#vs.labels('drums.dat', wf, data)

vs.visualize(data, wf)
