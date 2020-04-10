import numpy as np
import cv2 
drawing_mode = False # true if mouse is pressed
ix,iy = -1,-1
save_permission = "Denied"
Entry_mode = "Line"
path_coordinates_X = []
path_coordinates_Y = []
img = cv2.imread('physics_corrected.jpg',0)


def draw_path(event,x,y,flags,param):
    global path_coordinates_X
    global path_coordinates_Y

    if event == cv2.EVENT_LBUTTONDOWN:
        path_coordinates_X.append(x)
        path_coordinates_Y.append(y)




def draw_line():
    global path_coordinates_X
    global path_coordinates_Y
    if len(path_coordinates_X) == 2:
        cv2.line(img,(path_coordinates_X[0],path_coordinates_Y[0]),(path_coordinates_X[1],path_coordinates_Y[1]),(0,0,255),10)
        path_coordinates_X = []
        path_coordinates_Y = []
    else:
        pass


cv2.namedWindow('image')
path_coordinates_X = []
path_coordinates_Y = []
cv2.setMouseCallback('image',draw_path)


while(True):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    draw_line()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()