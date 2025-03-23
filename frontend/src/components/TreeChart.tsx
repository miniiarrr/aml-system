import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  NodeTypes,
  EdgeTypes,
  ConnectionLineType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useEffect, useState } from 'react';
import TreeNode from './TreeNode';
import EdgeLabel from './input-page/EdgeLabel';
import { initialNodes, initialEdges } from '../lib/treeData';
import { createTransactionTreeData } from '../lib/transactionTreeData';
import transactionsData from '../all_transactions.json';
import './TreeChart.css';

const nodeTypes: NodeTypes = {
  treeNode: TreeNode,
};

const edgeTypes: EdgeTypes = {
  default: EdgeLabel,
};

export default function TreeChart() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [useTransactionData, setUseTransactionData] = useState(true);

  useEffect(() => {
    if (useTransactionData) {
      try {
        // Convert transaction data to tree format
        const { nodes: txNodes, edges: txEdges } = createTransactionTreeData(transactionsData);
        setNodes(txNodes);
        setEdges(txEdges);
      } catch (error) {
        console.error("Error processing transaction data:", error);
        // Fallback to initial sample data in case of error
        setNodes(initialNodes);
        setEdges(initialEdges);
      }
    } else {
      // Use the initial sample data
      setNodes(initialNodes);
      setEdges(initialEdges);
    }
  }, [useTransactionData]);

  const toggleDataSource = () => {
    setUseTransactionData(!useTransactionData);
  };

  return (
    <div className="tree-chart-container">
      <div className="tree-chart-controls">
        <button 
          onClick={toggleDataSource}
          className="data-toggle-button"
        >
          {useTransactionData ? 'Show Sample Data' : 'Show Transaction Data'}
        </button>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        nodesConnectable={false}
        nodesDraggable={true}
        connectionLineType={ConnectionLineType.Bezier}
        defaultEdgeOptions={{
          type: 'default',
          animated: true
        }}
        fitView
      >
        <Controls />
        {/* <MiniMap 
          nodeColor="#9D00FF" 
          maskColor="rgba(0, 0, 0, 0.1)" 
          className="cyberpunk-minimap"
        /> */}
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
}
