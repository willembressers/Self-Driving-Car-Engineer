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
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 255

    # 6) Return this mask as your binary_output image
    return binary_output

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

def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    
    # Apply the following steps to img
    # 1) Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2) Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

    # 3) Take the absolute value of the x and y gradients
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)

    # 4) Use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the gradient 
    direction = np.arctan2(abs_sobely, abs_sobelx)

    # 5) Create a binary mask where mag thresholds are met
    binary_output = np.zeros_like(direction)
    binary_output[(direction >= thresh[0]) & (direction <= thresh[1])] = 255

    # 6) Return this mask as your binary_output image
    return binary_output

# define a window
window_name = 'Combining thresholds'
cv2.namedWindow(window_name)

# Read the image
img = cv2.imread('signs_vehicles_xygrad.png')

# create (abs_sobel_thresh) trackbars
cv2.createTrackbar('sobel_thresh_min', window_name, 0, 255, nothing)
cv2.createTrackbar('sobel_thresh_max', window_name, 0, 255, nothing)

# create (mag_thresh) trackbars
cv2.createTrackbar('magnitude_thresh_min', window_name, 0, 255, nothing)
cv2.createTrackbar('magnitude_thresh_max', window_name, 0, 255, nothing)
cv2.createTrackbar('magnitude_sobel_kernel',  window_name, 1, 31, nothing)

# create (dir_threshold) trackbars
granularity = 100
cv2.createTrackbar('direction_thresh_min', window_name, 0, int((np.pi / 2) * granularity), nothing)
cv2.createTrackbar('direction_thresh_max', window_name, 0, int((np.pi / 2) * granularity), nothing)
cv2.createTrackbar('direction_sobel_kernel', window_name, 1, 31, nothing)

while(1):

    # (abs_sobel_thresh) trackbars
    sobel_thresh_min = cv2.getTrackbarPos('sobel_thresh_min', window_name)
    sobel_thresh_max = cv2.getTrackbarPos('sobel_thresh_max', window_name)

    # (mag_thresh) trackbars
    magnitude_thresh_min = cv2.getTrackbarPos('magnitude_thresh_min',window_name)
    magnitude_thresh_max = cv2.getTrackbarPos('magnitude_thresh_max',window_name)
    magnitude_sobel_kernel = cv2.getTrackbarPos('magnitude_sobel_kernel',window_name)

    # (dir_threshold) trackbars
    direction_thresh_min = cv2.getTrackbarPos('direction_thresh_min', window_name)
    direction_thresh_max = cv2.getTrackbarPos('direction_thresh_max', window_name)
    direction_sobel_kernel = cv2.getTrackbarPos('direction_sobel_kernel', window_name)

    # kernel must be odd, so subtract 1 if parameter is even
    magnitude_sobel_kernel = magnitude_sobel_kernel - 1 if (magnitude_sobel_kernel % 2) == 0 else magnitude_sobel_kernel
    direction_sobel_kernel = direction_sobel_kernel - 1 if (direction_sobel_kernel % 2) == 0 else direction_sobel_kernel

    # Apply each of the thresholding functions
    gradx = abs_sobel_thresh(img, orient='x', thresh_min=sobel_thresh_min, thresh_max=sobel_thresh_max)
    grady = abs_sobel_thresh(img, orient='y', thresh_min=sobel_thresh_min, thresh_max=sobel_thresh_max)
    mag_binary = mag_thresh(img, sobel_kernel=magnitude_sobel_kernel, mag_thresh=(magnitude_thresh_min, magnitude_thresh_max))
    dir_binary = dir_threshold(img, sobel_kernel=direction_sobel_kernel, thresh=(direction_thresh_min / granularity, direction_thresh_max / granularity))

    # combine the functions
    combined = np.zeros_like(dir_binary)
    combined[((gradx == 255) & (grady == 255)) | ((mag_binary == 255) & (dir_binary == 255))] = 255

    # show the image
    cv2.imshow(window_name, combined)

    # wait 1 sec on keypress = (esc)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()