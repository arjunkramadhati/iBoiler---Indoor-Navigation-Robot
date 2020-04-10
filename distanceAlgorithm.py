import numpy 
from numpy import linalg as LA
from scipy.spatial import distance
import cv2

class distanceAlgorithm:

    def __init__(self, apLocations, legalPoints):
        self.accessPointOne = apLocations['AP1']
        self.accessPointTwo = apLocations['AP2']
        self.accessPointThree = apLocations['AP3']
        self.legalPoints =legalPoints
        self.distanceDictionary = {}
        self.trylist = []
        
    def getFingerprints(self):
        c=cv2.imread('physics_corrected.jpg',0)
        for i in range(len(self.legalPoints)):
            t = self.calculateDistance(self.legalPoints[i])
            d1 = (t[0]/1200)* 255 
            d2 = (t[1]/1200)* 255 
            d3 = (t[2]/1200)* 255 
            cv2.circle(c,(self.legalPoints[i][0],self.legalPoints[i][1]),2,(d1,d2,d3),2 )
            #self.trylist.append(self.calculateDistance(self.legalPoints[i]))
            #self.distanceDictionary[self.calculateDistance(self.legalPoints[i])] = self.legalPoints[i]
        cv2.imwrite('try.jpg',c)
        #print(self.distanceDictionary)           
        
    def calculateDistance(self, point):
        distance_apOne = distance.euclidean(self.accessPointOne,point)
        distance_apTwo = distance.euclidean(self.accessPointTwo,point)
        distance_apThree = distance.euclidean(self.accessPointOne,point)
        return (distance_apOne,distance_apTwo,distance_apThree)

