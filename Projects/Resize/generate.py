import BMP
import color

def color_stripes():
    draw = BMP.BMP('color_stripes.bmp', 'w')
    draw.default()
    draw.raw_to_data(40, 20)

    for c in range(20):
        for r in range(40):
            i = c
            col = []
            for e in color.Color:
                if i % 5 == 0:
                    col = e.value
                i += 1
            draw.putColor(r, c, col) 

    draw.data_to_raw()
    draw.update_params()
    draw.writeData()

def blue_line():
    draw = BMP.BMP('draw.bmp', 'w')
    draw.default()
    draw.raw_to_data(20, 20)

    for x in range(20):
        draw.putPixel(0,x,'r', 0)
        draw.putPixel(0,x,'g', 0)
        draw.putPixel(0,x,'b', 255)

    draw.data = np.repeat(draw.data, 2, 1)
    draw.data = np.repeat(draw.data, 2, 0)


    draw.data_to_raw()
    draw.update_params()
    draw.writeData()
