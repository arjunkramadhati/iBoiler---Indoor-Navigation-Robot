from getAPLocations import getAPLocations
from mapGenerator import mapGenerator
from distanceAlgorithm import distanceAlgorithm
from mapParameters import mapParameters
from databaseManager import databaseManager
from rssAlgorithm import rssAlgorithm
import cv2
import numpy 
from numpy import linalg as LA
from scipy.spatial import distance
import cv2
from scipy.stats import nakagami 


class validationMaster:

    def __init__(self,databaseLocation,resultdbLocation, input_image, scale_factor):
        self.databaseLocation = databaseLocation
        self.resultdbLocation = resultdbLocation
        self.input_image = input_image
        self.scale_factor = scale_factor
        self.saver = databaseManager(self.databaseLocation)
        self.result = databaseManager(self.resultdbLocation)
        self.legalPoints = self.saver.getDbEntry('L2')
        self.apArrays = []
        self.apArrayAll = []
        self.referencePoints = []
        self.fingerprintDictionary = {}
        self.fingerprintDictionaryAll = []
        self.nakagamiA = 4.32
        self.nakagamiB = 3.18
        self.RSS0 = 10

    def validationAP(self):
        self.fetchAPArrays()
        print(self.apArrayAll)
        self.fetchReferencePoints()
        self.fetchHeatMaps()
        print(self.fingerprintDictionaryAll)

    def fetchHeatMaps(self):

        for j in range(len(self.apArrayAll)):

            for i in range(len(self.legalPoints)):
                t = tuple(self.calculateRSS(self.legalPoints[i],j))
                self.fingerprintDictionary[t] = self.legalPoints[i]
            
            self.fingerprintDictionaryAll.append(self.fingerprintDictionary)
            self.fingerprintDictionary = {}
 
    def calculateRSS(self, point, j):
        dTuple = self.calculateDistance(point, j)
        return self.getRSS(dTuple)

    def calculateDistance(self,point, j):
        dTuple = []
        for i in range(len(self.apArrayAll[j])):
            d = distance.euclidean(self.apArrayAll[j][i],point)
            dTuple.append(d)
        return dTuple

    def getRSS(self,dTuple):
        rssTuple = []
        for i in range(len(dTuple)):
            noiseG = numpy.random.randn(1)
            noiseNakagami = nakagami.rvs(self.nakagamiA,self.nakagamiB)
            logvalue = 10 * (numpy.log10(dTuple[i]))
            rss = self.RSS0 - logvalue - noiseG[0] - noiseNakagami
            rssTuple.append(rss)
        return rssTuple



    def draw_APs(self):
        radius = 30
        color = (0, 0, 255) 
        thickness = 4
        output = self.img

        for point in self.apArrays:
            cv2.circle(output,(point[0],point[1]),radius,color,thickness)

        while(True):
            cv2.imshow('output',output)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def draw_RPs(self):
        radius = 30
        color = (0, 0, 255) 
        thickness = 4
        output = self.img

        for point in self.referencePoints:
            cv2.circle(output,(point[0],point[1]),radius,color,thickness)

        while(True):
            cv2.imshow('output',output)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def draw_path(self,event,x,y,flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.apArrays.append((x,y))

    def draw_path2(self,event,x,y,flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.referencePoints.append((x,y))


    def fetchAPArrays(self):
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))
        for i in range(3,11,1):
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',self.draw_path)
            print('count ' + str(i))
            while(len(self.apArrays) < i):
                cv2.imshow('image',self.img)
                k = cv2.waitKey(1) & 0xFF
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            print(len(self.apArrays))
            self.apArrayAll.append(self.apArrays)
            self.draw_APs()
            self.apArrays = []
            self.img = cv2.imread(self.input_image,0)
            self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
            self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))

    def fetchReferencePoints(self):
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))

        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path2)
        
        while(len(self.referencePoints) < 30):
            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.draw_RPs()
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))


a = validationMaster('Database/db','Database/dbResult','physics_corrected.jpg',0.7)
a.validationAP()