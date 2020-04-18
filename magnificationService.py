import numpy as np
import cv2 
import math
from pathTracker import pathTracker


class magnificationService:

    def __init__(self, input_image, scale_factor, magnificationLevel=4, cropLevel=70):
        self.cropLevel = cropLevel
        self.magnificationLevel = magnificationLevel
        self.input_image=input_image
        self.selectedLocation = []
        self.scale_factor=scale_factor
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))

    def draw_path(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            #cv2.circle(self.img,(x,y) , 10, (0,255,255), 4)
            self.selectedLocation.append((x,y))


    def tester(self, theta):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)
        while(len(self.selectedLocation) < 1):

            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        result = self.magnify(self.selectedLocation[0], theta)
        while(True):
            cv2.imshow('output',result)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    
    def magnify(self,point, theta):
        self.drawBot(point, theta)
        result = self.img[int(point[1]-self.cropLevel):int(point[1]+self.cropLevel),int(point[0]-self.cropLevel):int(point[0]+self.cropLevel)]
        result = cv2.resize(result,(int(result.shape[1]*self.magnificationLevel),int(result.shape[0]*self.magnificationLevel)))

        return result

    def drawBot(self,point,theta, radius = 4):
        cv2.circle(self.img,(point[0],point[1]) , radius, (255,0,0), 5)
        angle = np.deg2rad(theta - 25) 
        angle2 = np.deg2rad(theta + 25) 
        ep1 = point[0] + int(radius*(np.sin(angle)))
        ep2 = point [1] + int(radius*(np.cos(angle)))
        ep3 = point[0] + int((radius+10)*(np.sin(angle)))
        ep4 = point [1] + int((radius+10)*(np.cos(angle)))
        ep5 = point[0] + int(radius*(np.sin(angle2)))
        ep6 = point [1] + int(radius*(np.cos(angle2)))
        ep7 = point[0] + int((radius+10)*(np.sin(angle2)))
        ep8 = point [1] + int((radius+10)*(np.cos(angle2)))
        b = pathTracker()
        print(b.getAngle([(ep5,ep6),(ep7,ep8)],1))
        angle = b.getAngle([(ep5,ep6),(ep7,ep8)],1)
        if (ep5 >= ep7) and (ep6 >= ep8):
            print("1")
            print(str(angle + 90))
        cv2.line(self.img,(ep1,ep2),(ep3,ep4),(255,0,0),2)
        cv2.line(self.img,(ep5,ep6),(ep7,ep8),(255,0,0),2)


a = magnificationService('physics_corrected.jpg',0.7,4,70)

a.tester(180)