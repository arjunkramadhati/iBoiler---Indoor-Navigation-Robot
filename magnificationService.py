import numpy as np
import cv2 

class magnificationService:

    def __init__(self, input_image, scale_factor, magnificationLevel, cropLevel):
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
            cv2.circle(self.img,(x,y) , 10, (0,255,255), 4)
            self.selectedLocation.append((x,y))


    def tester(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)
        while(len(self.selectedLocation) < 1):

            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        result = self.magnify(self.selectedLocation[0])
        while(True):
            cv2.imshow('output',result)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    
    def magnify(self,point):
        result = self.img[int(point[1]-self.cropLevel):int(point[1]+self.cropLevel),int(point[0]-self.cropLevel):int(point[0]+self.cropLevel)]
        result = cv2.resize(result,(int(result.shape[1]*self.magnificationLevel),int(result.shape[0]*self.magnificationLevel)))

        return result




a = magnificationService('physics_corrected.jpg',0.7,5,100)
a.tester()