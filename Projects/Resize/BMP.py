import numpy as np

class UnknownFileFormat (Exception):
    pass
        
class BMP:

    def __init__(self, bmp_file, mode):
        if mode == 'r':
            self.read(bmp_file)
            self.name = bmp_file
        elif mode == 'w':
            self.name = bmp_file
            self.biWidth = 0
            self.biHeight = 0
            self.bfSize = 54
            self.dataRaw = b''
        else :
            raise ValueError('Unknown mode of opening')
    
    def inform(self):
        print ("size of the file is " + str(self.bfSize) + ' bytes')
        print ('image width is ' + str(self.biWidth))
        print ('image height is ' + str(self.biHeight))
        print ('bits per pixel: ' + str(self.biBitCount))
    
    def read(self, bmp_file):
        inp = open(bmp_file, 'rb')

        # file header 14 bytes
        bfType = inp.read(2)
        self.bfType = bfType.decode('ASCII')
        if self.bfType != 'BM':
            raise UnknownFileFormat('bfType is not \'BM\' as expected!')
        bfSize = inp.read(4)
        self.bfSize = int.from_bytes(bfSize, byteorder='little', signed = False)
        bfReserved1 = inp.read(2)
        self.bfReserved1 = int.from_bytes(bfReserved1, byteorder='little', signed = True)
        bfReserved2 = inp.read(2)
        self.bfReserved2 = int.from_bytes(bfReserved2, byteorder='little', signed = True)
        bfOffBits = inp.read(4)
        self.bfOffBits = int.from_bytes(bfOffBits, byteorder='little', signed = False)

        # image header usually 40 bytes
        self.biSize = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        if self.biSize < 40:
            raise UnknownFileFormat('Size of image header less than 40')
        self.biWidth = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        self.biHeight = int.from_bytes(inp.read(4), byteorder='little', signed=True)
        if self.biHeight < 0:
            self.upside_down = True
        else :
            self.upside_down = False
        self.biPlanes = int.from_bytes(inp.read(2), byteorder='little', signed=False)
        if self.biPlanes != 1:
            raise UnknownFileFormat('Number of planes must be 1!')
        self.biBitCount = int.from_bytes(inp.read(2), byteorder='little', signed=False)
        self.biCompression = int.from_bytes(inp.read(4), byteorder='little', signed=True)
        if self.biCompression != 0:
            raise UnknownFileFormat('We only support uncompressed formats')
        self.biSizeImage = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        # if uncompressed can be set to 0
        self.biXPelsPerMeter = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        self.biYPelsPerMeter = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        self.biClrUsed = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        self.biClrImportant = int.from_bytes(inp.read(4), byteorder='little', signed=False)
        # the rest of image header
        self.biRest = inp.read(self.biSize-40)

        # color table
        # this if-else statement is temporary
        if self.bfOffBits - 14 - self.biSize < 0:
            print('negative')
            self.raw_data = inp.read()
            return
        else:
            self.colorTable = inp.read(self.bfOffBits - 14 - self.biSize)
        
        # data
        #self.raw_data = inp.read(self.biWidth*abs(self.biHeight)*self.biBitCount//8)
        self.raw_data = inp.read()
        
        inp.close()

    # creates a bmp file and fills it with this instance of BMP
    # if output_file is not specified, uses self.name
    # WARNING: uses raw_data rather than data
    # if pad is set to True also pads raw_data correctly (by calling
    # pad_raw_data) and updates bfSize accordingly
    # NOTE: writes colorTable (if not empty) as well
    def write_data(self, output_file = None, pad=True):
        if output_file == None:
            output_file = self.name
        out = open(output_file, 'wb')

        if pad:
            self.pad_raw_data()
            self.bfSize = 54 + self.colorTable.__len__() + self.raw_data.__len__()

        # file header 14 bytes
        out.write(bytes(self.bfType, 'ASCII'))
        out.write(self.bfSize.to_bytes(4, byteorder='little', signed=False))
        out.write(self.bfReserved1.to_bytes(2, byteorder='little', signed=True))
        out.write(self.bfReserved2.to_bytes(2, byteorder='little', signed=True))
        out.write(self.bfOffBits.to_bytes(4, byteorder='little', signed=False))

        # image header forced to 40 bytes
        out.write(self.biSize.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biWidth.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biHeight.to_bytes(4, byteorder='little', signed=True))
        out.write(self.biPlanes.to_bytes(2, byteorder='little', signed=False))
        out.write(self.biBitCount.to_bytes(2, byteorder='little', signed=False))
        out.write(self.biCompression.to_bytes(4, byteorder='little', signed=True))
        out.write(self.biSizeImage.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biXPelsPerMeter.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biYPelsPerMeter.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biClrUsed.to_bytes(4, byteorder='little', signed=False))
        out.write(self.biClrImportant.to_bytes(4, byteorder='little', signed=False))

        # color table
        if hasattr(self, 'colorTable'):
            out.write(self.colorTable)
        
        # data
        out.write(self.raw_data)

        out.close()

    def putColor (self, x, y, color):
        self.data[x][y] = color
    
    def putPixel (self, x, y, color_slot, value):
        if color_slot == 'r':
            color_slot = 2
        elif color_slot == 'g':
            color_slot = 1
        elif color_slot == 'b':
            color_slot = 0
        else :
            raise ValueError("param color_slot must be either 'r', 'g' or 'b'")
        self.data[x][y][color_slot] = value

    # converts the raw data into a ndarray [row][column][pixel]
    # ignores (skips) padding
    def raw_to_data (self, maxHeight = None, maxWidth = None):
        if maxHeight == None or maxHeight < self.biHeight:
            maxHeight = abs(self.biHeight)
        if maxWidth == None or maxWidth < self.biWidth:
            maxWidth = self.biWidth
        self.width = maxWidth
        self.height = maxHeight
        # '''[int.from_bytes(self.dataRaw[p*r+pix], byteorder = 'little', signed=False)]'''
        # np.frombuffer(self.dataRaw, dtype='uint8', count = 1, offset = r*p+pix).tolist()
        #self.data = np.array([[ [int.from_bytes(self.dataRaw[p*r+pix], byteorder = 'little', signed=False) for pix in range(self.biBitCount//8-1, -1, -1) ] for p in range(self.biWidth) ] for r in range(self.biHeight)], np.uint8)

        pixels = np.frombuffer(self.raw_data, dtype='uint8')
        padding = (4 - (self.biWidth*self.biBitCount//8 % 4)) % 4
        
        to_add = maxWidth-self.biWidth    
        points = []
        col = 0
        #self.biWidth*self.biHeight*self.biBitCount//8
        #for p in range(0, self.raw_data.__len__(), 3):
        p = 0
        while p <= self.raw_data.__len__()-3:
            points.append(pixels[p:p+3])
            col += 1
            if col % self.biWidth == 0:
                p += padding
                col = 0
                for i in range(to_add):
                    points.append(np.array([0,0,0], np.uint8))
            p += 3
        #print (points)
        #print (points.__len__())
        rows = []
        for r in range(0, maxWidth*self.biHeight, maxWidth):
            rows.append(points[r:r+maxWidth])
        
        to_add = maxHeight - self.biHeight
        for i in range(to_add):
            rows.append(np.array([(0,0,0) for j in range(maxWidth)]))
        
        self.data = np.array(rows, np.uint8)

    def data_to_raw (self):
        self.raw_data = self.data.tostring()

    # deprecated, use pad_raw_data instead
    def pad_data(self):
        if (not hasattr(self, 'data')):
            raise AttributeError('There is no \'data\'')      
        to_pad = self.data.shape[1] % 4
        self.data = np.append(self.data, np.zeros((self.data.shape[0],to_pad,self.data.shape[2]), np.uint8), axis=1)

    # pad each row so it ends on a 4 byte boundary
    # doesn't update any stats
    def pad_raw_data(self):
        if (not hasattr(self, 'raw_data')):
            raise AttributeError('There is no \'raw_data\'') 
        h = self.biHeight
        w = self.biWidth*self.biBitCount//8
        raw = np.frombuffer(self.raw_data, np.uint8)
        padded = raw.reshape(h, w)
        to_pad = (4 - (w % 4)) % 4
        padded = np.append(padded, np.zeros((h,to_pad), np.uint8), axis=1)
        self.raw_data = padded.astype(np.uint8).tostring()
        
    
    # updates biHeight, biWidth and bfSize according to data.shape
    def update_params(self):
        self.height = self.data.shape[0]
        self.width = self.data.shape[1]
        self.bytecount = self.data.shape[2]
        self.biHeight = self.height
        self.biWidth = self.width
        self.bfSize = 54 + self.height*self.width*self.bytecount

    # sets all necessary parameters to a predefined state
    # WARNING: rewrites all File and Image header data of the instance
    def default(self):
        self.bfType = 'BM'
        self.bfSize = 54   # alter
        self.bfReserved1 = 0
        self.bfReserved2 = 0
        self.bfOffBits = 54
        self.biSize = 40
        self.biWidth = 0 # alter
        self.biHeight = 0 # alter
        self.biPlanes = 1
        self.biBitCount = 24 # alter
        self.biCompression = 0
        self.biSizeImage = 0
        self.biXPelsPerMeter = 0
        self.biYPelsPerMeter = 0
        self.biClrUsed = 0
        self.biClrImportant = 0
        self.colorTable = b''
        self.raw_data = b''
