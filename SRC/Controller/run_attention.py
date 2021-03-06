try:
    print("Elementary imports: ")
    import os
    import json
    import glob
    import argparse
    
    print("numpy/scipy imports:")
    import numpy as np
    from scipy import signal as sg
    import scipy.ndimage as ndimage
    from scipy.ndimage.filters import maximum_filter
    
    print("PIL imports:")
    from PIL import Image
    
    print("matplotlib imports:")
    
    import matplotlib.pyplot as plt
    
except ImportError:
    print("Need to fix the installation")
    raise

print("All imports okay. Yay!")


def find_tfl_lights(c_image: np.ndarray):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """

    red_x, red_y, green_x, green_y = find_light_sources_candidates(c_image)
    marking_the_coordinates(c_image, red_x, red_y, 'red')
    marking_the_coordinates(c_image, green_x, green_y, 'green')
    
    return red_x, red_y, green_x, green_y
    

def show_image_and_gt(image, objs, fig_num=None):
    plt.figure(fig_num).clf()
    plt.imshow(image)
    labels = set()
    
    if objs is not None:
        
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        
        if len(labels) > 1:
            plt.legend()


def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """

    image = np.array(Image.open(image_path))

    if json_path is None:
        objects = None
    
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]
        
    show_image_and_gt(image, objects, fig_num)
    
    red_x, red_y, green_x, green_y = find_tfl_lights(image)
    plt.plot(red_x, red_y, 'ro', color='r', markersize=4)
    plt.plot(green_x, green_y, 'ro', color='g', markersize=4)


def get_kernel():
    return np.array([[-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, 8 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324],
                    [-1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1 / 324, -1/324, -1/324, -1/324]])  # Gx + j*Gy


def get_maximum_points(image):
    dX, dY = 18, 18
    M, N = image.shape
    list_x = ()
    list_y = ()
    
    for x in range(0, M - dX + 1, dX):
        for y in range(0, N - dY + 1, dY):
            window = image[x:x + dX, y:y + dY]
            local_max = np.amax(window)
            max_coord = np.argmax(window)
            
            if local_max > 65:
                coord_x = x + max_coord // dX
                coord_y = y + max_coord % dX
                list_x += (coord_x,)
                list_y += (coord_y,)
                
    return list_x, list_y
    

def get_lights_coordinates(convert_image):
    kernel = get_kernel()
    grad = sg.convolve2d(convert_image, kernel, boundary='symm', mode='same')
    axis_x, axis_y = get_maximum_points(grad)
    plt.show()
    
    return axis_x, axis_y
    

def marking_the_coordinates(image, axis_x, axis_y, name_color):
    image = np.array(image)
    
    if name_color == 'red':
        color = [255, 0, 0]
    
    elif name_color == 'green':
        color = [0, 255, 0]

    else:
        color = [255, 255, 255]
    
    for i in range(len(axis_x)):
        image[axis_x[i]: axis_x[i] + 8, axis_y[i]: axis_y[i] + 8] = [[color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color],
                                                                        [color, color, color, color, color, color, color, color]]
    Image.fromarray(image).show()


def find_light_sources_candidates(image):
    red_image = np.array(image)[:, :, 0]
    red_x, red_y = get_lights_coordinates(red_image)
    green_image = np.array(image)[:, :,  1]
    green_x, green_y = get_lights_coordinates(green_image)

    return red_x, red_y, green_x, green_y


def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""

    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = 'data'
    
    if args.dir is None:
        args.dir = default_base

    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    
    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        
        if not os.path.exists(json_fn):
            json_fn = None

        test_find_tfl_lights(image, json_fn)
    
    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    
    else:
        print("Bad configuration?? Didn't find any picture to show")

    plt.show(block=True)


if __name__ == '__main__':
    main()
