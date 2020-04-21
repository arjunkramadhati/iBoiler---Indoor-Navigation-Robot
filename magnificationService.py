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

    def reInit(self):
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
        result = self.magnify((1,1),self.selectedLocation[0], theta)
        while(True):
            cv2.imshow('output',result)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    
    def magnify(self,wp,point, theta):
        self.drawBot(wp,point, theta)
        result = self.img[int(point[1]-self.cropLevel):int(point[1]+self.cropLevel),int(point[0]-self.cropLevel):int(point[0]+self.cropLevel)]
        result = cv2.resize(result,(int(result.shape[1]*self.magnificationLevel),int(result.shape[0]*self.magnificationLevel)))

        return result

    def getOriginalSize(self):
        #cv2.circle(self.img,(wp[1],wp[0]),5,(0,0,255),5)
        return self.img

    #def getBotLocComparison(self,point,theta):
        #self.drawBot(point,theta,(0,0,255))



    def drawBot(self,wp,point,theta, radius = 4, color = (255,0,0)):
        cv2.circle(self.img,(wp[1],wp[0]),5,(0,0,255),5)
        cv2.circle(self.img,(point[0],point[1]) , radius, color, 5)
        angle = theta - 0.436332
        angle2 = theta + 0.436332 
        angleTest = theta 
        radius2= radius+10
        ept1=int( point[0] + radius*(np.cos(angleTest)))
        ept2=int( point[1] + radius*(np.sin(angleTest)))
        ep1 = int(point[0] + radius*(np.cos(angle)))
        ep2 = int(point [1] + (radius*(np.sin(angle))))
        ep3 = int(point[0] + (radius2*(np.cos(angle))))
        ep4 = int(point [1] + (radius2*(np.sin(angle))))
        ep5 = int(point[0] + radius*(np.cos(angle2)))
        ep6 = int(point [1] + radius*(np.sin(angle2)))
        ep7 = int(point[0] + (radius+10)*(np.cos(angle2)))
        ep8 = int(point [1] + (radius+10)*(np.sin(angle2)))
        #b = pathTracker()
        #print(b.getAngle([(point[0],point[1]),(ep5,ep6)],1))
        '''angle = b.getAngle([(ep5,ep6),(ep7,ep8)],1)
        if (ep5 >= ep7) and (ep6 >= ep8):
            print("1")
            print(str(angle + 90))'''
        
        if(point[0]>ept1) and (point[1]>ept2):
            print("Target towards NW")
        if(point[0]<ept1) and (point[1]<ept2):
            print("Target towards SE")
        if(point[0]>ept1) and (point[1]<ept2):
            print("Target towards NE")
        if(point[0]<ept1) and (point[1]>ept2):
            print("Target towards SW")
        cv2.circle(self.img,(ept1,ept2) , 1, (0,0,255), 5)
        
        cv2.line(self.img,(ep1,ep2),(ep3,ep4),color,2)
        cv2.line(self.img,(ep5,ep6),(ep7,ep8),color,2)


'''
a = magnificationService('physics_corrected.jpg',0.7,4,70)

a.tester(0)
'''