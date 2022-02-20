import numpy as np
import os
import cv2
import time
import colorama


PIXEL = '▀'

def create_pixel(rgb1,rgb2, is_last=False):
    if is_last:
         return f'\x1b[38;2;{rgb1[0]};{rgb1[1]};{rgb1[2]}m' + PIXEL
    else:
        return f'\x1b[38;2;{rgb1[0]};{rgb1[1]};{rgb1[2]}m' + f'\x1b[48;2;{rgb2[0]};{rgb2[1]};{rgb2[2]}m' + PIXEL 
def print_screen(image, rewrite=False):
    size = os.get_terminal_size()

    x = size[0] - 1
    y = (size[1]*2) -8
    if (image.shape[0]/x >=1 or  image.shape[1]/y>=1):
        if image.shape[0]/x >=  image.shape[1]/y:
            resize = x/image.shape[0]
        else:
            resize = y/image.shape[1]
            
        image = cv2.resize(image, (int(image.shape[1]*resize), int(image.shape[0]*resize)), interpolation = cv2.INTER_AREA)
    string_image = ''
    if rewrite:
        old_height = image.shape[0]//2
    for i in range(image.shape[0]//2):
        string_row = ''
        row1 = image[i*2]
        row2 = image[(i*2)+1]
        for pix1, pix2 in zip(row1,row2):
            string_row = string_row + create_pixel(pix1,pix2)
        string_image = string_image + '\n' +string_row + '\x1b[0m'
    if len(image) % 2:
        string_row = [create_pixel(pix, (0,0,0), is_last=True) for pix in image[-1]]
        string_row = ''.join(string_row)
        string_image = string_image + '\n' +string_row + '\x1b[0m'
        if rewrite:
            
            
            old_height = old_height + 1
    print(string_image, end='')
    if rewrite:
        print((old_height)*'\033[A', end ='')
            
def print_image(path='pizza2.png'):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)  
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
    
    
    print_screen(image)
def print_animated(path, loop = True, duration = 0.1, do_clear = False):

    cap = cv2.VideoCapture(path)
    
    while True:
        old_time = time.time()
        ret, frame = cap.read()
        if not ret:
            if loop:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            else:
                break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Bye')
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if do_clear: 
            os.system('cls' if os.name == 'nt' else 'clear')
        print_screen(frame, rewrite=True)
        new_time = time.time()
        if duration-(new_time-old_time)> 0 : time.sleep(duration-(new_time-old_time))
        
def print_camera(number=0, do_clear=False):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if do_clear: 
            os.system('cls' if os.name == 'nt' else 'clear')
        print_screen(frame, rewrite=True)
#array_image = np.asarray( image, dtype="int32" )
#print_image('pizza2.png')
#print_animated('rickroll-rick.gif')
print_camera()
