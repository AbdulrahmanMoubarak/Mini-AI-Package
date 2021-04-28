# -*- coding: utf-8 -*-
import numpy
from sklearn.datasets._samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class DBSCAN_Algo:
    lables = []
    Points = []

    def __init__(self, pointList):
        self.Points = self.initPoints(pointList)
        pass

    def initPoints(self, pointList):
        NewList = {}
        i = 0
        for item in pointList:
            newPoint = Point(item, i)
            NewList[str(newPoint.index)] = newPoint
            i += 1

        return NewList

    def getlables(self):
        mylables = []
        for point in self.Points.values():
            x = point.clusterId
            mylables.append(x)

        return mylables


def GetDistance(Point1, Point2):
    return numpy.sqrt(((Point1.values[0] - Point2.values[0]) ** 2) + ((Point1.values[1] - Point2.values[1]) ** 2))


class Point:
    index = -1
    values = []
    clusterId = -1

    def __init__(self, values, index):
        self.values = values
        self.visited = False
        self.index = index
        pass


# for making density data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)


# ------------------------------------------------------------------


def MyDBSCAN(D, eps, MinPts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.

    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.

    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """
    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.

    DB = DBSCAN_Algo(D)
    c = 0
    for point in DB.Points.values():
        if point.visited == False:
            point.visited = True
            sphere_points = regionQuery(DB.Points, point, eps)
            if len(sphere_points) >= MinPts:
                c += 1
                DB = growCluster(DB.Points, DB, point, sphere_points, c, eps, MinPts)


    myLables = DB.getlables()
    return myLables


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    labels.Points[str(P.index)].clusterId = C

    while len(NeighborPts)!=0:
        point=NeighborPts[0]
        NeighborPts.remove(point)
        if point.visited == False:
            labels.Points[str(point.index)].visited = True
            x = len(NeighborPts)

            sphere = regionQuery(D, point, eps)
            if len(sphere) >= MinPts:
                NeighborPts = NeighborPts + sphere

            if point.clusterId == -1:
                labels.Points[str(point.index)].clusterId = C



    return labels


def regionQuery(D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    sp = []
    for point in D.values():
        dist = GetDistance(P, point)
        if dist <= eps:
            sp.append(point)



    return sp







my_labels = MyDBSCAN(X, eps=0.3, MinPts=10)
print(my_labels)

print("==========================================")
# built in DBSCAN Function
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
skl_labels = db.labels_

# Scikit learn uses -1 to for NOISE, and starts cluster labeling at 0. I start
# numbering at 1, so increment the skl cluster numbers by 1.
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == -1:
        skl_labels[i] += 1

# print(skl_labels)

num_disagree = 0
# ---------------------------------
# compare built in and custom made dbscan function
# Go through each label and make sure they match (print the labels if they
# don't)
x = len(skl_labels)
print(x)
for i in range(0, len(skl_labels)):
    if not skl_labels[i] == my_labels[i]:
        print ('index', i,'Scikit learn:', skl_labels[i], 'mine:', my_labels[i])
        num_disagree += 1

y=(x-num_disagree)/x
percent=y*100

print('success percentage => ', round(percent,1) ,'%')
if num_disagree == 0:
    print('PASS - All labels match!')
else:
    print('FAIL -', num_disagree, 'labels don\'t match.')
