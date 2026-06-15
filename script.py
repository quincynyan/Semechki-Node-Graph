import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 1. Load Data
df = pd.read_csv("Semechki Node - Sheet2.csv", index_col=0)
df = df.replace('-', 0).apply(pd.to_numeric)

# 2. Build Graph
G = nx.Graph()
for node in df.columns:
    G.add_node(node)

for i in range(len(df.columns)):
    for j in range(i + 1, len(df.columns)):
        weight = df.iloc[i, j]
        if weight > 0:
            G.add_edge(df.columns[i], df.columns[j], weight=weight)

# 3. Calculate Layout & Metrics
pos = nx.spring_layout(G, weight='weight', k=0.7, seed=42)

# Exaggerate Node Sizes: Apply a power factor to the node strength
node_strengths = {node: sum(d['weight'] for _, _, d in G.edges(node, data=True)) for node in G.nodes()}
# Using node_strength^1.5 makes large nodes much larger and small nodes smaller
node_sizes = [pow(node_strengths[node], 1.5) * 15 for node in G.nodes()]

# Edge attributes: Red to Green spectrum
weights = [G[u][v]['weight'] for u, v in G.edges()]
norm = mcolors.Normalize(vmin=min(weights), vmax=max(weights))
# cmap='RdYlGn' maps low values to red, high values to green
edge_colors = [plt.cm.RdYlGn(norm(w)) for w in weights]
edge_widths = [w * 0.8 for w in weights]

# 4. Draw
plt.figure(figsize=(14, 12))
# Draw nodes with a slight transparency to look more modern
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='#333333', alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=10, font_color='white', font_weight='bold')
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.8)

plt.title("Friendship Cluster Network (Red-Green Scale)", color='white')
plt.axis('off')
plt.gcf().set_facecolor('#1a1a1a') # Dark background for aesthetic
plt.show()