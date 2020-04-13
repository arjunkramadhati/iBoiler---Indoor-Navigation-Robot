from getAPLocations import getAPLocations
from mapGenerator import mapGenerator
from distanceAlgorithm import distanceAlgorithm
from mapParameters import mapParameters

class mainRunner:

    def __init__(self):
        self.image = 'physics_corrected.jpg'
        self.levelOneOutputAddress = 'APs.jpg'
        self.levelTwoOutputAddress = 'legalPoints.jpg'
        self.levelThreeOutputAddress = 'levelThree.jpg'
        self.levelFourOutputAddress = 'mapParameters.jpg'
        self.scale_factor = 0.7
        self.apLocations = {}
        self.legalPoints = []
        self.fingerprintDict ={}
        self.mapParametersDict = {}


    def runProcess(self):
        self.levelOne()
        self.levelTwo()
        self.levelThree()


    def levelOne(self):
        levelOne = getAPLocations(self.image, self.levelOneOutputAddress, self.scale_factor)
        self.apLocations = levelOne.getAPDone()
        levelOne.showOutput()
        print("Level One Done")

    def levelTwo(self):
        levelTwo = mapGenerator(self.image,self.levelTwoOutputAddress,self.scale_factor)
        self.legalPoints = levelTwo.getMapDone()
        print("Level Two Done")

    def levelThree(self):
        levelThree = distanceAlgorithm(self.apLocations,self.legalPoints, self.image, self.levelThreeOutputAddress,self.scale_factor)
        self.fingerprintDict = levelThree.getFingerprintDone()
        print("Level Three Done")

    def levelFour(self):
        levelFour = mapParameters(self.image, self.levelFourOutputAddress,self.scale_factor)
        self.mapParametersDict = levelFour.getmapParameterDone()

        


a = mainRunner()
a.runProcess()

