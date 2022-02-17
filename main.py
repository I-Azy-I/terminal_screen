from PIL import Image
import numpy as np
import os

PIXEL = '▀'
def create_pixel(rgb1,rgb2):
    return f'\x1b[38;2;{rgb1[0]};{rgb1[1]};{rgb1[2]}m' + f'\x1b[48;2;{rgb2[0]};{rgb2[1]};{rgb2[2]}m' + PIXEL 
def print_screen(screen):
    string_screen = ''
    for i in range(len(screen)//2):
        string_row = ''
        row1 = screen[i*2]
        row2 = screen[(i*2)+1]
        for pix1, pix2 in zip(row1,row2):
            string_row = string_row + create_pixel(pix1,pix2)
        #print(string_row + '\x1b[0m', flush=True)
        string_screen = string_screen + '\n' +string_row + '\x1b[0m'
    if len(screen) % 2:
        string_row = [create_pixel(pix, (0,0,0)) for pix in screen[-1]]
        string_row = ''.join(string_row)
        string_screen = string_screen + '\n' +string_row + '\x1b[0m'
        #print(string_row+ '\x1b[0m')
    print(string_screen)
            
        
image = Image.open("rainbow.png")
size = os.get_terminal_size()
x = size[0] -1
y = size[1]*2 - 2
if image.size[0]/x >=  image.size[1]/y:
    resize = x/image.size[0]
else:
    resize = y/image.size[1]
    
image = image.resize((int(image.size[0]*resize),int(image.size[1]*resize)))

array_image = np.array(image)
print_screen(array_image)


