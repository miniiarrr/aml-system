from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class LogType(str, Enum):
    """Enumeration of possible log types."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"

class LogEntry(BaseModel):
    """Represents a log entry with message and type."""
    message: str
    type: LogType
    timestamp: datetime = datetime.now()

class WorkflowStatus(str, Enum):
    """Enumeration of possible workflow statuses."""
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELED = "canceled"

class TransactionType(str, Enum):
    """Enumeration of possible transaction types."""
    TRANSACTION = "transaction"
    DUPLICATE = "duplicate"

class InitNodeInput(BaseModel):
    """Input model for initial node data."""
    wallet: str
    blockchain: str
    link_etherscan: str

class TransactionInput(BaseModel):
    """Input model for transaction data."""
    from_blockchain: str
    from_wallet: str
    to_blockchain: str
    to_wallet: str
    hash: str
    sum: float
    ticker_token: str
    date: str
    prev_hash: str | None = None

class Node(BaseModel):
    """Represents a node in the workflow graph."""
    internal_id: int
    wallet: str
    blockchain: str
    link_etherscan: str

class Edge(BaseModel):
    """Represents an edge in the workflow graph."""
    internal_id: int
    from_node_id: int
    to_node_id: int
    sum: float
    ticker_token: str
    type: TransactionType
    date: str
    hash: str
    etherscan_link: str
    extra: Optional[Dict[str, Any]] = None 