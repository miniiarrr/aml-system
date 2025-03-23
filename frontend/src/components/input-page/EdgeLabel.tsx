import { getBezierPath, EdgeProps, BaseEdge, EdgeLabelRenderer } from 'reactflow';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@radix-ui/react-tooltip';
import './EdgeLabel.css';

interface EdgeLabelData {
  tooltip?: string;
  label?: string;
  amount?: string;
  token?: string;
  details?: Record<string, string>;
}

const EdgeLabel = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  style = {},
  markerEnd
}: EdgeProps<EdgeLabelData>) => {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  // Parse label string if it exists
  const labelText = data?.label || '';
  
  // Extract amount and token from the label or use provided values
  let amount = data?.amount;
  let token = data?.token;
  
  if (!amount && !token && labelText) {
    // If no explicit amount/token provided, try to parse from label
    const lines = labelText.split('\n');
    for (const line of lines) {
      if (line.includes('amount:')) {
        amount = line.split('amount:')[1].trim();
      } else if (line.includes('token:')) {
        token = line.split('token:')[1].trim();
      }
    }
  }

  // Fallback to basic display if parsing fails
  const displayText = amount && token 
    ? `${amount} ${token}` 
    : (labelText.length > 20 ? labelText.substring(0, 20) + '...' : labelText);

  return (
    <>
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} />
      {labelText && (
        <EdgeLabelRenderer>
          <div
            className="edge-label-container"
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
              pointerEvents: 'all',
              zIndex: 5, // Ensure edge labels are above edges
            }}
          >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="edge-label-simple">
                    {displayText}
                  </div>
                </TooltipTrigger>
                <TooltipContent side="top" sideOffset={5} className="edge-tooltip-content">
                  <div className="edge-tooltip">
                    <div className="edge-tooltip-header">TX DATA</div>
                    <div className="edge-tooltip-scanlines"></div>
                    {labelText.split('\n').map((line, i) => (
                      <div key={i} className="tooltip-row">
                        {line}
                      </div>
                    ))}
                    {data?.details && Object.entries(data.details).map(([key, value], i) => (
                      <div key={`detail-${i}`} className="tooltip-row">
                        <span className="tooltip-key">{key}:</span> {value}
                      </div>
                    ))}
                  </div>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
};

export default EdgeLabel;
