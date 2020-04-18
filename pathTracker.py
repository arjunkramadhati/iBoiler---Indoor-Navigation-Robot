import numpy as np
import cv2
from planPath import planPath
from databaseManager import databaseManager
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from locationServices import locationServices
from scipy.spatial import distance

class pathTracker:

    def __init__(self):
        self.wayPoints = []

    def getAngle(self,points, mode = 1):
        if mode == 0:
            if abs(points[0][0]-points[1][0]) == 0:
                return 90.0
            return np.rad2deg(np.arctan((abs(points[0][1]-points[1][1])/abs(points[0][0]-points[1][0]))))
        if mode == 1:
            if abs(points[0][1]-points[1][1]) == 0:
                return 90.0
            return np.rad2deg(np.arctan((abs(points[0][0]-points[1][0])/abs(points[0][1]-points[1][1]))))

    def cleanWPs(self):
        poplist = []
        for i in range(len(self.wayPoints)):
            if i ==0:
                pass
            if i == len(self.wayPoints) - 1:
                pass
            else:

                if distance.euclidean((self.wayPoints[i][1],self.wayPoints[i][0]),(self.wayPoints[i-1][1],self.wayPoints[i-1][0])) <= 20:
                    poplist.append(self.wayPoints[i])

        self.wayPoints = [x for x in self.wayPoints if x not in poplist]

    def getWayPoints(self,route):
        initialAngle = self.getAngle([(route[0][0],route[0][1]),(route[1][0],route[1][1])])
        for i in range(len(route)):
            if i == (len(route)-1):
                self.wayPoints.append(route[i])
                break
            else:
                angle = self.getAngle([(route[i][0],route[i][1]),(route[i+1][0],route[i+1][1])])
                if (angle == initialAngle or (angle >= (initialAngle -25) and angle <= (initialAngle+25))):
                    pass
                else:
                    self.wayPoints.append(route[i])
                    initialAngle = angle
        self.cleanWPs()
        
        return self.wayPoints
            


'''
pt=pathTracker()
saver = databaseManager('Database/db')
locationServicesH = locationServices(saver.getDbEntry('L5'),saver.getDbEntry('L1'),saver.getDbEntry('L2'),10,4.32,3.18,)
print((198,92) in saver.getDbEntry('L2'))
a = planPath('physics_corrected.jpg','Database/runtimeImages/path.jpg',saver.getDbEntry('L2'),0.7)
goal = saver.getDbEntry('L2')[locationServicesH.getLegalKNN(saver.getDbEntry('L4')['R117'])[0][0]]
start = saver.getDbEntry('L2')[locationServicesH.getLegalKNN(saver.getDbEntry('L4')['R112'])[0][0]]
#start = (496,112)
#goal = (207,92)
#print(start)
#print(goal)
grid = a.getMatrix()
route = a.executePathPlanning((start[1],start[0]),(goal[1],goal[0]))
#route,grid,start,goal = a.planPath()
#start = (start[1],start[0])
#goal = (goal[1],goal[0])
start = tuple(reversed(start))
goal = tuple(reversed(goal))
wps = pt.getWayPoints(route)
x_coords = []

y_coords = []

image = cv2.imread('map.jpg')


for i in (range(0,len(route))):

    x = route[i][0]

    y = route[i][1]

    x_coords.append(x)

    y_coords.append(y)

# plot map and path

fig, ax = plt.subplots(figsize=(20,20))

ax.imshow(grid, cmap=plt.cm.Dark2)
#ax.scatter(397,128, marker = "*", color = "yellow", s = 200)
ax.scatter(198,92, marker = "*", color = "yellow", s = 200)

ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 200)


for i in range(len(wps)):
    ax.scatter(wps[i][1],wps[i][0], marker = "*", color = "yellow", s = 200)
    

print(distance.euclidean((wps[1][1],wps[1][0]),(wps[0][1],wps[0][0])))
ax.scatter(goal[1],goal[0], marker = "*", color = "red", s = 200)

ax.plot(y_coords,x_coords, color = "black")

plt.show()
'''