import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gml('knowledge_graph.gml')

fig, ax = plt.subplots()
pos = nx.spring_layout(G, k=55)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, ax=ax)
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

plt.show()
