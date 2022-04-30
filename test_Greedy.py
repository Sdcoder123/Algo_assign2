from polygon_triangulation import triangulation
import matplotlib.pyplot as plt


sides = 4
error = [0 for i in range(15)]
while(sides < 14):
    for i in range(1000):
        p = triangulation(sides)
        if int(p.dynamic(p.poly)) != int(p.greedy()):
            error[sides-1] += 1
    sides += 1
x = [i+1 for i in range(14)]
error = [i/10 for i in error]
plt.bar(x, error, color="blue", width=0.4)
plt.xlabel("Polygon length")
plt.ylabel("Percentage error")
plt.show()