from getAPLocations import getAPLocations
from mapGenerator import mapGenerator
from distanceAlgorithm import distanceAlgorithm

class mainRunner:

    def __init__(self):
        self.image = 'physics_corrected.jpg'
        self.levelOneOutputAddress = 'APs.jpg'
        self.levelTwoOutputAddress = 'legalPoints.jpg'
        self.apLocations = {}
        self.legalPoints = []


    def runProcess(self):
        self.levelOne()
        self.levelTwo()
        self.levelThree()


    def levelOne(self):
        levelOne = getAPLocations(self.image, self.levelOneOutputAddress)
        self.apLocations = levelOne.getAPDone()
        levelOne.showOutput()

    def levelTwo(self):
        levelTwo = mapGenerator(self.image,self.levelTwoOutputAddress)
        self.legalPoints = levelTwo.getMapDone()

    def levelThree(self):
        levelThree = distanceAlgorithm(self.apLocations,self.legalPoints)
        levelThree.getFingerprints()
        


a = mainRunner()
a.runProcess()

