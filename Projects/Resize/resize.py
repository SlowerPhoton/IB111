import numpy as np
import BMP
import math


def naive_enlarge(bmp_file, output_file, h, w):
    inp = BMP.BMP(bmp_file, 'r')
    inp.raw_to_data()
    inp.data = np.repeat(inp.data, h, 0)
    inp.data = np.repeat(inp.data, w, 1)
    inp.data_to_raw()
    inp.update_params()
    inp.writeData(output_file)

def naive_shrink(bmp_file, output_file, h, w):
    inp = BMP.BMP(bmp_file, 'r')
    inp.raw_to_data()

    cols = []
    for c in range (inp.biWidth//w):
        new_col = 0
        for i in range (w):
            new_col += inp.data[:,c*w+i].astype('uint16')
        new_col //= w
        cols.append(new_col.astype('uint8'))
    new_data = np.column_stack(cols)
    new_data = new_data.reshape(inp.biHeight, inp.biWidth//w, 3)

    rows = []
    for r in range (inp.biHeight//h):
        new_row = 0
        for i in range (h):
            new_row += new_data[r*h+i].astype('uint16')
        new_row //= h
        rows.append(new_row.astype(np.uint8))
    new_data = np.array(rows)
    
    
    inp.data = new_data
    #inp.pad_data()
    inp.data_to_raw()
    inp.update_params()
    inp.writeData(output_file)

def resize(bmp_file, output_file, new_height, new_width):
    inp = BMP.BMP(bmp_file, 'r')
    h = inp.biHeight
    w = inp.biWidth
    height_gcd = math.gcd(inp.biHeight, new_height)
    width_gcd = math.gcd(inp.biWidth, new_width)
    naive_enlarge(bmp_file, output_file, new_height//height_gcd, new_width//width_gcd)
    naive_shrink(output_file, output_file, inp.biHeight//height_gcd, inp.biWidth//width_gcd)

def weigthed_mean_shrink(bmp_file, output_file, h, w):
    inp = BMP.BMP(bmp_file, 'r')
    inp.raw_to_data()

    cols = []
    for c in range (inp.biWidth//w):
        #new_col = np.zeros((inp.biHeight, 3), np.uint8)
        #new_col.reshape((inp.biHeight, 3))
        new_col = 0
        for i in range (w):
            new_col += inp.data[:,c*w+i].astype('uint16')*2**(1/(2 +(2*abs(w//2-i))))
        new_col //= w
        cols.append(new_col.astype('uint8'))
    new_data = np.column_stack(cols)
    new_data = new_data.reshape(inp.biHeight, inp.biWidth//w, 3)  
    
    inp.data = new_data
    inp.data_to_raw()
    inp.update_params()
    inp.writeData(output_file)
