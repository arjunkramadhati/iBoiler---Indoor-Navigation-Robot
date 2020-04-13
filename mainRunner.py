'''
This code is the main code to manage the setting up of the map which the robot can understand. 
Author : Arjun Kramadhati Gopi


'''


from getAPLocations import getAPLocations
from mapGenerator import mapGenerator
from distanceAlgorithm import distanceAlgorithm
from mapParameters import mapParameters
from databaseManager import databaseManager

class mainRunner:

    def __init__(self):
        self.image = 'physics_corrected.jpg'
        self.levelOneOutputAddress = 'Database/checkpointImages/APs.jpg'
        self.levelTwoOutputAddress = 'Database/checkpointImages/legalPoints.jpg'
        self.levelThreeOutputAddress = 'Database/checkpointImages/levelThree.jpg'
        self.levelFourOutputAddress = 'Database/checkpointImages/mapParameters.jpg'
        self.databaseLocation ='Database/db'
        self.scale_factor = 0.7
        self.apLocations = {}
        self.legalPoints = []
        self.fingerprintDict ={}
        self.mapParametersDict = {}


    def runProcess(self):
        print("Loading resources...")
        print("Checking for saved work...")
        self.saver = databaseManager(self.databaseLocation)
        if self.saver.checkDbEntry('L1'):
            q = input('Level One entry exists. Press Enter to continue. Anything else to overwrite')
            if q == "":
                self.apLocations = self.saver.getDbEntry('L1')
                pass
            else:
                self.levelOne()
        else:
            self.levelOne()

        if self.saver.checkDbEntry('L2'):
            q = input('Level Two entry exists. Press Enter to continue. Anything else to overwrite')
            if q == "":
                self.legalPoints = self.saver.getDbEntry('L2')
                pass
            else:
                self.levelTwo()
        else:
            self.levelTwo()

        if self.saver.checkDbEntry('L3'):
            q = input('Level Three entry exists. Press Enter to continue. Anything else to overwrite')
            if q == "":
                self.fingerprintDict = self.saver.getDbEntry('L3')
                pass
            else:
                self.levelThree()
        else:
            self.levelThree()

        if self.saver.checkDbEntry('L4'):
            q = input('Level Four entry exists. Press Enter to continue. Anything else to overwrite')
            if q == "":
                self.mapParametersDict = self.saver.getDbEntry('L4')
                pass
            else:
                self.levelFour()
        else:
            self.levelFour()
        



    def levelOne(self):
        #get WiFi Access Point locations (3 APs)
        levelOne = getAPLocations(self.image, self.levelOneOutputAddress, self.scale_factor)
        self.apLocations = levelOne.getAPDone()
        levelOne.showOutput()
        self.saver.saveLevelOutput('L1',self.apLocations)
        print("Level One Done")

    def levelTwo(self):
        #get legal points
        levelTwo = mapGenerator(self.image,self.levelTwoOutputAddress,self.scale_factor)
        self.legalPoints = levelTwo.getMapDone()
        self.saver.saveLevelOutput('L2',self.legalPoints)
        print("Level Two Done")

    def levelThree(self):
        #get fingerprints
        levelThree = distanceAlgorithm(self.apLocations,self.legalPoints, self.image, self.levelThreeOutputAddress,self.scale_factor)
        self.fingerprintDict = levelThree.getFingerprintDone()
        self.saver.saveLevelOutput('L3',self.fingerprintDict)
        print("Level Three Done")

    def levelFour(self):
        #add map details
        levelFour = mapParameters(self.image, self.levelFourOutputAddress,self.scale_factor)
        self.mapParametersDict = levelFour.getmapParameterDone()
        self.saver.saveLevelOutput('L4',self.mapParametersDict)
        print("Level Four Done")


        


a = mainRunner()
a.runProcess()

