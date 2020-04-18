import numpy as np
import cv2
from planPath import planPath
from databaseManager import databaseManager
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

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


    def getWayPoints(self,route):
        initialAngle = self.getAngle([(route[0][0],route[0][1]),(route[1][0],route[1][1])])
        for i in range(len(route)):
            if i == (len(route)-1):
                self.wayPoints.append(route[i])
                break
            else:
                angle = self.getAngle([(route[i][0],route[i][1]),(route[i+1][0],route[i+1][1])])
                if angle == initialAngle or (angle >= (initialAngle -25) and angle <= (initialAngle+25)):
                    pass
                else:
                    self.wayPoints.append(route[i])
                    initialAngle = angle
        return self.wayPoints
            


'''
pt=pathTracker()


saver = databaseManager('Database/db')
a = planPath('physics_corrected.jpg','Database/runtimeImages/path.jpg',saver.getDbEntry('L2'),0.7)
route,grid,start,goal = a.planPath()
wps = pt.getWayPoints(route)
x_coords = []

y_coords = []

for i in (range(0,len(route))):

    x = route[i][0]

    y = route[i][1]

    x_coords.append(x)

    y_coords.append(y)

# plot map and path

fig, ax = plt.subplots(figsize=(20,20))

ax.imshow(grid, cmap=plt.cm.Dark2)

ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 200)

ax.scatter(goal[1],goal[0], marker = "*", color = "red", s = 200)

for i in range(len(wps)):
    ax.scatter(wps[i][1],wps[i][0], marker = "*", color = "yellow", s = 200)


ax.plot(y_coords,x_coords, color = "black")

plt.show()
'''