import cv2
import numpy as np
import Serial_Comm

# File Main
def frontMain(currImage:np.array):
    '''Main File fo this section. Called in main to get intended functionality out of functions'''
    # Get green filtered image
    greenImage = filter_around_green(currImage=currImage)
    
    # Segment for boundaries in the gree image
    segmentedImage = segment_for_path(green_filtered_image=greenImage)
    
    # Draw the boundaries on the image
    preprocessedImage, leftBorder, rightBorder = drawMargins(currImage=segmentedImage)
    
    # process the image and it's boundary info, then return the result
    left, right = processMargins(currImage=preprocessedImage, leftBorder=leftBorder, rightBorder=rightBorder)
    
    # Check for the farthest in
    
    if (left[0][2] > right[0][2]):
        Serial_Comm.send("l:" + str(left[0][2]) + "\n")
    elif (left[0][2] > right[0][2]):
        Serial_Comm.send("r:" + str(right[0][2]) + "\n")
    else:
        # if the left encroachment is greater
        if(left[0][0] > right[0][0]):
            # Send level of turn information to the Arduino
            Serial_Comm.send("l:" + str(left[0][2]) + "\n")
            
        # if the right encroachment is greater
        elif (left[0][0] < right[0][0]):
            Serial_Comm.send("r:" + str(right[0][2]) + "\n")
    
        

def processMargins(currImage:np.array, leftBorder, rightBorder):
    '''
    Function to Take the image with the boundaries drawn in 
    and process the image for depth information based on those boundaries
    '''
    left_depth = []
    right_depth = []
    # print(f"Searching within range: {(leftBorder[0,1], leftBorder[1,1])}")
    # Check for farthest in black pixel on the left 
    for i in range(leftBorder[0,1], leftBorder[1,1], 5):
        # generate horizontal bonudary location for that height
        # Using line equation: X_2 + slope*(Y_curr - Y_1) .... It works that's all
        j =  int(leftBorder[1,0] + (0.1 * (i - leftBorder[0,1]) ))
        # Search from border
        if currImage[i,j] == 0:
        # print("Left Search\n:Pixel of interest detected")
            # Move farthr into image to find deepest black pixel
            curr = j
            while currImage[i,curr] == 0:
                curr += 1
            # update the farthest depth
            left_depth.append((i, j, curr - j))

    # check for the farthest in black pixel on the right
    for i in range(rightBorder[0,1], rightBorder[1,1], 5):
        # generate horizontal bonudary location for that height
        # Using line equation: X_2 - slope*(Y_curr - Y_1) .... It works that's all
        j =  int(rightBorder[1,0] - (0.1 * (i - rightBorder[0,1]) ))
        if currImage[i,j] == 0:
            # Move in to find the farthest depth
            curr = j
            while currImage[i,curr] == 0:
                curr -= 1
            # update the farthest depth
            right_depth.append((i, j, j - curr))

    # Create intermediate list index for the largest relative distance
    l = np.array([k for i,j,k in left_depth])
    r = np.array([k for i,j,k in right_depth])

    # return max depth for lef_depth and min depth for te right search
    return left_depth[l.argmax()], right_depth[r.argmin()]


def drawMargins(currImage:np.array):
    '''
    Function to draw the brder margins on an image
    :param currImage: Images passed in
    :return: image with margins drawn
    '''
    # get dimensions
    h, w = currImage.shape

    # Set baseline for border widths
    leftWidth = int(w * 0.39)
    rightWidth = int(w * 0.65)

    # Define line endpoints with boundaries
    left = np.array([[leftWidth, 300], [leftWidth - 30, h]])
    right = np.array([[rightWidth, 300], [rightWidth + 30, h]])

    # draw the lines
    currImage = cv2.line(currImage, left[0], left[1], [0, 0, 0], 2)
    currImage = cv2.line(currImage, right[0], right[1], [0, 0, 0], 2)

    # Update the boundary information for the preprocessing step to come
    left = np.array([[leftWidth, 450], [leftWidth - 30, h]])
    right = np.array([[rightWidth, 450], [rightWidth + 30, h]])
    
    # return image
    return currImage, left, right
    


def filter_around_green(currImage : np.array):
    '''
    Function which returns an image with the rio (area between green segments) filtered for
    :param currImage: The frame/image being considered
    :return: filtered image
    '''
    currImage = cv2.cvtColor(currImage, cv2.COLOR_BGR2HSV)

    # convert RGB to green
    greenRGB = np.array([[[0, 255, 0]]], dtype=np.uint8)
    greenHSV = cv2.cvtColor(greenRGB, cv2.COLOR_BGR2HSV)

    # define the range for green
    hue = greenHSV[0, 0, 0]
    lower_hue = int(hue - 30)
    upper_hue = int(hue + 30)

    # kernel for erosion and dilation
    kernel = np.ones((5, 5), dtype=np.uint8)

    # get as mask of the green region in the image
    mask_green = cv2.inRange(currImage, (lower_hue, 0, 0), (upper_hue, 255, 255))

    # Erode
    mask_green = cv2.erode(mask_green, kernel, iterations=5)

    # Dilate
    mask_green = cv2.dilate(mask_green, kernel, iterations=1)

    # threshold the image for inversion
    _, thres = cv2.threshold(mask_green, 20, 255, cv2.THRESH_BINARY_INV)

    # erode the image, to smoothen the balck areas
    eroded = cv2.erode(thres, kernel, iterations=1)

    return eroded

def segment_for_path(green_filtered_image : np.array):
    '''
    Function takes in the filtered image and defines boundaries around the region of interest
    :param green_filtered_image: Image that has been filted for a path around the green
    :return:
    '''

    # define a bounding region for the image
    h, w = green_filtered_image.shape[:2]          # height and width
    poly = np.array([(int(w*0.37), 300), (int(w*0.67),300), (int(w*0.87), h), (int(w*0.17), h)])

    # define a mask (size) of the image
    mask = np.zeros_like(green_filtered_image)

    # Define region of interest
    rio = cv2.fillPoly(mask, [poly], 255)

    # Mask the image for the region of interest
    masked_image = cv2.bitwise_and(green_filtered_image, green_filtered_image, mask=rio)

    return masked_image