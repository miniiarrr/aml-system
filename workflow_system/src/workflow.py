from datetime import datetime, UTC
from typing import Optional, Dict, Any
from loguru import logger
import aiohttp

from config import CONFIGS
from .models import (
    WorkflowStatus,
    TransactionType,
    TransactionInput,
    Node,
    Edge,
    LogType
)
from .buffer import WorkflowBuffer

class Workflow:
    """
    Base class for workflow implementations.
    
    This class serves as a boilerplate for specific workflow implementations.
    It provides basic workflow functionality and status management.
    """
    
    def __init__(self, workflow_id: str, name: str, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize a new workflow instance.
        
        Args:
            workflow_id (str): Unique identifier for the workflow
            name (str): Name of the workflow
            parameters (Optional[Dict[str, Any]]): Optional parameters for the workflow
        """
        self.workflow_id = workflow_id
        self.name = name
        self.parameters = parameters or {}
        self.status = WorkflowStatus.INITIALIZED
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
        
        # Graph structure
        self.nodes: Dict[int, Node] = {}
        self.edges: Dict[int, Edge] = {}
        
        # ID counters
        self._next_node_id = 1
        self._next_edge_id = 1
        
        # Initialize buffer
        self.buffer = WorkflowBuffer()
        
        logger.info(f"Created new workflow: {self.name} (ID: {self.workflow_id})")
        self.buffer.add_log(f"Created new workflow: {self.name} (ID: {self.workflow_id})", LogType.INFO)
    
    async def start(self, input_data: Dict[str, Any]) -> bool:
        """
        Start the workflow by sending initial request to AI agent system.
        
        Args:
            input_data (Dict[str, Any]): Input data for the workflow
            
        Returns:
            bool: True if the workflow was started successfully, False otherwise
        """
        if CONFIGS.ENV == "local":
            self.update_status(WorkflowStatus.PROCESSING)
            self.buffer.add_log(f"Started workflow {self.workflow_id}", LogType.INFO)
            return True
        
        try:
            async with aiohttp.ClientSession() as session:
                # Send initial request to AI agent system
                async with session.post(
                    "http://localhost:8001/agent/start",
                    json={
                        "workflow_id": self.workflow_id,
                        "input": input_data
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Failed to start AI agent process: {error_text}")
                    
                    # Update status to processing
                    self.update_status(WorkflowStatus.PROCESSING)
                    logger.info(f"Started workflow {self.workflow_id}")
                    self.buffer.add_log(f"Started workflow {self.workflow_id}", LogType.INFO)
                    return True
            
        except Exception as e:
            self.error = str(e)
            self.update_status(WorkflowStatus.ERROR)
            logger.error(f"Failed to start workflow {self.workflow_id}: {str(e)}")
            self.buffer.add_log(f"Failed to start workflow {self.workflow_id}: {str(e)}", LogType.ERROR)
            return False
    
    def add_node(self, wallet: str, blockchain: str, link_etherscan: str) -> Node:
        """
        Add a new node to the workflow graph.
        
        Args:
            wallet (str): Wallet address
            blockchain (str): Blockchain identifier
            link_etherscan (str): Etherscan link for the wallet
            
        Returns:
            Node: The created node
        """
        node = Node(
            internal_id=self._next_node_id,
            wallet=wallet,
            blockchain=blockchain,
            link_etherscan=link_etherscan
        )
        self.nodes[node.internal_id] = node
        self._next_node_id += 1
        logger.info(f"Added node to workflow {self.workflow_id}: {wallet} (ID: {node.internal_id})")
        self.buffer.add_node(node)
        self.buffer.add_log(f"Added node to workflow {self.workflow_id}: {wallet} (ID: {node.internal_id})", LogType.INFO)
        return node
    
    def add_edge(self, from_node_id: int, to_node_id: int, sum: float, ticker_token: str,
                 type: TransactionType, date: datetime, hash: str, etherscan_link: str,
                 extra: Optional[Dict[str, Any]] = None) -> Edge:
        """
        Add a new edge to the workflow graph.
        
        Args:
            from_node_id (int): Internal ID of the source node
            to_node_id (int): Internal ID of the target node
            sum (float): Transaction amount
            ticker_token (str): Token ticker
            type (TransactionType): Edge type (duplicate or transaction)
            date (datetime): Transaction date
            hash (str): Transaction hash
            etherscan_link (str): Etherscan link for the transaction
            extra (Optional[Dict[str, Any]]): Additional edge data
            
        Returns:
            Edge: The created edge
            
        Raises:
            ValueError: If either from_node_id or to_node_id doesn't exist
        """
        # Verify nodes exist
        if from_node_id not in self.nodes:
            raise ValueError(f"Source node with ID {from_node_id} not found")
        if to_node_id not in self.nodes:
            raise ValueError(f"Target node with ID {to_node_id} not found")
        
        edge = Edge(
            internal_id=self._next_edge_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            sum=sum,
            ticker_token=ticker_token,
            type=type,
            date=date,
            hash=hash,
            etherscan_link=etherscan_link,
            extra=extra
        )
        self.edges[edge.internal_id] = edge
        self._next_edge_id += 1
        logger.info(f"Added edge to workflow {self.workflow_id}: {hash} (ID: {edge.internal_id})")
        self.buffer.add_edge(edge)
        self.buffer.add_log(f"Added edge to workflow {self.workflow_id}: {hash} (ID: {edge.internal_id})", LogType.INFO)
        return edge
    
    def add_transaction(self, transaction: TransactionInput) -> Edge:
        """
        Add a transaction to the workflow, creating necessary nodes if they don't exist.
        
        Args:
            transaction (TransactionInput): Transaction data
            
        Returns:
            Edge: The created edge representing the transaction
        """
        if transaction.prev_hash:
            from_node_id = next((edge.to_node_id for edge in self.edges.values() if edge.hash == transaction.prev_hash), None)
            # Find or create source node
            from_node = self.nodes.get(from_node_id, None)
            if not from_node:
                from_node = self.add_node(
                    wallet=transaction.from_wallet,
                    blockchain=transaction.from_blockchain,
                    link_etherscan=f"https://etherscan.io/address/{transaction.from_wallet}"
                )
        else:
            from_node = next(
                (node for node in self.nodes.values() if node.wallet == transaction.from_wallet),
                None
            )
            if not from_node:
                from_node = self.add_node(
                    wallet=transaction.from_wallet,
                    blockchain=transaction.from_blockchain,
                    link_etherscan=f"https://etherscan.io/address/{transaction.from_wallet}"
                )
        
        # Find or create target node
        to_node = next(
            (node for node in self.nodes.values() if node.wallet == transaction.to_wallet),
            None
        )
        if not to_node:
            to_node = self.add_node(
                wallet=transaction.to_wallet,
                blockchain=transaction.to_blockchain,
                link_etherscan=f"https://etherscan.io/address/{transaction.to_wallet}"
            )
        else:
            to_node = self.add_node(
                wallet=transaction.to_wallet,
                blockchain=transaction.to_blockchain,
                link_etherscan=f"https://etherscan.io/address/{transaction.to_wallet}"
            )
            self.add_edge(
                from_node_id=from_node.internal_id,
                to_node_id=to_node.internal_id,
                ticker_token=transaction.ticker_token,
                type=TransactionType.DUPLICATE,
            )
        
        # Create edge with transaction data
        edge = self.add_edge(
            from_node_id=from_node.internal_id,
            to_node_id=to_node.internal_id,
            sum=transaction.sum,
            ticker_token=transaction.ticker_token,
            type=TransactionType.TRANSACTION,
            date=transaction.date,
            hash=transaction.hash,
            etherscan_link=f"https://etherscan.io/tx/{transaction.hash}",
            extra={"prev_hash": transaction.prev_hash}
        )
        
        logger.info(f"Added transaction to workflow {self.workflow_id}: {transaction.hash}")
        self.buffer.add_log(f"Added transaction to workflow {self.workflow_id}: {transaction.hash}", LogType.INFO)
        return edge
    
    def update_status(self, new_status: WorkflowStatus) -> None:
        """
        Update the workflow status and timestamp.
        
        Args:
            new_status (WorkflowStatus): New status to set
        """
        self.status = new_status
        self.updated_at = datetime.now(UTC)
        logger.info(f"Workflow {self.workflow_id} status updated to: {new_status.value}")
        self.buffer.set_status(new_status)
        self.buffer.add_log(f"Workflow {self.workflow_id} status updated to: {new_status.value}", LogType.INFO)
    
    def get_buffer(self) -> dict:
        """
        Get the workflow buffer.
        """
        result = self.buffer.to_dict()
        self.buffer.clear()
        return result

    def has_changes(self) -> bool:
        """
        Check if there are any buffered changes in the workflow.
        
        Returns:
            bool: True if there are any new nodes, edges, status changes, or logs
        """
        return self.buffer.has_changes()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the workflow instance to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the workflow
        """
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "parameters": self.parameters,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result,
            "error": self.error,
            "nodes": {
                node_id: {
                    "internal_id": node.internal_id,
                    "wallet": node.wallet,
                    "blockchain": node.blockchain,
                    "link_etherscan": node.link_etherscan
                }
                for node_id, node in self.nodes.items()
            },
            "edges": {
                edge_id: {
                    "internal_id": edge.internal_id,
                    "from_node_id": edge.from_node_id,
                    "to_node_id": edge.to_node_id,
                    "sum": edge.sum,
                    "ticker_token": edge.ticker_token,
                    "type": edge.type.value,
                    "date": edge.date.isoformat(),
                    "hash": edge.hash,
                    "etherscan_link": edge.etherscan_link,
                    "extra": edge.extra
                }
                for edge_id, edge in self.edges.items()
            },
            "buffer": self.buffer.to_dict()
        }
