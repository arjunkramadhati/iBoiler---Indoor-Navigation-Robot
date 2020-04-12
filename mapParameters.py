import cv2
import numpy as np

class mapParameters:

    def __init__(self,image_address, output_address):
        self.image_address = image_address
        self.output_address = output_address
        self.parameterCoordinates = []
        self.parameterName = []
        self.mapParametersDict = {}
        self.image = cv2.imread(self.image_address,0)

    def getmapParameterDone(self):
        self.getmapInfo()
        self.saveOutput()
        cv2.destroyAllWindows()
        return self.mapParametersDict


    def saveOutput(self):
        cv2.imwrite(self.output_address,self.image)

    def drawInfo(self, name,x,y):
        cv2.putText(self.image,name,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)



    def getName(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.parameterCoordinates.append((x,y))
            self.parameterName.append(input("Enter Name of Parameter:"))
            self.mapParametersDict[self.parameterName[-1]] = (x,y)
            self.drawInfo(self.parameterName[-1],x,y)

    def getmapInfo(self):

        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', self.getName)

        while(True):
            cv2.imshow('Image',self.image)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break