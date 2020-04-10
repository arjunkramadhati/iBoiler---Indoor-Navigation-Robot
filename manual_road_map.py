import numpy as np
import cv2 
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
path_coordinates_X = []
path_coordinates_Y = []
img = cv2.imread('Scan Mar 7, 2020_page-0001.jpg',0)
img2 = cv2.imread('Scan Mar 7, 2020_page-0001.jpg',0)

def draw_path(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global path_coordinates_X
    global path_coordinates_Y
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        path_coordinates_X.append(x)
        path_coordinates_Y.append(y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            path_coordinates_X.append(x)
            path_coordinates_Y.append(y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print(path_coordinates_X)
        print(path_coordinates_Y)
        path_coordinates_X = []
        path_coordinates_Y = []

def draw_all_points():
    if len(path_coordinates_X) >=2:
        for i in range(0,len(path_coordinates_X)-2):
            cv2.line(img,(path_coordinates_X[i],path_coordinates_Y[i]),(path_coordinates_X[i+1],path_coordinates_Y[i+1]),(0,0,255),10)
    else:
        pass


cv2.namedWindow('image')
path_coordinates_X = []
path_coordinates_Y = []
cv2.setMouseCallback('image',draw_path)


while(True):
    cv2.imshow('image',img)
    cv2.imshow('imag1e',img2)
    k = cv2.waitKey(1) & 0xFF
    draw_all_points()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
