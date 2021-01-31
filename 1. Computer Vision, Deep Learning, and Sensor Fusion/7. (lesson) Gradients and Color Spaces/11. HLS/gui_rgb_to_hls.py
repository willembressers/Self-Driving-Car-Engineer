import cv2
import numpy as np

def nothing(x):
    pass

def hls_select(img, thresh=(0, 255)):
    # 1) Convert to HLS color space
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    H = hls[:,:,0]
    L = hls[:,:,1]
    S = hls[:,:,2]  

    # 2) Apply a threshold to the S channel
    binary = np.zeros_like(S)
    binary[(S > thresh[0]) & (S <= thresh[1])] = 255

    # 3) Return a binary image of threshold result
    return binary

# define a window
window_name = 'Combining thresholds'
cv2.namedWindow(window_name)

# Read the image
img = cv2.imread('test6.jpg')

# create (hls_select) trackbars
cv2.createTrackbar('S_thresh_min', window_name, 0, 255, nothing)
cv2.createTrackbar('S_thresh_max', window_name, 0, 255, nothing)

while(1):

    # (hls_select) trackbars
    S_thresh_min = cv2.getTrackbarPos('S_thresh_min', window_name)
    S_thresh_max = cv2.getTrackbarPos('S_thresh_max', window_name)

    # Apply each of the thresholding functions
    binary = hls_select(img, thresh=(S_thresh_min, S_thresh_max))

    # show the image
    cv2.imshow(window_name, binary)

    # wait 1 sec on keypress = (esc)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()