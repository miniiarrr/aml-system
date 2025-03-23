import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

# Read the transaction data
with open('all_transactions.json', 'r') as f:
    transactions = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add edges with weights (amount) and timestamps
for tx in transactions:
    processed_time = datetime.strptime(tx['time'], '%Y-%m-%d %H:%M:%S')
    
    G.add_edge(tx['from'], 
               tx['to'], 
               weight=tx['amount'],
               time=processed_time,
               block_number=int(tx['blockNumber']),
               tx_hash=tx['tx_hash'])

# Calculate node sizes based on total transaction amount (both sent and received)
node_sizes = {}
for node in G.nodes():
    # Sum of all transactions (both sent and received)
    total_amount = (sum(d['weight'] for _, _, d in G.in_edges(node, data=True)) +
                   sum(d['weight'] for _, _, d in G.out_edges(node, data=True)))
    node_sizes[node] = total_amount

# Normalize node sizes for visualization (using log scale for better visibility)
max_size = max(node_sizes.values())
node_sizes = {k: np.log1p(v/max_size * 1000) * 100 for k, v in node_sizes.items()}

# Create the visualization
plt.figure(figsize=(20, 20))

# Use spring layout for better visualization
pos = nx.spring_layout(G, k=1, iterations=50)

# Draw the network
nx.draw_networkx_nodes(G, pos, 
                      node_size=[node_sizes[node] for node in G.nodes()],
                      node_color='lightblue',
                      alpha=0.7)

# Draw edges with width based on transaction amount (using log scale)
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
max_weight = max(edge_weights)
edge_widths = [np.log1p(w/max_weight * 5) * 2 for w in edge_weights]

# Draw edges with transaction amounts as labels
edge_labels = {edge: f"{G[edge[0]][edge[1]]['weight']:.2f} ETH" 
              for edge in G.edges()}

# Draw edges with color gradient based on amount
edge_colors = [w/max_weight for w in edge_weights]
nx.draw_networkx_edges(G, pos,
                      width=edge_widths,
                      edge_color=edge_colors,
                      edge_cmap=plt.cm.viridis,
                      alpha=0.7,
                      arrows=True)

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, 
                           edge_labels=edge_labels,
                           font_size=6)

# Add labels for nodes (shortened addresses)
labels = {node: node[:8] + '...' for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title('ETH Flow Visualization\n(Circle size and line thickness represent transaction amounts)', fontsize=16, pad=20)
plt.axis('off')

# Save the visualization
plt.savefig('eth_flow.png', dpi=300, bbox_inches='tight')
plt.close()

# Print statistics
print("\n=== Transaction Statistics ===")
print(f"Total number of transactions: {len(transactions)}")
print(f"Total number of unique wallets: {len(G.nodes())}")
print(f"Total number of connections: {len(G.edges())}")
print(f"Total ETH transferred: {sum(edge_weights):.2f} ETH")

# Calculate and print top receivers
receivers = {}
for node in G.nodes():
    received_amount = sum(d['weight'] for _, _, d in G.in_edges(node, data=True))
    receivers[node] = received_amount

top_receivers = sorted(receivers.items(), key=lambda x: x[1], reverse=True)[:5]
print("\n=== Top 5 Receivers by Amount ===")
for addr, amount in top_receivers:
    print(f"{addr[:8]}...: {amount:.2f} ETH")

# Calculate and print top senders
senders = {}
for node in G.nodes():
    sent_amount = sum(d['weight'] for _, _, d in G.out_edges(node, data=True))
    senders[node] = sent_amount

top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:5]
print("\n=== Top 5 Senders by Amount ===")
for addr, amount in top_senders:
    print(f"{addr[:8]}...: {amount:.2f} ETH")

# Time-based statistics
print("\n=== Time-based Statistics ===")
transaction_times = [G[u][v]['time'] for u, v in G.edges()]
print(f"Date range: from {min(transaction_times).strftime('%Y-%m-%d')} to {max(transaction_times).strftime('%Y-%m-%d')}")

# Convert times to pandas Series for easier analysis
times_series = pd.Series(transaction_times)
print(f"Most active hour: {times_series.dt.hour.value_counts().idxmax()}:00")
print(f"Number of transactions in most active hour: {times_series.dt.hour.value_counts().max()}")

# Print gas statistics
gas_prices = [G[u][v]['gas_price'] for u, v in G.edges()]
gas_used = [G[u][v]['gas'] for u, v in G.edges()]
print("\n=== Gas Statistics ===")
print(f"Average gas price: {np.mean(gas_prices):.2f} Gwei")
print(f"Average gas used: {np.mean(gas_used):.2f}")
print(f"Total gas used: {sum(gas_used):,}")

# Print block number statistics
block_numbers = [G[u][v]['block_number'] for u, v in G.edges()]
print("\n=== Block Statistics ===")
print(f"Block range: from {min(block_numbers):,} to {max(block_numbers):,}")
print(f"Number of blocks spanned: {max(block_numbers) - min(block_numbers) + 1:,}")