import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from databaseManager import databaseManager
import cv2
from scipy.spatial import distance




class planPath:

    def __init__(self, image_Address, output_Address, legalPoints, scale_factor):

        self.image_Address = image_Address
        self.output_Address = output_Address
        self.legalPoints = legalPoints
        self.scale_factor = scale_factor
        self.sgCoordinates = []
        self.img = cv2.imread(self.image_Address,0)
        self.img = cv2.resize(self.img,(int(self.img.shape[1]*self.scale_factor),int(self.img.shape[0]*self.scale_factor)))
        self.prepareMatrix()

    def prepareMatrix(self):
        self.matrix = np.ones(self.img.shape)

        for p in self.legalPoints:
            self.matrix[p[1],p[0]]=0
        
    def getMatrix(self):
        return self.matrix
    def draw_path(self,event,x,y,flags,param):

        if event == cv2.EVENT_LBUTTONDOWN:
            #print(x,y)
            self.sgCoordinates.append((y,x))


    def planPath(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.draw_path)

        while(len(self.sgCoordinates) < 2):
            cv2.imshow('image',self.img)
            k = cv2.waitKey(1) & 0xFF
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        route = self.executePathPlanning(self.sgCoordinates[0],self.sgCoordinates[1])
        print(route)
        return route, self.matrix,self.sgCoordinates[0],self.sgCoordinates[1]

    def executePathPlanning(self,startCoord, endCoord):
        #print(startCoord)
        #print(endCoord)
        route = self.astar(self.matrix, startCoord, endCoord)
        #print(type(startCoord))
        #print(type(route))

        route = route + [startCoord]

        #route = route[::-1]
        route = list(reversed(route))
        return route





    def claculateHeuristic(self,a,b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, array, start, goal):

        neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

        close_set = set()

        came_from = {}

        gscore = {start:0}

        fscore = {start:self.claculateHeuristic(start, goal)}

        oheap = []

        heapq.heappush(oheap, (fscore[start], start))
    

        while oheap:

            current = heapq.heappop(oheap)[1]

            if current == goal:

                data = []

                while current in came_from:

                    data.append(current)

                    current = came_from[current]

                return data

            close_set.add(current)

            for i, j in neighbors:

                neighbor = current[0] + i, current[1] + j

                tentative_g_score = gscore[current] + self.claculateHeuristic(current, neighbor)

                if 0 <= neighbor[0] < array.shape[0]:

                    if 0 <= neighbor[1] < array.shape[1]:                

                        if array[neighbor[0]][neighbor[1]] == 1:

                            continue

                    else:

                        # array bound y walls

                        continue

                else:

                    # array bound x walls

                    continue
    

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):

                    continue
    

                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:

                    came_from[neighbor] = current

                    gscore[neighbor] = tentative_g_score

                    fscore[neighbor] = tentative_g_score + self.claculateHeuristic(neighbor, goal)

                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
    

        return False

'''
saver = databaseManager('Database/db')
a = planPath('physics_corrected.jpg','Database/runtimeImages/path.jpg',saver.getDbEntry('L2'),0.7)
route,grid,start,goal = a.planPath()

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

ax.plot(y_coords,x_coords, color = "black")

plt.show()
'''