import numpy as np
import cv2
from databaseManager import databaseManager
from locationServices import locationServices
from planPath import planPath
from pathTracker import pathTracker
from scipy.spatial import distance
from magnificationService import magnificationService
import time

class iBoiler:

    def __init__(self, image_Address, dbLocation, botRadius, botMaxVelocity, botturningVelocity, RSS0, nakagamiA, nakagamiB, scale_factor, timeStep):
        self.dbHelper = databaseManager(dbLocation)
        self.input_image = image_Address
        self.scale_factor = scale_factor
        self.timeStep = timeStep
        self.apLocations = self.dbHelper.getDbEntry('L1')
        self.legalPoints = self.dbHelper.getDbEntry('L2')
        self.fingerprintDict = self.dbHelper.getDbEntry('L3')
        self.mapParametersDict = self.dbHelper.getDbEntry('L4')
        self.rssFingerprintDict = self.dbHelper.getDbEntry('L5')
        self.locactionServicesHelper = locationServices(self.rssFingerprintDict,self.apLocations,self.legalPoints,RSS0,nakagamiA,nakagamiB)
        self.pathPlanner = planPath(self.input_image,'Database/runtimeImages/path.jpg',self.legalPoints,self.scale_factor)
        self.pathTracker = pathTracker()
        self.magnificationServiceHelper = magnificationService(self.input_image,self.scale_factor)
        self.botRadius =botRadius
        self.botMaxVelocity = botMaxVelocity
        self.botturningVelocity = botturningVelocity
        self.vL = 0
        self.vR = 0
        self.img = cv2.imread(self.input_image,0)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))



    def botGod(self):
        self.magnificationServiceHelper.reInit()
        updatedImage = self.magnificationServiceHelper.magnify(self.masterLocation[0],self.masterTheta)
        filename = 'Navigation/' + str(time.time()) + '.jpg'
        cv2.imwrite(filename,updatedImage)


    def botBrain(self,startRoom, goalRoom, masterLocation, masterTheta):
        self.masterLocation = masterLocation
        self.masterTheta =masterTheta
        self.botGod()
        self.startRoomCoordinates = self.getNearestLegalPoint(self.getRoomCoordinates(startRoom))
        self.goalRoomCoordinates = self.getNearestLegalPoint(self.getRoomCoordinates(goalRoom))
        self.currentLocation = self.locactionServicesHelper.getCurrentLocation(self.masterLocation)
        wayPoints1 = self.planNavigation(tuple(reversed(self.currentLocation)),tuple(reversed(self.startRoomCoordinates)))
        self.autoNavigate(wayPoints1)
        time.sleep(3)
        wayPoints2 = self.planNavigation(self.startRoomCoordinates,self.goalRoomCoordinates)
        self.autoNavigate(wayPoints2)

    def planNavigation(self,start,goal):

        return self.pathTracker.getWayPoints(self.planPath(start,goal))


    def truePositionUpdate(self,vL,vR):
        currentPosition = self.masterLocation
        radiusRight = vR * self.timeStep
        rightWheelPosX = currentPosition[0][0] + int(self.botRadius*(np.sin(-90)))
        rightWheelPosY = currentPosition[0][1] + int(self.botRadius*(np.cos(-90)))
        rightWheelPosXUpdated = rightWheelPosX + int(radiusRight*(np.sin(self.masterTheta)))
        rightWheelPosYUpdated = rightWheelPosY + int(radiusRight*(np.cos(self.masterTheta)))

        radiusLeft = vL * self.timeStep
        leftWheelPosX = currentPosition[0][0] + int(self.botRadius*(np.sin(90)))
        leftWheelPosY = currentPosition[0][1] + int(self.botRadius*(np.cos(90)))
        leftWheelPosXUpdated = leftWheelPosX + int(radiusLeft*(np.sin(self.masterTheta)))
        leftWheelPosYUpdated = leftWheelPosY + int(radiusLeft*(np.cos(self.masterTheta)))
        masterX = int((rightWheelPosXUpdated + leftWheelPosXUpdated)/2)
        masterY = int((rightWheelPosYUpdated + leftWheelPosYUpdated)/2)
        self.masterTheta = self.getAngle([self.masterLocation[0],(masterX,masterY)])
        self.masterLocation = [(masterX,masterY)]
        
        

    def autoNavigate(self,wayPoints,navigationTresh = 3):
        botLocation = self.masterLocation
        for wayPoint in wayPoints:
            while(distance.euclidean(botLocation,wayPoint) >3):
                vL,vR = self.velocityControls(botLocation,wayPoint)
                print(self.masterLocation)
                self.truePositionUpdate(vL,vR)
                print(self.masterLocation)
                botLocation = [self.locactionServicesHelper.getCurrentLocation(self.masterLocation)]
                print(botLocation)
                
                self.botGod()


    def velocityControls(self, currentPoint, endPoint):
        #print(currentPoint[0])
        #print(endPoint)
        headingAngleNeeded = self.getAngle([currentPoint[0],endPoint])
        
        if headingAngleNeeded == self.masterTheta:
            vL = self.setVelocity(currentPoint,endPoint)
            vR = vL
        if headingAngleNeeded > self.masterTheta:
            vR = self.botturningVelocity
            vL = 0
        if headingAngleNeeded < self.masterTheta:
            vL = self.botturningVelocity
            vR = 0

        return vL,vR

    def setVelocity(self,start,goal):
        if distance.euclidean(start,goal) <=3:
            return 0
        if distance.euclidean(start,goal) >= 20:
            return self.botMaxVelocity
        if distance.euclidean(start,goal) < 20:
            return (self.botMaxVelocity/2)

        

    def getInitialTheta(self):
        return None

    def getAngle(self,points, mode = 1):
        if mode == 0:
            if abs(points[0][0]-points[1][0]) == 0:
                return 90.0
            return np.rad2deg(np.arctan((abs(points[0][1]-points[1][1])/abs(points[0][0]-points[1][0]))))
        if mode == 1:
            if abs(points[0][1]-points[1][1]) == 0:
                return 90.0
            return np.rad2deg(np.arctan((abs(points[0][0]-points[1][0])/abs(points[0][1]-points[1][1]))))

    def getRoomCoordinates(self,roomNumber):
        return self.mapParametersDict[roomNumber]
    
    def getNearestLegalPoint(self,point):
        return self.legalPoints[self.locactionServicesHelper.getLegalKNN(point)[0][0]]

    def planPath(self,start,goal):
        return self.pathPlanner.executePathPlanning(start, goal)

    def trackPath(self,plannedRoute):
        return self.pathTracker.getWayPoints(plannedRoute)


a = iBoiler('physics_corrected.jpg','Database/db',4,5,5,10,4.32,3.18,0.7,1)
a.botBrain('R112','R121',[(500,111)],-90)