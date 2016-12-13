import BMP
import color as c
import numpy as np
import generate as gen
import resize as rs
import math


def expand_to(bmp_file, output_file, new_height, new_width):
    inp = BMP.BMP(bmp_file, 'r')
    h = inp.biHeight
    w = inp.biWidth
    height_gcd = math.gcd(inp.biHeight, new_height); print(height_gcd)
    width_gcd = math.gcd(inp.biWidth, new_width); print(width_gcd)
    rs.naive_enlarge(bmp_file, output_file, new_height//height_gcd, new_width//width_gcd)
    rs.naive_shrink(output_file, output_file, inp.biHeight//height_gcd, inp.biWidth//width_gcd)
    
bmp = BMP.BMP('collision.bmp', 'r')
#gen.color_stripes()
#for i in range(10):
#    rs.naive_enlarge('color_stripes.bmp', 'mega_stripes.bmp', 5, 5)
#    rs.naive_shrink('mega_stripes.bmp', 'color_stripes.bmp', 5, 5)


#yes
