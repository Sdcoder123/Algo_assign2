from distutils.command.check import check
from typing import List

from test_data import polygon
from shapely.geometry import Point, Polygon
from matplotlib import pyplot as plt
import operator


class triangulation(polygon):
    def __init__(self, n):
        super().__init__(n)
        super().generate()
        self.name = {}
        self.partition = []
        self.partition_greedy = []
        # naming of points to identify the intersecting ones
        for i in range(len(self.poly.exterior.coords)-1):
            self.name[self.poly.exterior.coords[i]] = i
    # dp is a n*n matrix storing permeter

    def tri_perimeter(self, points: Polygon):
        perimeter = 0
        for i in range(len(points.exterior.coords)-1):
            x = points.exterior.coords[i]
            y = points.exterior.coords[i+1]
            perimeter = perimeter +\
                Point(x[0], x[1]).distance(
                    Point(y[0], y[1]))
        return perimeter

    def dynamic(self, points: Polygon):
        # dp is a 2d matrix storing the perimeter of the polygons formed by the diagonals of two indexed points
        n = len(points.exterior.coords)-1
        if n < 3:
            return 0

        dp = [[0 for i in range(n)] for j in range(n)]
        partition = [[float('-inf') for i in range(n)] for j in range(n)]
        for gap in range(0, n):
            i = 0
            j = gap
            while(j < n):
                if j < i+2:
                    dp[i][j] = 0
                else:
                    dp[i][j] = float("inf")
                    for k in range(i+1, j):
                        x1, y1 = points.exterior.xy
                        x = [x1[p] for p in (i, k, j)]
                        y = [y1[p] for p in (i, k, j)]
                        val = dp[i][k]+dp[k][j] + \
                            self.tri_perimeter(Polygon(zip(x, y)))
                        if val < dp[i][j]:
                            dp[i][j] = val
                            partition[i][j] = k
                i = i+1
                j = j+1

        def find_partition(i, j):
            if abs(i-j) <= 1:
                return
            if abs(i-j) == 2:
                self.partition.append((i, j))
                return
            k = partition[i][j]
            self.partition.extend([(i, k), (k, j)])
            find_partition(i, k)
            find_partition(k, j)
        find_partition(0, n-1)
        return dp[0][n-1]

    def greedy(self):
        diagonal = []
        n = len(self.poly.exterior.coords)-1
        for i in range(n):
            for j in range(i+2, n):
                if i == 0 and j == n-1:
                    continue
                x = self.poly.exterior.coords[i]
                y = self.poly.exterior.coords[j]
                l = {}
                l['diagonal'] = (i, j)
                l['val'] = Point(
                    x[0], x[1]).distance(Point(y[0], y[1]))
                diagonal.append(l)
        diagonal.sort(key=operator.itemgetter('val'))
        print(diagonal)
        partition = []

        def check_intersection(p):
            for i in range(len(partition)):
                diff1 = partition[i][0]-p[0]
                diff2 = partition[i][1]-p[0]
                diff3 = partition[i][0]-p[1]
                diff4 = partition[i][1]-p[1]
                # compare these diff to find the best value
                p1 = diff1*diff3
                p2 = diff2*diff4
                if not ((p1 >= 0 and p2 >= 0) or (p1 <= 0 and p2 <= 0)):
                    return False
            return True
        peri = 0.0
        for i in range(len(diagonal)):
            if check_intersection(diagonal[i]['diagonal']):
                partition.append(diagonal[i]['diagonal'])
                peri = peri+diagonal[i]['val']*2
        peri = peri+self.tri_perimeter(self.poly)
        # though named triperi can work for any n sided polygon
        self.partition_greedy = partition
        return peri

    def get_key(self, val):
        for key, value in self.name.items():
            if val == value:
                return key

    def visualize(self, partition):
        x, y = self.poly.exterior.xy
        plt.plot(x, y)
        for i in range(len(partition)):
            x1, y1 = self.get_key(partition[i][0])
            x2, y2 = self.get_key(partition[i][1])
            plt.plot([x1, x2], [y1, y2])
        plt.show()


#p = triangulation([(-40, -39), (-47, 13), (24, 44), (32, 23), (35, 15)])
p = triangulation(7)
print(p.name)
i = 0
k = 1
j = 3
x1, y1 = p.poly.exterior.xy
x = [x1[p] for p in (i, k, j)]
y = [y1[p] for p in (i, k, j)]
print(x1, y1, x, y)
peri = p.dynamic(p.poly)
print(peri)
print(p.partition)
p.plot()
p.visualize(p.partition)
print(p.greedy())
p.visualize(p.partition_greedy)