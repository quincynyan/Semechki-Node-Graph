import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 1. Load Data
df = pd.read_csv("Semechki Node - Sheet2.csv", index_col=0)
df = df.replace('-', 0).apply(pd.to_numeric)

# 2. Build Graph (Filtering < 5)
G = nx.Graph()
for node in df.columns:
    G.add_node(node)

for i in range(len(df.columns)):
    for j in range(i + 1, len(df.columns)):
        weight = df.iloc[i, j]
        if weight >= 5:
            G.add_edge(df.columns[i], df.columns[j], weight=weight)

# 3. Calculate Metrics
# pos = nx.spring_layout(G, weight='weight', k=0.7, seed=42)
# pos = nx.kamada_kawai_layout(G, weight='weight')
pos = nx.spectral_layout(G, weight='weight')

# # pip install fa2
# from fa2 import ForceAtlas2
# 
# forceatlas2 = ForceAtlas2(
#     gravity=1.0,
#     scalingRatio=2.0,
#     strongGravityMode=True  # This is the key to creating "islands"
# )
# pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=200)

# Exaggerate Node Sizes (Power factor 1.5)
node_strengths = {node: sum(d['weight'] for _, _, d in G.edges(node, data=True)) for node in G.nodes()}
node_sizes = [pow(node_strengths[node], 1.5) * 15 for node in G.nodes()]

# 4. Scaling Logic: 5-10
# We want weight 5 to be thin/red and 10 to be thicker/green
weights = [G[u][v]['weight'] for u, v in G.edges()]

# Create a custom normalization range [5, 10]
norm = mcolors.Normalize(vmin=5, vmax=10)

# Edge Widths: Map 5->0.3 and 10->1.5 (Avoids overwhelming thickness)
edge_widths = [0.3 + (w - 5) * (10 / 5) for w in weights]

# Edge Colors: RdYlGn
edge_colors = [plt.cm.RdYlGn(norm(w)) for w in weights]

# 5. Draw
plt.figure(figsize=(14, 12))
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='#333333', alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=10, font_color='white', font_weight='bold')
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.8)

plt.title("Refined Friendship Cluster (Strength 5-10)", color='white')
plt.axis('off')
plt.gcf().set_facecolor('#1a1a1a')
plt.show()