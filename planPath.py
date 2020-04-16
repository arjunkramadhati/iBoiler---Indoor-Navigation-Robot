import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from databaseManager import databaseManager
import cv2




class planPath:

    def __init__(self, image_Address, output_Address, legalPoints, scale_factor):

        self.image_Address = image_Address
        self.output_Address = output_Address
        self.legalPoints = legalPoints
        self.scale_factor = scale_factor
        self.img = cv2.imread(self.image_Address,0)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))
        self.prepareMatrix()

    def prepareMatrix(self):
        self.matrix = np.ones(self.img.shape)

        for p in self.legalPoints:
            self.matrix[p[1],p[0]]=0






    def claculateHeuristic(self,a,b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


saver = databaseManager('Database/db')
a = planPath('physics_corrected.jpg','Database/runtimeImages/path.jpg',saver.getDbEntry('L2'),0.7)