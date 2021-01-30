import cv2
import numpy as np

def nothing(x):
    pass

def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):
    
    # Apply the following steps to img
    # 1) Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2) Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

    # 3) Calculate the magnitude
    abs_sobelxy = np.sqrt(sobelx**2 + sobely**2)

    # 4) Scale to 8-bit (0 - 255) and convert to type = np.uint8
    scaled_sobel = np.uint8(255 * abs_sobelxy / np.max(abs_sobelxy))

    # 5) Create a binary mask where mag thresholds are met
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= mag_thresh[0]) & (scaled_sobel <= mag_thresh[1])] = 255
    
    # 6) Return this mask as your binary_output image
    return binary_output

# define a window
window_name = 'Magnitude of the Gradient'
cv2.namedWindow(window_name)

# Read the image
img = cv2.imread('signs_vehicles_xygrad.png')

# create trackbars
cv2.createTrackbar('thresh_min',window_name,0,255,nothing)
cv2.createTrackbar('thresh_max',window_name,0,255,nothing)
cv2.createTrackbar('sobel_kernel', window_name,1,31,nothing)

while(1):

    # get current positions of our trackbars
    thresh_min = cv2.getTrackbarPos('thresh_min',window_name)
    thresh_max = cv2.getTrackbarPos('thresh_max',window_name)
    sobel_kernel = cv2.getTrackbarPos('sobel_kernel',window_name)

    # kernel must be odd, so subtract 1 if parameter is even
    sobel_kernel = sobel_kernel - 1 if (sobel_kernel % 2) == 0 else sobel_kernel

    # Run the function
    grad_binary = mag_thresh(img, sobel_kernel=sobel_kernel, mag_thresh=(thresh_min, thresh_max))

    # show the image
    cv2.imshow(window_name, grad_binary)

    # wait 1 sec on keypress = (esc)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()