import cv2
import numpy as np
import sys
shapeDict = {-1:'none', 
        0:'pentagon',
        1:'octagon',
        2:'hexagon',
        3:'circle',        
        4:'square',
        5:'rectangular'}
def approx2shape(approx):
    vertexCount = approx.shape[0]
    
    if vertexCount == 5:
        return 0
    elif vertexCount == 8:
        return 1
    elif vertexCount == 6:
        return 2
    elif vertexCount == 4:
        e1 = np.linalg.norm(approx[0] - approx[1])
        e2 = np.linalg.norm(approx[1] - approx[2])
        rate = 1.2
        if e1 > e2 * rate or e1 < e2 / rate:
            return 5
        else:
            return 4

        return 4
    elif vertexCount >= 10:
        return 3
    return -1;

def findLargestContour(contours):
    if contours is None:
        retrun -1,None
    if len(contours) == 0:
        retrun -1,None
    maxPerimeter = sys.float_info.min
    maxIndex = -1
    for i in np.arange(len(contours)):
        contour = contours[i]
        
        #area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        #M = cv2.moments(contour)
        #cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00'] 

        if(perimeter > maxPerimeter):
            maxIndex = i
    return maxIndex,contours[maxIndex]

def getShape(image):
    #image.show()
    try:
        if hasattr(image, "shape"):
            if len(image.shape) == 3:

                img2gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

                _, thresh = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                contours, hierarchy = cv2.findContours(thresh, 3, 2)

                miaxIndex,maxContour = findLargestContour(contours)
                if maxContour is None:
                    return shapeDict[-1]
                epsilon = 0.01*cv2.arcLength(maxContour,True)
                approx = cv2.approxPolyDP(maxContour,epsilon,True)

                return shapeDict[approx2shape(approx)]
        
        return shapeDict[-1]
    except cv2.error as e:
        print(e)
        return shapeDict[-1]

def test():
    image = cv2.imread("D:/DevelopProj/Dadao/ESP32Project/Datasets/Shapes/Dst/tfrecord/shapes_photos/5/5_15.jpg")
    ret = getShape(image)
    print(ret)

if __name__ == '__main__':
    test()