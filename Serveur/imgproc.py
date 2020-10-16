""" Second part with EC2 and image processing """
from skimage.io import imread, imsave
from skimage.morphology import dilation, erosion, square
from skimage.color import rgb2gray

def detect_edges(img_path):
    # read image
    img = imread(img_path)

    # convert to grayscale
    gray_img = rgb2gray(img)

    # process image
    dilated = dilation(gray_img, square(3))
    erosed = erosion(gray_img, square(3))
    gradient = dilated - erosed

    # save modified image
    imsave("/home/arnaud/Pictures/after_processing.png", gradient)


""" Test """

detect_edges("/home/arnaud/Pictures/test_gradient.tiff")