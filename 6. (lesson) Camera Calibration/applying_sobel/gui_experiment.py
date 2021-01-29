import cv2
import numpy as np

def nothing(x):
    pass

def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    # Apply the following steps to img

    # 1) Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2) Take the derivative in x or y given orient = 'x' or 'y'
    if orient == 'x':
        derivative = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    if orient == 'y':
        derivative = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

    # 3) Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(derivative)

    # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    # 5) Create a mask of 1's where the scaled gradient magnitude 
            # is > thresh_min and < thresh_max
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # 6) Return this mask as your binary_output image
    return binary_output

# define a window
cv2.namedWindow('image')

# Read the image
img = cv2.imread('signs_vehicles_xygrad.png')

# create trackbars for color change
cv2.createTrackbar('thresh_min','image',0,255,nothing)
cv2.createTrackbar('thresh_max','image',0,255,nothing)

# # create switch for ON/OFF functionality
# orient = 'orient : OFF \n1 : ON'
# cv2.createTrackbar(orient, 'image',0,1,nothing)

while(1):

    # get current positions of our trackbars
    thresh_min = cv2.getTrackbarPos('thresh_min','image')
    thresh_max = cv2.getTrackbarPos('thresh_max','image')

    # Run the function
    grad_binary = abs_sobel_thresh(img, orient='x', thresh_min=20, thresh_max=100)

    cv2.imshow('image', grad_binary)
    print('done')

    k = cv2.waitKey(2000) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()