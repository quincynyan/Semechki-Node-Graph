import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import louvain_communities
import numpy as np

# 1. Setup Graph
df = pd.read_csv("Semechki Node - Sheet2.csv", index_col=0).replace('-', 0).apply(pd.to_numeric)
G = nx.Graph()
for i in range(len(df.columns)):
    for j in range(i + 1, len(df.columns)):
        if df.iloc[i, j] >= 5: # Keep the filter
            G.add_edge(df.columns[i], df.columns[j], weight=df.iloc[i, j])

# 2. Community Detection (The "Island" Creator)
communities = louvain_communities(G, weight='weight')

# 3. Custom Position: Place communities in a circle
pos = {}
for i, comm in enumerate(communities):
    subgraph = G.subgraph(comm)
    # Give each community its own 'spring' layout, centered in a circle
    sub_pos = nx.spring_layout(subgraph, k=0.5, seed=42)
    # Shift community positions so they don't overlap
    shift = (np.cos(2*np.pi*i/len(communities)), np.sin(2*np.pi*i/len(communities)))
    for node, coords in sub_pos.items():
        pos[node] = coords + shift

# 4. Draw
plt.figure(figsize=(12, 12), facecolor='#1a1a1a')
nx.draw_networkx_nodes(G, pos, node_size=800, node_color='#555555')
nx.draw_networkx_labels(G, pos, font_color='white')
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3)
plt.axis('off')
plt.show()