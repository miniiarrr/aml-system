import { Node, Edge, Position } from 'reactflow';

export const initialNodes: Node[] = [
  {
    id: '1',
    type: 'treeNode',
    data: { 
      label: 'Root Node',
      tooltip: 'This is the root of the tree' 
    },
    position: { x: 0, y: 100 },
  },
  {
    id: '2',
    type: 'treeNode',
    data: { 
      label: 'Child Node 1',
      tooltip: 'First child node',
      url: 'https://example.com/1'
    },
    position: { x: 350, y: 0 },
  },
  {
    id: '3',
    type: 'treeNode',
    data: { 
      label: 'Child Node 2',
      tooltip: 'Second child node',
      url: 'https://example.com/2'
    },
    position: { x: 350, y: 120 },
  },
  {
    id: '4',
    type: 'treeNode',
    data: { 
      label: 'Child Node 3',
      tooltip: 'Third child node'
    },
    position: { x: 350, y: 240 },
  },
  {
    id: '5',
    type: 'treeNode',
    data: { 
      label: 'Grandchild 1',
      tooltip: 'Child of Child Node 2'
    },
    position: { x: 700, y: 60 },
  },
  {
    id: '6',
    type: 'treeNode',
    data: { 
      label: 'Grandchild 2',
      tooltip: 'Another child of Child Node 2'
    },
    position: { x: 700, y: 180 },
  },
  // New nodes added here
  {
    id: '7',
    type: 'treeNode',
    data: { 
      label: 'Grandchild 3',
      tooltip: 'Child of Child Node 3'
    },
    position: { x: 700, y: 240 },
  },
  {
    id: '8',
    type: 'treeNode',
    data: { 
      label: 'Great-Grandchild 1',
      tooltip: 'Child of Grandchild 1',
      url: 'https://example.com/8'
    },
    position: { x: 1050, y: 0 },
  },
  {
    id: '9',
    type: 'treeNode',
    data: { 
      label: 'Great-Grandchild 2',
      tooltip: 'Child of Grandchild 1'
    },
    position: { x: 1050, y: 120 },
  },
  {
    id: '10',
    type: 'treeNode',
    data: { 
      label: 'Great-Grandchild 3',
      tooltip: 'Child of Grandchild 2'
    },
    position: { x: 1050, y: 180 },
  },
  {
    id: '11',
    type: 'treeNode',
    data: { 
      label: 'Great-Grandchild 4',
      tooltip: 'Child of Grandchild 3'
    },
    position: { x: 1050, y: 240 },
  },
  {
    id: '12',
    type: 'treeNode',
    data: { 
      label: 'Child Node 4',
      tooltip: 'Fourth child node'
    },
    position: { x: 350, y: 360 },
  },
  {
    id: '13',
    type: 'treeNode',
    data: { 
      label: 'Great-Great-Grandchild',
      tooltip: 'Fourth generation node',
      url: 'https://example.com/13'
    },
    position: { x: 1400, y: 120 },
  },
  // Adding new nodes
  {
    id: '14',
    type: 'treeNode',
    data: { 
      label: 'DeFi Hub',
      tooltip: 'Decentralized Finance Center',
      url: 'https://example.com/defi'
    },
    position: { x: 350, y: 480 },
  },
  {
    id: '15',
    type: 'treeNode',
    data: { 
      label: 'Lending Protocol',
      tooltip: 'Decentralized Lending Platform',
      url: 'https://example.com/lending'
    },
    position: { x: 700, y: 420 },
  },
  {
    id: '16',
    type: 'treeNode',
    data: { 
      label: 'DEX Platform',
      tooltip: 'Decentralized Exchange',
      url: 'https://example.com/dex'
    },
    position: { x: 700, y: 540 },
  },
  {
    id: '17',
    type: 'treeNode',
    data: { 
      label: 'Yield Farming',
      tooltip: 'Yield Optimization Protocol',
      url: 'https://example.com/yield'
    },
    position: { x: 1050, y: 420 },
  },
  {
    id: '18',
    type: 'treeNode',
    data: { 
      label: 'NFT Marketplace',
      tooltip: 'Digital Art Marketplace',
      url: 'https://example.com/nft'
    },
    position: { x: 1050, y: 540 },
  },
  {
    id: '19',
    type: 'treeNode',
    data: { 
      label: 'Layer 2 Solution',
      tooltip: 'Ethereum Scaling Solution',
      url: 'https://example.com/l2'
    },
    position: { x: 1400, y: 420 },
  },
  {
    id: '20',
    type: 'treeNode',
    data: { 
      label: 'DAO Governance',
      tooltip: 'Decentralized Autonomous Organization',
      url: 'https://example.com/dao'
    },
    position: { x: 1400, y: 540 },
  }
];

export const initialEdges: Edge[] = [
  {
    id: 'e1-2',
    source: '1',
    target: '2',
   
    data: {
      label: 'ETH - 0.01\n2025.01.01 - 12:53:12',
      tooltip: 'Ethereum transaction',
      token: 'ETH',
      amount: 0.01,
      chain: 'Ethereum',
      date: '2025.01.01 - 12:53:12'
    },
  },
  {
    id: 'e1-3',
    source: '1',
    target: '3',
   
    data: {
      label: 'BTC - 0.005\n2025.01.02 - 14:27:33',
      tooltip: 'Bitcoin transaction',
      token: 'BTC',
      amount: 0.005,
      chain: 'Bitcoin',
      date: '2025.01.02 - 14:27:33'
    },
  },
  {
    id: 'e1-4',
    source: '1',
    target: '4',
   
    data: {
      label: 'SOL - 1.25\n2025.01.03 - 09:15:47',
      tooltip: 'Solana transaction',
      token: 'SOL',
      amount: 1.25,
      chain: 'Solana',
      date: '2025.01.03 - 09:15:47'
    },
  },
  {
    id: 'e3-5',
    source: '3',
    target: '5',
   
    data: {
      label: 'DOT - 3.75\n2025.01.04 - 17:42:59',
      tooltip: 'Polkadot transaction',
      token: 'DOT',
      amount: 3.75,
      chain: 'Polkadot',
      date: '2025.01.04 - 17:42:59'
    },
  },
  {
    id: 'e3-6',
    source: '3',
    target: '6',
   
    data: {
      label: 'AVAX - 2.33\n2025.01.05 - 08:11:26',
      tooltip: 'Avalanche transaction',
      token: 'AVAX',
      amount: 2.33,
      chain: 'Avalanche',
      date: '2025.01.05 - 08:11:26'
    },
  },
  // New edges added here
  {
    id: 'e4-7',
    source: '4',
    target: '7',
   
    data: {
      label: 'MATIC - 15.5\n2025.01.06 - 11:22:05',
      tooltip: 'Polygon transaction',
      token: 'MATIC',
      amount: 15.5,
      chain: 'Polygon',
      date: '2025.01.06 - 11:22:05'
    },
  },
  {
    id: 'e5-8',
    source: '5',
    target: '8',
   
    data: {
      label: 'LINK - 2.75\n2025.01.07 - 13:45:30',
      tooltip: 'Chainlink transaction',
      token: 'LINK',
      amount: 2.75,
      chain: 'Chainlink',
      date: '2025.01.07 - 13:45:30'
    },
  },
  {
    id: 'e5-9',
    source: '5',
    target: '9',
   
    data: {
      label: 'XRP - 50.0\n2025.01.08 - 16:33:21',
      tooltip: 'Ripple transaction',
      token: 'XRP',
      amount: 50.0,
      chain: 'Ripple',
      date: '2025.01.08 - 16:33:21'
    },
  },
  {
    id: 'e6-10',
    source: '6',
    target: '10',
   
    data: {
      label: 'ADA - 100.25\n2025.01.09 - 09:05:17',
      tooltip: 'Cardano transaction',
      token: 'ADA',
      amount: 100.25,
      chain: 'Cardano',
      date: '2025.01.09 - 09:05:17'
    },
  },
  {
    id: 'e7-11',
    source: '7',
    target: '11',
   
    data: {
      label: 'DOGE - 420.69\n2025.01.10 - 04:20:00',
      tooltip: 'Dogecoin transaction',
      token: 'DOGE',
      amount: 420.69,
      chain: 'Dogecoin',
      date: '2025.01.10 - 04:20:00'
    },
  },
  {
    id: 'e1-12',
    source: '1',
    target: '12',
   
    data: {
      label: 'SHIB - 1000000\n2025.01.11 - 15:30:45',
      tooltip: 'Shiba Inu transaction',
      token: 'SHIB',
      amount: 1000000,
      chain: 'Shiba Inu',
      date: '2025.01.11 - 15:30:45'
    },
  },
  {
    id: 'e9-13',
    source: '9',
    target: '13',
   
    data: {
      label: 'UNI - 5.5\n2025.01.12 - 10:15:33',
      tooltip: 'Uniswap transaction',
      token: 'UNI',
      amount: 5.5,
      chain: 'Uniswap',
      date: '2025.01.12 - 10:15:33'
    },
  },
  // Adding new edges
  {
    id: 'e1-14',
    source: '1',
    target: '14',
   
    data: {
      label: 'AAVE - 12.8\n2025.01.13 - 18:22:41',
      tooltip: 'AAVE protocol interaction',
      token: 'AAVE',
      amount: 12.8,
      chain: 'Ethereum',
      date: '2025.01.13 - 18:22:41'
    },
  },
  {
    id: 'e14-15',
    source: '14',
    target: '15',
   
    data: {
      label: 'COMP - 3.25\n2025.01.14 - 07:35:19',
      tooltip: 'Compound governance token',
      token: 'COMP',
      amount: 3.25,
      chain: 'Ethereum',
      date: '2025.01.14 - 07:35:19'
    },
  },
  {
    id: 'e14-16',
    source: '14',
    target: '16',
   
    data: {
      label: 'SUSHI - 45.33\n2025.01.15 - 11:05:52',
      tooltip: 'SushiSwap DEX transaction',
      token: 'SUSHI',
      amount: 45.33,
      chain: 'Ethereum',
      date: '2025.01.15 - 11:05:52'
    },
  },
  {
    id: 'e15-17',
    source: '15',
    target: '17',
   
    data: {
      label: 'CAKE - 75.5\n2025.01.16 - 14:47:03',
      tooltip: 'PancakeSwap yield farming',
      token: 'CAKE',
      amount: 75.5,
      chain: 'Binance Smart Chain',
      date: '2025.01.16 - 14:47:03'
    },
  },
  {
    id: 'e16-18',
    source: '16',
    target: '18',
   
    data: {
      label: 'SAND - 230.15\n2025.01.17 - 19:26:38',
      tooltip: 'The Sandbox metaverse token',
      token: 'SAND',
      amount: 230.15,
      chain: 'Ethereum',
      date: '2025.01.17 - 19:26:38'
    },
  },
  {
    id: 'e17-19',
    source: '17',
    target: '19',
   
    data: {
      label: 'LRC - 512.33\n2025.01.18 - 09:33:15',
      tooltip: 'Loopring L2 scaling solution',
      token: 'LRC',
      amount: 512.33,
      chain: 'Ethereum',
      date: '2025.01.18 - 09:33:15'
    },
  },
  {
    id: 'e18-20',
    source: '18',
    target: '20',
   
    data: {
      label: 'ENS - 1.5\n2025.01.19 - 22:14:37',
      tooltip: 'Ethereum Name Service governance',
      token: 'ENS',
      amount: 1.5,
      chain: 'Ethereum',
      date: '2025.01.19 - 22:14:37'
    },
  },
  {
    id: 'e12-15',
    source: '12',
    target: '15',
   
    data: {
      label: 'MKR - 0.08\n2025.01.20 - 13:48:55',
      tooltip: 'MakerDAO governance token',
      token: 'MKR',
      amount: 0.08,
      chain: 'Ethereum',
      date: '2025.01.20 - 13:48:55'
    },
  },
  {
    id: 'e10-18',
    source: '10',
    target: '18',
   
    data: {
      label: 'MANA - 350.45\n2025.01.21 - 16:03:22',
      tooltip: 'Decentraland virtual real estate',
      token: 'MANA',
      amount: 350.45,
      chain: 'Ethereum',
      date: '2025.01.21 - 16:03:22'
    },
  }
];

// Generate a large tree dataset with ~50,000 nodes and edges
export const generateLargeTreeData = (nodeCount = 25000) => {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  
  // Constants for layout
  const LEVEL_HEIGHT = 120;
  const HORIZONTAL_SPACING = 150;
  
  // Helper function to create a node
  const createNode = (id: number, label: string, level: number, position: number) => {
    // Calculate x, y position based on level and position within level
    const x = position * HORIZONTAL_SPACING;
    const y = level * LEVEL_HEIGHT;
    
    nodes.push({
      id: id.toString(),
      type: 'treeNode',
      data: { 
        label,
        tooltip: `Level ${level}, Position ${position}`
      },
      position: { x, y },
    });
    
    return id.toString();
  };
  
  // Create a structured tree
  const createTree = (maxNodes: number) => {
    let nodeId = 0;
    
    // Create root node
    const rootId = createNode(nodeId++, "Root", 0, 0);
    
    if (maxNodes <= 1) return;
    
    // Queue for BFS tree generation [nodeId, level, horizontalPosition]
    const queue: [string, number, number][] = [[rootId, 0, 0]];
    
    // Keep track of nodes per level for positioning
    const nodesPerLevel: number[] = [1]; // Level 0 has 1 node (root)
    
    while (nodeId < maxNodes && queue.length > 0) {
      const [parentId, parentLevel, parentPosition] = queue.shift()!;
      const nextLevel = parentLevel + 1;
      
      // Initialize count for the next level if not already set
      if (!nodesPerLevel[nextLevel]) {
        nodesPerLevel[nextLevel] = 0;
      }
      
      // Determine number of children (decreases with depth)
      const maxChildrenForLevel = Math.max(1, Math.floor(10 / (nextLevel + 1)));
      const childrenCount = Math.min(
        maxChildrenForLevel,
        // More children for nodes closer to center
        Math.max(1, Math.floor(Math.random() * maxChildrenForLevel))
      );
      
      for (let i = 0; i < childrenCount && nodeId < maxNodes; i++) {
        // Create child node
        const childLabel = `Node ${parentId}-${i+1}`;
        const childPosition = nodesPerLevel[nextLevel];
        const childId = createNode(nodeId++, childLabel, nextLevel, childPosition);
        
        // Create edge from parent to child
        edges.push({
          id: `e${parentId}-${childId}`,
          source: parentId,
          target: childId,
          type: 'customEdge',
          data: {
            label: `${parentId} → ${childId}`
          }
        });
        
        // Increment position counter for this level
        nodesPerLevel[nextLevel]++;
        
        // Add child to queue if not too deep
        if (nextLevel < 15) { // Limit depth to prevent too much recursion
          queue.push([childId, nextLevel, childPosition]);
        }
      }
    }
  };
  
  // Generate the tree
  createTree(nodeCount);
  
  return { nodes, edges };
};

// Generate and export different sized datasets
export const smallTreeData = { nodes: initialNodes as Node[], edges: initialEdges as Edge[] };
export const mediumTreeData = generateLargeTreeData(1000);
export const largeTreeData = generateLargeTreeData(5000);
export const veryLargeTreeData = generateLargeTreeData(25000); // ~50k elements (nodes + edges)

export default smallTreeData;
