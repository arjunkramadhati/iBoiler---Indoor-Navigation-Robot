import numpy 
from numpy import linalg as LA
from scipy.spatial import distance
import cv2
from scipy.stats import nakagami 

class rssAlgorithm:

    def __init__(self, apLocations, legalPoints, input_image, output_address, scale_factor,RSS0, nakagamiA, nakagamiB):
        self.input_image = input_image
        self.output_address = output_address
        self.scale_factor =scale_factor
        self.RSS0 = RSS0
        self.numargs = nakagami.numargs
        self.nakagamiA = nakagamiA
        self.nakagamiB = nakagamiB
        self.accessPointOne = apLocations['AP1']
        self.accessPointTwo = apLocations['AP2']
        self.accessPointThree = apLocations['AP3']
        self.legalPoints =legalPoints
        self.fingerprintDictionary = {}
        self.trylist = []
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))


    def getFingerprintDone(self):
        self.getFingerprints()
        self.drawAPs()
        self.saveOutput()
        print(self.fingerprintDictionary)
        return self.fingerprintDictionary

    def drawAPs(self):   
        radius = 30
        color = (0, 0, 255) 
        thickness = 4
        cv2.circle(self.img,self.accessPointOne , radius, color, thickness) 
        cv2.circle(self.img,self.accessPointTwo , radius, color, thickness) 
        cv2.circle(self.img,self.accessPointThree , radius, color, thickness) 
        

    def getFingerprints(self):

        for i in range(len(self.legalPoints)):
            t = tuple(self.calculateRSS(self.legalPoints[i]))
            self.fingerprintDictionary[t] = self.legalPoints[i]
            # maxItem = max(t)
            # d1 = (t[0]/maxItem)* 25(5 
            # d2 = (t[1]/maxItem)* 255 
            # d3 = (t[2]/maxItem)* 255
            t=numpy.array(t)
            d = ((t-numpy.mean(t))/numpy.std(t))*255
            cv2.circle(self.img,(self.legalPoints[i][0],self.legalPoints[i][1]),2,(d[0],d[1],d[2]),2 )
        
    def saveOutput(self):
        cv2.imwrite(self.output_address,self.img)
        
    def calculateRSS(self, point):
        dTuple = self.calculateDistance(point)
        return self.getRSS(dTuple)


    def calculateDistance(self,point):
        distance_apOne = distance.euclidean(self.accessPointOne,point)
        distance_apTwo = distance.euclidean(self.accessPointTwo,point)
        distance_apThree = distance.euclidean(self.accessPointThree,point)
        return (distance_apOne,distance_apTwo,distance_apThree)

    def getRSS(self,dTuple):
        rssTuple = []
        for i in range(3):
            noiseG = numpy.random.randn(1)
            noiseNakagami = nakagami.rvs(self.nakagamiA,self.nakagamiB)
            logvalue = 10 * (numpy.log10(dTuple[i]))
            rss = self.RSS0 - logvalue - noiseG[0] - noiseNakagami
            rssTuple.append(rss)
        return rssTuple


