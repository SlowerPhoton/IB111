import BMP
import generate as gen
import resize as rs


rs.resize('nature_standardized.bmp', 'pad_test.bmp', 540, 480)
    
#bmp = BMP.BMP('collision.bmp', 'r')
#gen.color_stripes()
#for i in range(10):
#    rs.naive_enlarge('color_stripes.bmp', 'mega_stripes.bmp', 5, 5)
#    rs.naive_shrink('mega_stripes.bmp', 'color_stripes.bmp', 5, 5)
