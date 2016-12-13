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
            self.dataRaw = inp.read()
            return
        else:
            self.colorTable = inp.read(self.bfOffBits - 14 - self.biSize)
        
        # data
        self.dataRaw = inp.read(self.biWidth*abs(self.biHeight)*self.biBitCount//8)

        inp.close()

    def writeData(self, output_file = None):
        if output_file == None:
            output_file = self.name
        out = open(output_file, 'wb')

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
        out.write(self.dataRaw)

        out.close()

    def putColor (self, x, y, color):
        self.data[x][y] = color
    
    def putPixel (self, x, y, color_slot, value):
        '''
        if y > self.biHeight-1:
            to_add = y - self.biHeight
            for i in range(to_add):
                self.data = np.insert(self.data, -1, [ [0,0,0] for j in range(self.biWidth)], axis=1)
        '''
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

        pixels = np.frombuffer(self.dataRaw, dtype='uint8')
        
        to_add = maxWidth-self.biWidth    
        points = []
        col = 0
        for p in range(0, self.biWidth*self.biHeight*self.biBitCount//8, 3):
            #points.append(np.flipud(pixels[p:p+3]))
            points.append(pixels[p:p+3])
            col += 1
            if col % (self.biWidth) == 0:
                col = 0
                for i in range(to_add):
                    points.append(np.array([0,0,0], np.uint8))
        rows = []
        for r in range(0, maxWidth*self.biHeight, maxWidth):
            rows.append(points[r:r+maxWidth])
        
        to_add = maxHeight - self.biHeight
        for i in range(to_add):
            rows.append(np.array([(0,0,0) for j in range(maxWidth)]))
        
        self.data = np.array(rows, np.uint8)

    def data_to_raw (self):
        ''', height = None, width = None'''
        '''
        if height == None:
            height = abs(self.biHeight)
        if width == None:
            width = self.biWidth
        '''
        self.dataRaw = self.data.tostring()

    def pad_data(self):
        if (not hasattr(self, 'data')):
            raise ValueError('There is no \'data\'')
        to_pad = self.data.shape[1] % 4
        self.data = np.append(self.data, np.zeros((self.data.shape[0],to_pad,self.data.shape[2]), np.uint8), axis=1)

    # updates biHeight, biWidth and bfSize according to the data array
    def update_params(self):
        self.height = self.data.shape[0]
        self.width = self.data.shape[1]
        self.bytecount = self.data.shape[2]
        self.biHeight = self.height
        self.biWidth = self.width
        self.bfSize = 54 + self.height*self.width*self.bytecount

    # sets all necessary parameters to a predefined state
    # WARNING: deletes all previous data of the object
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
