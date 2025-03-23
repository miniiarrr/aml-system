import { Handle, Position, NodeProps } from 'reactflow';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger, Portal } from '@radix-ui/react-tooltip';
import './TreeNode.css';

interface TreeNodeData {
  label: string;
  tooltip?: string;
  url?: string;
}

export default function TreeNode({ data }: NodeProps<TreeNodeData>) {
  const handleNodeClick = () => {
    if (data.url) {
      window.open(data.url, '_blank');
    }
  };

  return (
    <>
      <div 
        className={`cyberpunk-node ${data.url ? 'clickable' : ''}`}
        onClick={handleNodeClick}
      >
        <Handle type="target" position={Position.Left} />
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="node-content">{data.label}</div>
            </TooltipTrigger>
            {data.tooltip && (
              <Portal>
                <TooltipContent side="top" sideOffset={5} align="center" className="node-tooltip-content">
                  <div className="node-tooltip">
                    <div className="node-tooltip-header">NODE DATA</div>
                    <div className="node-tooltip-scanlines"></div>
                    {data.tooltip.split('\n').map((line, i) => (
                      <div key={i} className="tooltip-row">
                        {line}
                      </div>
                    ))}
                  </div>
                </TooltipContent>
              </Portal>
            )}
          </Tooltip>
        </TooltipProvider>
        
        <Handle type="source" position={Position.Right} />
      </div>
    </>
  );
}
