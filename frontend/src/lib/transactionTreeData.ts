import { Node, Edge } from 'reactflow';

interface Transaction {
  tx_hash: string;
  parent_tx: string | null;
  from: string;
  to: string;
  amount: number;
  currency: string;
  time: string;
  blockNumber: string;
  method: string;
  input: string;
  depth: number;
}

/**
 * This function transforms transaction data into a format suitable for ReactFlow
 * @param transactions Array of transaction objects
 * @returns Object containing nodes and edges for TreeChart
 */
export function transformTransactionsToTreeData(transactions: Transaction[]) {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const addressMap = new Map<string, string>(); // Maps addresses to node IDs
  let nodeId = 1;
  
  // Create a graph structure that preserves the hierarchy
  const txMap = new Map<string, Transaction>(); // Maps tx_hash to transaction
  const childrenMap = new Map<string, string[]>(); // Maps tx_hash to child tx_hashes
  
  // First pass: map transactions and build parent-child relationships
  transactions.forEach(tx => {
    txMap.set(tx.tx_hash, tx);
    
    if (tx.parent_tx) {
      // Add this tx_hash as a child of its parent
      const children = childrenMap.get(tx.parent_tx) || [];
      children.push(tx.tx_hash);
      childrenMap.set(tx.parent_tx, children);
    }
  });
  
  // Helper function to get or create a node ID for an address
  const getNodeId = (address: string): string => {
    if (!addressMap.has(address)) {
      const id = `node-${nodeId++}`;
      addressMap.set(address, id);
      
      // Create a node for this address
      const shortAddress = `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
      nodes.push({
        id,
        type: 'treeNode',
        data: { 
          label: shortAddress,
          tooltip: `Address: ${address}`,
          url: `https://etherscan.io/address/${address}`
        },
        // We'll calculate positions later
        position: { x: 0, y: 0 }
      });
    }
    return addressMap.get(address)!;
  };
  
  // Create nodes for all addresses involved in transactions
  transactions.forEach(tx => {
    getNodeId(tx.from);
    getNodeId(tx.to);
  });
  
  // Create edges for all transactions
  transactions.forEach(tx => {
    const sourceId = getNodeId(tx.from);
    const targetId = getNodeId(tx.to);
    
    const edgeLabel = `${tx.amount} ${tx.currency}\n${tx.time}`;
    const edgeId = `edge-${tx.tx_hash}`;
    
    // Create tooltip with detailed transaction info
    const tooltip = [
      `Transaction: ${tx.tx_hash.substring(0, 10)}...`,
      `Method: ${tx.method}`,
      `From: ${tx.from.substring(0, 10)}...`,
      `To: ${tx.to.substring(0, 10)}...`,
      `Amount: ${tx.amount} ${tx.currency}`,
      `Block: ${tx.blockNumber}`,
      `Time: ${tx.time}`
    ].join('\n');
    
    edges.push({
      id: edgeId,
      source: sourceId,
      target: targetId,
      data: {
        label: edgeLabel,
        tooltip,
        token: tx.currency,
        amount: tx.amount.toString(),
        details: {
          txHash: tx.tx_hash,
          blockNumber: tx.blockNumber,
          method: tx.method
        }
      }
    });
  });
  
  // Calculate positions using a basic tree layout
  const ROOT_X = 0;
  const ROOT_Y = 500;
  const LEVEL_X_GAP = 3000;
  const NODE_Y_GAP = 500;
  
  // First find the root transaction (where parent_tx is null)
  const rootTx = transactions.find(tx => tx.parent_tx === null);
  
  if (rootTx) {
    // Start with the root transaction at (0, 0)
    const rootFromNodeId = getNodeId(rootTx.from);
    const rootNode = nodes.find(n => n.id === rootFromNodeId);
    if (rootNode) {
      rootNode.position = { x: ROOT_X, y: ROOT_Y };
    }
    
    // Helper function to position child nodes recursively
    const positionChildNodes = (txHash: string, level: number, startY: number) => {
      const childTxHashes = childrenMap.get(txHash) || [];
      const childCount = childTxHashes.length;
      
      // If this transaction has children, position them
      if (childCount > 0) {
        const xPos = ROOT_X + (level * LEVEL_X_GAP);
        let currentY = startY - (childCount - 1) * NODE_Y_GAP / 2;
        
        childTxHashes.forEach(childTxHash => {
          const childTx = txMap.get(childTxHash);
          if (childTx) {
            const childNodeId = getNodeId(childTx.to);
            const childNode = nodes.find(n => n.id === childNodeId);
            if (childNode) {
              childNode.position = { x: xPos, y: currentY };
              currentY += NODE_Y_GAP;
            }
            
            // Position this child's children
            positionChildNodes(childTxHash, level + 1, currentY - NODE_Y_GAP/2);
          }
        });
      }
    };
    
    // Start positioning from the root
    positionChildNodes(rootTx.tx_hash, 1, ROOT_Y);
  }
  
  return { nodes, edges };
}

// Force-directed layout algorithm (simplified)
function applyForceDirectedLayout(nodes: Node[], edges: Edge[], iterations = 100) {
  const REPULSION = 1000;   // Repulsion force between nodes
  const ATTRACTION = 0.1;   // Attraction force of edges
  const GRAVITY = 0.1;      // Pull towards the center
  const MAX_DISPLACEMENT = 100;  // Limit node movement per iteration
  
  const centerX = nodes.reduce((sum, node) => sum + node.position.x, 0) / nodes.length;
  const centerY = nodes.reduce((sum, node) => sum + node.position.y, 0) / nodes.length;
  
  for (let iter = 0; iter < iterations; iter++) {
    // Calculate repulsion between nodes
    const forces = nodes.map(() => ({ x: 0, y: 0 }));
    
    // Repulsion between nodes
    for (let i = 0; i < nodes.length; i++) {
      for (let j = 0; j < nodes.length; j++) {
        if (i === j) continue;
        
        const nodeA = nodes[i];
        const nodeB = nodes[j];
        
        const dx = nodeA.position.x - nodeB.position.x;
        const dy = nodeA.position.y - nodeB.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy) || 1;
        
        // Apply repulsion force (inversely proportional to distance)
        const force = REPULSION / (distance * distance);
        const forceX = (dx / distance) * force;
        const forceY = (dy / distance) * force;
        
        forces[i].x += forceX;
        forces[i].y += forceY;
      }
    }
    
    // Attraction along edges
    for (const edge of edges) {
      const sourceNode = nodes.find(n => n.id === edge.source);
      const targetNode = nodes.find(n => n.id === edge.target);
      
      if (sourceNode && targetNode) {
        const dx = sourceNode.position.x - targetNode.position.x;
        const dy = sourceNode.position.y - targetNode.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy) || 1;
        
        // Apply attraction force (proportional to distance)
        const force = distance * ATTRACTION;
        const forceX = (dx / distance) * force;
        const forceY = (dy / distance) * force;
        
        forces[nodes.indexOf(sourceNode)].x -= forceX;
        forces[nodes.indexOf(sourceNode)].y -= forceY;
        forces[nodes.indexOf(targetNode)].x += forceX;
        forces[nodes.indexOf(targetNode)].y += forceY;
      }
    }
    
    // Add gravity towards the center
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      forces[i].x -= (node.position.x - centerX) * GRAVITY;
      forces[i].y -= (node.position.y - centerY) * GRAVITY;
    }
    
    // Apply forces with displacement limit
    for (let i = 0; i < nodes.length; i++) {
      const displacement = Math.sqrt(forces[i].x * forces[i].x + forces[i].y * forces[i].y);
      
      if (displacement > MAX_DISPLACEMENT) {
        forces[i].x = (forces[i].x / displacement) * MAX_DISPLACEMENT;
        forces[i].y = (forces[i].y / displacement) * MAX_DISPLACEMENT;
      }
      
      nodes[i].position.x += forces[i].x;
      nodes[i].position.y += forces[i].y;
    }
  }
  
  return nodes;
}

// Function to create tree data from transactions
export function createTransactionTreeData(transactions: Transaction[]) {
  // Base transformation
  let { nodes, edges } = transformTransactionsToTreeData(transactions);
  
  // Optional: Apply force-directed layout for better visual spacing
  // This is a simple implementation and might not be optimal for very large trees
  // nodes = applyForceDirectedLayout(nodes, edges, 50);
  
  return { nodes, edges };
}
