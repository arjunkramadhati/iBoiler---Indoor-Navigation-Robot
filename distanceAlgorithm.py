import numpy 
from numpy import linalg as LA
from scipy.spatial import distance
import cv2

class distanceAlgorithm:

    def __init__(self, apLocations, legalPoints, input_image, output_address, scale_factor):
        self.input_image = input_image
        self.output_address = output_address
        self.scale_factor =scale_factor
        self.accessPointOne = apLocations['AP1']
        self.accessPointTwo = apLocations['AP2']
        self.accessPointThree = apLocations['AP3']
        self.legalPoints =legalPoints
        self.fingerprintDictionary = {}
        self.trylist = []
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))


    def getFingerprintDone(self):
        self.getFingerprints()
        self.saveOutput()
        return self.fingerprintDictionary


    def getFingerprints(self):

        for i in range(len(self.legalPoints)):
            t = self.calculateDistance(self.legalPoints[i])
            self.fingerprintDictionary[t] = self.legalPoints[i]
            d1 = (t[0]/1200)* 255 
            d2 = (t[1]/1200)* 255 
            d3 = (t[2]/1200)* 255 
            cv2.circle(self.img,(self.legalPoints[i][0],self.legalPoints[i][1]),2,(d1,d2,d3),2 )
        
    def saveOutput(self):
        cv2.imwrite(self.output_address,self.img)
        
    def calculateDistance(self, point):
        distance_apOne = distance.euclidean(self.accessPointOne,point)
        distance_apTwo = distance.euclidean(self.accessPointTwo,point)
        distance_apThree = distance.euclidean(self.accessPointOne,point)
        return (distance_apOne,distance_apTwo,distance_apThree)

