# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import numpy as np
import cv2
import os

import math

def _prepare(img):
    """ prepare proc for edge collection """
    ht, wd, dp = img.shape

    # only care about the horizont block, filter out up high block
    #img[0:int(ht/2),:] = (0, 0, 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gaussian smooth over standard deviation, reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 10) #kernel_size, border
    #display_img(gray)

    # smooth and canny edge detection
    edge = cv2.Canny(gray, 1, 100) # low_threshold, high_threshold
    return edge

def _detect(edge):
    """ find correlation edges for standard line detection """
    lines = cv2.HoughLinesP(edge, 1, np.pi/180, 50, 0, 11) #rho, theta, threshold, min_line_ln, max_line_gap
    draw_lines(img, lines)
    #return line_img

def draw_lines(img, lines):
    """ draw results """
    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    for line in lines:
        for obj in line:
            [x1, y1, x2, y2] = obj
            dx, dy = x2 - x1, y2 - y1
            angle = np.arctan2(dy, dx) * 180/np.pi
            print angle
            if (angle >= 10 or angle <= -10):
                cv2.line(img, (x1,y1), (x2,y2), (255, 0, 0), 3) #colour, thickness
    display_img(img)

def display_img(img):
    """ show img """
    cv2.imshow('houghlinesp_img', img)

#####
imglist = os.listdir("test_images/")
print imglist
for i in range(len(imglist)):
    #reading in an image
    img = cv2.imread('test_images/' + imglist[i])

    # main
    edge = _prepare(img.copy())
    print edge
    lines = _detect(edge)
    print lines
    cv2.waitKey(0)
    cv2.destroyAllWindows()
