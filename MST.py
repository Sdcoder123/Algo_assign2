import snap
import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('facebook_combined.txt',
                     create_using=nx.Graph(), nodetype=int)
print(nx.info(g))
sp = nx.spring_layout(g)
plt.axis("off")
nx.draw_networkx(g, pos=sp, with_labels=False, node_size=35)
plt.show()

p = nx.minimum_spanning_tree(g)
sp = nx.spring_layout(p)
plt.axis("off")
nx.draw_networkx(p, pos=sp, with_labels=False, node_size=35)
plt.show()