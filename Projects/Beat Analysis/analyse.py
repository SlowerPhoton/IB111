import numpy as np

'''
    Obsolete function
    
    Find the maximum amplitude between samples in a given time interval
    (interval is in seconds)
'''
def findMaxAmplInInterval(wavFile = "snow.wav", interval = 0.5):
    f = open(wavFile, 'rb')
    f.read(allChunksSize) # skip everything and get straight to the data
    maxAmplitude = []
    samplesAtInterval = int (SampleRate*interval);
    for i in range(0, numSamples, samplesAtInterval):
        samples = f.read(samplesAtInterval*BitsPerSample//8)
        #print(samples)
        localMax = 0
        for s in range (0, samplesAtInterval, BitsPerSample//8):
            sample = int.from_bytes(samples[s:s+4], byteorder='little', signed=True)
            if sample > localMax:
                localMax = sample
        maxAmplitude.append(localMax)
        
    f.close()
    print (maxAmplitude)
    print ("no of values: " + str(maxAmplitude.__len__()))

'''
    Obsolete function
'''
def findDrums(wavFile, timestampsFile = "drums.data"):
    inp = open(wavFile.fileName, 'rb')
    inp.read(wavFile.allChunksSize)

    inp.close()
    out = open(timestampsFile, 'w')

    if data.__len__() < 2:
        print("insufficient data to process")
        quit()
        
    monotony = 0 # 1 amplitude is increasing, -1 decreasing, 0 stagnating  
    if data[0] < data[1]:
        monotony = 1
    elif data[0] > data[1]:
        monotony = -1
    else:
        monotony = 0

    
    localMins = [] # stores the index (from data) of all local minimums
    localMaxs = []
    for sampleIndex in range(2, numSamples):
        if data[sampleIndex-1] < data[sampleIndex]:
            if monotony != 1:
                localMins.append(sampleIndex-1)
                monotony = 1
        elif data[sampleIndex-1] > data[sampleIndex]:
            if monotony != -1:
                localMaxs.append(sampleIndex-1)
                monotony = -1
        else: # stagnating
            pass

    for mn in localMins:
        if (abs(data[mn] - data[mn+1]) > 9800):
            print (sampleIndexToSec(mn))
    print(data[-1])
def sampleIndexToSec(sampleIndex):
    return sampleIndex/SampleRate
def append(threshold, data, app, i, sample):
    for i in range(data.__len__()):
        if abs(data[i][2]-sample) < threshold:
            return
    #data.append((app, i, sample))
    data.append(sample)

'''
    Attempt to make a hash of each block of samples

    WARNING: completely useless and extremely slow
'''
def AdditiveHash(wf):
    data = []
    for j in range(500):
        start = 48000+j
        added_up = []
        for i in range(start*wf.blockAlign, 100000*wf.blockAlign, wf.blockAlign*500):
            tmp = 0;
            for j in range(500):
                tmp += int.from_bytes(wf.dataRaw[i+j:i+j+wf.blockAlign], byteorder='little', signed=False)
            added_up.append(tmp)

        k = 0.005
        base = added_up[0]
        for i in range(1, added_up.__len__()):
            if abs(base - added_up[i]) < abs(k*base):
                #data.append( (added_up[i], i, start+500*i) )
                append(500, data, added_up[i], i, start+500*i)

    # all 'found' repetetions merge into groups
    grps = [0 for i in range((100000-48000)//5000+1)]
    for i in range(data.__len__()):
        rep = (data[i][2] - 48000)//5000
        grps[rep] += 1

    # find the most common sample from groups
    mx = 0
    mx_index = -1
    for i in range(1, grps.__len__()):
        if grps[i] > mx:
            mx = grps[i]
            mx_index = i

    return data

'''
    Find beats

    Algorithm is based on checking the difference of
    each pair of samples

    If the difference is greater than threshold
    mark a beat
'''
def difference(threshold, wf):
    data = []
    lastSample = wf.dataRaw[0:wf.blockAlign]
    lastSample = int.from_bytes(lastSample, byteorder='little', signed=True)
    for sampleIndex in range(wf.blockAlign, 500000*wf.blockAlign, wf.blockAlign):
        sample = wf.dataRaw[sampleIndex:sampleIndex+wf.blockAlign]
        sample = int.from_bytes(sample, byteorder='little', signed=True)
        if (sample - lastSample) > threshold:
            data.append(sampleIndex//wf.blockAlign)
        lastSample = sample
    return data

'''
    Find beats

    Algorithm is based on checking the absolute value of each sample

    If the value is greater than threshold
    mark a beat
'''
def amplitude(threshold, wf):
    data = []
    for sampleIndex in range(0, 20000000*wf.blockAlign, wf.blockAlign//wf.numChannels):
        sample = wf.dataRaw[sampleIndex:sampleIndex+wf.blockAlign//wf.numChannels]
        sample = int.from_bytes(sample, byteorder='little', signed=True)
        if abs(sample) > threshold:
            data.append(sampleIndex//wf.blockAlign)
    return data

'''
    Clean data by removing 'outliers' and redundancy
'''
def cleanData(data, tolerance=1000):
    cleanData = []
    for i in range (1, data.__len__()):
        start_i = i
        occurences = 0
        while i < data.__len__() and (data[i] - data[i-1]) <= tolerance:
            occurences += 1
            i += 1
        if 8 >= occurences >= 4:
            cleanData.append(data[(i-start_i)//2 + start_i])
    return cleanData

'''
    Compute the number of (local) maximums of the sound function
    at given interval
''' 
def number_of_maxs(beg, end, wf):   
    # monotonicity > 0 if increasing, < 0 if decreasing, 0 if stagnant
    monotonicity = 1
    data = np.frombuffer(wf.dataRaw[beg*wf.blockAlign:end*wf.blockAlign], dtype=wf.dtype)
    i = 0
    while monotonicity == 0:
        monotonicity = data[i+1] - data[i]
        i += 1
    maxs = 0
    for sample in range(i, data.__len__()-1):
        new_monotonicity = data[sample+1] - data[sample]
        if new_monotonicity == 0:
            continue
        if new_monotonicity < 0:
            if monotonicity > 0:
                maxs += 1
        monotonicity = new_monotonicity
        #else :
        #    if monotonicity < 0:
        #        maxs += 1
        #        monotonicity = new_monotonicity
    return maxs

'''
    Find beats

    Algorithm is based on checking the monotonicity of
    the sound function in blocks
    This is accomplished by counting each time it changes
    from increasing to decreasing

    If the number of changes is greater than threshold
    mark a beat

    Calls number_of_maxs
'''
def curvature(threshold, wf, block):
    data = []
    for block_index in range(0, 100000):
        maxs = number_of_maxs(block_index*block, block*(block_index+1), wf)
        if maxs >= threshold:
            data.append(block_index*block)
    return data


