from PIL import Image
from math import floor

def convert_image(in_name, resize_factor, mode):
    
    # Method for deciding pixel value
    def convert_pixel(r, g, b, column, is_even_row, mode):
        # Offset mode
        if mode == 0:
            if column == 0:
                return [(r, 0, 0), (0, g, 0)][is_even_row]
            elif column == 1:
                return [(0, g, 0), (0, 0, b)][is_even_row]
            else:
                return [(0, 0, b), (r, 0, 0)][is_even_row]
        # Vertical mode
        elif mode == 1:
            if column == 0:
                return (r, 0, 0)
            elif column == 1:
                return (0, g, 0)
            else:
                return (0, 0, b)
        # Red only mode
        elif mode == 2:
            if column == 0:
                return (r, 0, 0)
            else:
                return (0, 0, 0)
        # Green only mode
        elif mode == 3:
            if column == 1:
                return (0, b, 0)
            else:
                return (0, 0, 0)
        # Blue only mode
        elif mode == 4:
            if column == 2:
                return (0, 0, g)
            else:
                return (0, 0, 0)
        # Default to black pixel
        else:
            return (0, 0, 0)
    
    print('Beginning conversion...')
    # Load image
    im = Image.open(in_name)
    print('File opened')

    # Resize to get pixelation
    # Reduce size
    small_im = im.resize((int(im.width/resize_factor),int(im.height/resize_factor)), resample = Image.BOX)
    # Increase size
    big_im = small_im.resize((small_im.width*3,small_im.height*3), resample = Image.BOX)
    print('Image resized')

    # Load pixels to modify
    rgb_im = big_im.convert('RGB')
    pixels = rgb_im.load()

    # Loop through every pixel:
    for x in range(rgb_im.width):
        print('Coverting row '+str(x+1)+' of '+str(rgb_im.width))
        for y in range(rgb_im.height):
            # Only one of the RGB channels will have data in each pixel
            r,g,b = rgb_im.getpixel((x,y))
            pixels[x, y] = convert_pixel(r, g, b, x % 3, floor(y/3) % 2 == 0, mode)
            

    print('Conversion successful!')
    
    # Return output
    return rgb_im.resize((small_im.width*3,small_im.height*3), resample = Image.BOX)
    

    

if __name__ == '__main__':
    print('--= Wecome to the Pointillistic image converter by Trent Baker! =--')
    print('#'*80)
    print('Ensure that your input image is in the same directory as this file.')
    in_name = input('Please enter the input image name with file extension (ex. input.jpg): ')
    out_name = input('Please enter the name of the output file WITHOUT file extension\n(ex. typing \'out\' will save as \'out.png\'): ')
    resize_factor = int(input('Please enter the output sub-pixel size (must be multiple of 3): '))
    print('Finally, please select the conversion mode.')
    print('''------------------------------
Mode 0 = Offset (recommended)
Mode 1 = Vertical
Mode 2 = Red only
Mode 3 = Green only
Mode 4 = Blue only
''')
    mode = int(input('Enter mode (0-4): '))
    out_im = convert_image(in_name, resize_factor, mode)
    out_im.save(out_name+'.png')
    print('Output saved as '+ out_name+'.png')
    
    