import numpy 
from numpy import linalg as LA
from scipy.spatial import distance
import cv2
from scipy.stats import nakagami 
from databaseManager import databaseManager
from rssAlgorithm import rssAlgorithm
from sklearn.neighbors import NearestNeighbors


class locationServices:

    def __init__(self,fingerprintDict, apLocations, legalPoints,RSS0, nakagamiA, nakagamiB, magnificationLevel):
        self.selectedLocation = []
        self.fingerprintDict = fingerprintDict
        self.RSS0 = RSS0
        self.nakagamiA = nakagamiA
        self.nakagamiB = nakagamiB
        self.apLocations = apLocations
        self.legalPoints =legalPoints
        self.magnificationLevel = magnificationLevel
        self.rssHelper = rssAlgorithm(self.apLocations,self.legalPoints,self.RSS0,self.nakagamiA,self.nakagamiB)
        self.getKNNReady()

    def getKNNReady(self):
        self.knnHelper = NearestNeighbors(n_neighbors=1)
        self.data_set = list(self.fingerprintDict.keys())
        self.knnHelper.fit(self.data_set)

    def getCircularPoints(self,x,y):
            self.selectedLocation.append((x,y))
            self.selectedLocation.append((x+1,y))
            self.selectedLocation.append((x-1,y))
            self.selectedLocation.append((x,y+1))
            self.selectedLocation.append((x,y-1))
            self.selectedLocation.append((x+1,y-1))
            self.selectedLocation.append((x+1,y+1))
            self.selectedLocation.append((x-1,y-1))
            self.selectedLocation.append((x-1,y+1))


    def draw_path(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.img,(x,y) , 10, (0,255,255), 4)
            self.getCircularPoints(x,y)

    def testLocation(self, inputImage, scale_factor):
        self.scale_factor =scale_factor
        self.input_image = inputImage
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)
        while(True):
            if len(self.selectedLocation) >=1:
                
                point = self.getCurrentLocation(self.selectedLocation)
                self.selectedLocation=[]
                cv2.circle(self.img,(point[0],point[1]) , 10, (0,0,255), 4)


            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        '''
        while(True):
            if len(self.selectedLocation) >=1:
                
                locations = self.getCurrentLocation(self.selectedLocation)
                self.selectedLocation=[]
                for point in locations:
                    cv2.circle(self.img,(point[0],point[1]) , 10, (0,0,255), 4)


            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                '''
        cv2.destroyAllWindows()
        

    def locationKNN(self,data_set,point):
        lKNN=NearestNeighbors(n_neighbors=1)
        lKNN.fit(data_set)
        return lKNN.kneighbors([point],return_distance=False)

    def getCurrentLocation(self,points, iter = 10):
        locations =[]
        for i in range(iter):
            for point in points:
                rssTuple = tuple(self.rssHelper.calculateRSS(point))
                locations.append(self.fingerprintDict[self.data_set[self.getKNN(rssTuple)[0][0]]])
        location = locations[self.locationKNN(locations,points[0])[0][0]]
        return location

    def getKNN(self,rssTuple):
        return self.knnHelper.kneighbors([rssTuple], return_distance=False)


saver = databaseManager('Database/db')
ls = locationServices(saver.getDbEntry('L5'),saver.getDbEntry('L1'),saver.getDbEntry('L2'),10,4.32,3.18,8)
ls.testLocation('physics_corrected.jpg',0.7)
