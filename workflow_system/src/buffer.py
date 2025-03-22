from typing import List, Optional, Dict, Any
from .models import Node, Edge, WorkflowStatus, LogEntry, LogType

class WorkflowBuffer:
    """
    Buffer class to store workflow state changes and logs.
    """
    def __init__(self):
        self.new_nodes: List[Node] = []
        self.new_edges: List[Edge] = []
        self.status: Optional[WorkflowStatus] = None
        self.logs: List[LogEntry] = []
    
    def add_node(self, node: Node) -> None:
        """Add a new node to the buffer."""
        self.new_nodes.append(node)
    
    def add_edge(self, edge: Edge) -> None:
        """Add a new edge to the buffer."""
        self.new_edges.append(edge)
    
    def set_status(self, status: WorkflowStatus) -> None:
        """Set the workflow status."""
        self.status = status
    
    def add_log(self, message: str, log_type: LogType = LogType.INFO) -> None:
        """
        Add a log message to the buffer.
        
        Args:
            message (str): The log message
            log_type (LogType): The type of log entry (default: INFO)
        """
        self.logs.append(LogEntry(message=message, type=log_type))
    
    def clear(self) -> None:
        """Clear all buffered changes."""
        self.new_nodes.clear()
        self.new_edges.clear()
        self.status = None
        self.logs.clear()
    
    def has_changes(self) -> bool:
        """Check if there are any buffered changes."""
        return bool(self.new_nodes or self.new_edges or self.status or self.logs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert buffer contents to a dictionary."""
        return {
            "new_nodes": [node.model_dump() for node in self.new_nodes],
            "new_edges": [edge.model_dump() for edge in self.new_edges],
            "status": self.status.value if self.status else None,
            "logs": [
                {
                    "message": log.message,
                    "type": log.type.value,
                    "timestamp": log.timestamp.isoformat()
                }
                for log in self.logs
            ]
        } 