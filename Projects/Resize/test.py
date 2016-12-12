import BMP
import color as c
import numpy as np
import generate as gen
import resize as rs

def expand_to(bmp_file, output_file, new_height, new_width):
    inp = BMP.BMP(bmp_file, 'r')
    h = inp.biHeight; print (h)
    w = inp.biWidth; print (w)
    rs.naive_enlarge(bmp_file, output_file, new_height, new_width)
    rs.naive_shrink(output_file, output_file, h, w)

bmp = BMP.BMP('collision.bmp', 'r')
#gen.color_stripes()
#for i in range(10):
#    rs.naive_enlarge('color_stripes.bmp', 'mega_stripes.bmp', 5, 5)
#    rs.naive_shrink('mega_stripes.bmp', 'color_stripes.bmp', 5, 5)


#yes
