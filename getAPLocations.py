import numpy as np
import cv2 


class getAPLocations:

    def __init__(self, image_address, output_address):
        self.image_path  = image_address
        self.output_address = output_address
        self.drawing_mode = False # true if mouse is pressed
        self.ix,self.iy = -1,-1
        self.locationMatrix = []
        self.path_coordinates_X = []
        self.path_coordinates_Y = []
        self.labels = ['AP1', 'AP2', 'AP3']
        self.img = cv2.imread(self.image_path,0)


    def getAPDone(self):
        self.getAPCoordinates()
        finalAPLocations = self.apDictionary()
        image_to_save = self.draw_APs(finalAPLocations)
        self.saveAPPicture(image_to_save)
        cv2.destroyAllWindows()
        return finalAPLocations


    def draw_APs(self,APLocations):
        radius = 30
        color = (0, 0, 255) 
        thickness = 4


        image_to_save = cv2.circle(self.img,(APLocations['AP1'][0],APLocations['AP1'][1]) , radius, color, thickness) 
        cv2.circle(image_to_save,(APLocations['AP2'][0],APLocations['AP2'][1]) , radius, color, thickness) 
        cv2.circle(image_to_save,(APLocations['AP3'][0],APLocations['AP3'][1]) , radius, color, thickness) 
        return image_to_save


    def saveAPPicture(self, image):
        cv2.imwrite(self.output_address, image )

     

    def draw_path(self,event,x,y,flags,param):
        

        if event == cv2.EVENT_LBUTTONDOWN:
            self.path_coordinates_X.append(x)
            self.path_coordinates_Y.append(y)


    def getAPCoordinates(self):
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)

        while(len(self.path_coordinates_X) < 3):
            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def apDictionary(self):
        output = {}

        for i in range(3):
            output[self.labels[i]] = [self.path_coordinates_X[i], self.path_coordinates_Y[i]]

        return output

    def showOutput(self):
        output = cv2.imread(self.output_address,0)

        while(True):
            cv2.imshow('output',output)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


