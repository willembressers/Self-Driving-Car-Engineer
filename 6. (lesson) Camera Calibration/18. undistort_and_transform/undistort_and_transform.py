import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read in the saved camera matrix and distortion coefficients
# These are the arrays you calculated using cv2.calibrateCamera()
dist_pickle = pickle.load( open( "wide_dist_pickle.p", "rb" ) )
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]

# Read in an image
img = cv2.imread('test_image2.png')
nx = 8 # the number of inside corners in x
ny = 6 # the number of inside corners in y

# MODIFY THIS FUNCTION TO GENERATE OUTPUT 
# THAT LOOKS LIKE THE IMAGE ABOVE
def corners_unwarp(img, nx, ny, mtx, dist):
    # Pass in your image into this function
    # Write code to do the following steps
    
    # 1) Undistort using mtx and dist
    undistorted = cv2.undistort(img, mtx, dist, None, None)

    # 2) Convert to grayscale
    gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

    # 3) Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    # 4) If corners found: 
    if ret == True:

            # a) draw corners
            cv2.drawChessboardCorners(gray, (nx, ny), corners, ret)
            
            # b) define 4 source points src = np.float32([[,],[,],[,],[,]])
                 #Note: you could pick any four of the detected corners 
                 # as long as those four corners define a rectangle
                 #One especially smart way to do this would be to use four well-chosen
                 # corners that were automatically detected during the undistortion steps
                 #We recommend using the automatic detection of corners in your code
            src_top_left = corners[0]
            src_top_right = corners[nx-1]
            src_bottom_left = corners[((nx*ny)-nx)]
            src_bottom_right = corners[(nx*ny)-1]

            src = np.float32([src_top_left, src_top_right, src_bottom_right, src_bottom_left])

            # c) define 4 destination points dst = np.float32([[,],[,],[,],[,]])
            offset = 100
            img_size = (img.shape[1], img.shape[0])

            # define the coordinates
            xmin = offset
            ymin = offset
            xmax = img_size[0] - offset
            ymax = img_size[1] - offset

            # define the rectangle points
            dst_top_left = [xmin, ymin]
            dst_top_right = [xmax, ymin] 
            dst_bottom_left = [xmin, ymax]
            dst_bottom_right = [xmax, ymax]

            # define the rectangle
            dst = np.float32([dst_top_left, dst_top_right, dst_bottom_right, dst_bottom_left])

            # d) use cv2.getPerspectiveTransform() to get M, the transform matrix
            M = cv2.getPerspectiveTransform(src, dst)

            # e) use cv2.warpPerspective() to warp your image to a top-down view
            warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
 
    return warped, M

top_down, perspective_M = corners_unwarp(img, nx, ny, mtx, dist)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=50)
ax2.imshow(top_down)
ax2.set_title('Undistorted and Warped Image', fontsize=50)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.savefig("output.png")
