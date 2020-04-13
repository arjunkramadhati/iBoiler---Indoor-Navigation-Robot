from __future__ import print_function
from __future__ import division
import numpy as np
import cv2 

class mapGenerator:

    def __init__(self, image_address, output_address, scale_factor):
        self.image_address = image_address
        self.outputPath = output_address
        self.scale_factor =scale_factor
        self.vertices = []
        self.masterArray =[]
        self.path_coordinates_X = []
        self.path_coordinates_Y = []
        
  


    def getMapDone(self):

        while(input("Continue?") == "Yes"):
            self.img = cv2.imread(self.image_address,0)
            self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))
            self.getLineCoordinatesOuter()
            floorPathImage = self.drawSelectedFloor()
            print('Processing...')
            finalLegalPoints = self.getLegalCoordinates(floorPathImage)
            self.masterArray.append(finalLegalPoints)
            cv2.destroyAllWindows()

        print("You entered the contours a total of : " + str(len(self.masterArray)) + " times" )
        finalLegalPoints = self.masterArray[0]

        for i in range(len(self.masterArray) -1):
            finalLegalPoints = [x for x in finalLegalPoints if x not in self.masterArray[i+1]]
        
        return finalLegalPoints


    def getLegalCoordinates(self,src) :
        filteredLP = []
        contours, _ = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        raw_dist = np.empty(src.shape, dtype=np.float32)
        for i in range(src.shape[0]):
            for j in range(src.shape[1]):
                raw_dist[i,j] = cv2.pointPolygonTest(contours[0], (j,i), True)

        for i in range(src.shape[0]):
            for j in range(src.shape[1]):
                if raw_dist[i,j] > 0:
                    filteredLP.append((j,i))


        
        '''minVal, maxVal, _, maxDistPt = cv2.minMaxLoc(raw_dist)
        minVal = abs(minVal)
        maxVal = abs(maxVal)
        drawing = np.zeros((self.img.shape[0], self.img.shape[1], 3), dtype=np.uint8)
        
        for i in range(src.shape[0]):
            for j in range(src.shape[1]):
                if raw_dist[i,j] < 0:
                    drawing[i,j,0] = 255 - abs(raw_dist[i,j]) * 255 / minVal
                elif raw_dist[i,j] > 0:
                    drawing[i,j,2] = 255 - raw_dist[i,j] * 255 / maxVal
                else:
                    drawing[i,j,0] = 255
                    drawing[i,j,1] = 255
                    drawing[i,j,2] = 255


        while(True):
            cv2.imshow("output", self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break'''

        return filteredLP




    def drawSelectedFloor(self):
        blank_image = np.zeros((self.img.shape[0],self.img.shape[1]), dtype=np.uint8)
        print(self.vertices)

        for i in range(len(self.vertices)):

            cv2.line(blank_image, self.vertices[i], self.vertices[(i+1)%len(self.vertices)], (255,255,255), 10)

        while(True):
            cv2.imshow("floorMap", blank_image)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.vertices = []
                return blank_image
                break



    def draw_path(self,event,x,y,flags,param):
    
        if event == cv2.EVENT_LBUTTONDOWN:
            
            self.path_coordinates_X.append(x)
            self.path_coordinates_Y.append(y)


    def drawLine(self):
        if len(self.path_coordinates_X) == 2:
            self.vertices.append((self.path_coordinates_X[0],self.path_coordinates_Y[0]))
            cv2.line(self.img,(self.path_coordinates_X[0],self.path_coordinates_Y[0]),(self.path_coordinates_X[1],self.path_coordinates_Y[1]),(0,0,255),10)
            self.path_coordinates_X = []
            self.path_coordinates_Y = []
        else:
            pass



        

    def getLineCoordinatesOuter(self):
        print("Taking Outer Loop")
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)

        while(True):
            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            self.drawLine()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




