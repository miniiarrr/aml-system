from typing import Dict, Optional, List, Any
from loguru import logger
from .workflow import Workflow, WorkflowStatus
from .models import TransactionInput

class WorkflowManager:
    """
    Manages the lifecycle of workflows in the system.
    
    This class is responsible for:
    - Storing and tracking all running workflows
    - Updating workflow statuses based on events from the AI agent system
    - Providing access to workflow statuses and information
    """
    
    def __init__(self):
        """Initialize the workflow manager with an empty workflow store."""
        self._workflows: Dict[str, Workflow] = {}
        logger.info("Initialized WorkflowManager")
    
    def add_workflow(self, workflow: Workflow) -> None:
        """
        Add a new workflow to the manager.
        
        Args:
            workflow (Workflow): The workflow instance to add
            
        Raises:
            ValueError: If a workflow with the same ID already exists
        """
        if workflow.workflow_id in self._workflows:
            raise ValueError(f"Workflow with ID {workflow.workflow_id} already exists")
        
        self._workflows[workflow.workflow_id] = workflow
        logger.info(f"Added new workflow: {workflow.name} (ID: {workflow.workflow_id})")
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Retrieve a workflow by its ID.
        
        Args:
            workflow_id (str): The ID of the workflow to retrieve
            
        Returns:
            Optional[Workflow]: The workflow instance if found, None otherwise
        """
        return self._workflows.get(workflow_id)
    
    def get_all_workflows(self) -> List[Workflow]:
        """
        Get all workflows managed by this instance.
        
        Returns:
            List[Workflow]: List of all workflow instances
        """
        return list(self._workflows.values())
    
    def update_workflow_status(self, workflow_id: str, new_status: WorkflowStatus) -> bool:
        """
        Update the status of a workflow.
        
        Args:
            workflow_id (str): The ID of the workflow to update
            new_status (WorkflowStatus): The new status to set
            
        Returns:
            bool: True if the update was successful, False if the workflow was not found
        """
        workflow = self.get_workflow(workflow_id)
        if workflow is None:
            logger.warning(f"Attempted to update status of non-existent workflow: {workflow_id}")
            return False
        
        workflow.update_status(new_status)
        logger.info(f"Updated workflow {workflow_id} status to: {new_status.value}")
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """
        Get the current status of a workflow.
        
        Args:
            workflow_id (str): The ID of the workflow to check
            
        Returns:
            Optional[WorkflowStatus]: The current status if the workflow exists, None otherwise
        """
        workflow = self.get_workflow(workflow_id)
        return workflow.status if workflow else None
    
    def remove_workflow(self, workflow_id: str) -> bool:
        """
        Remove a workflow from the manager.
        
        Args:
            workflow_id (str): The ID of the workflow to remove
            
        Returns:
            bool: True if the workflow was removed, False if it was not found
        """
        if workflow_id in self._workflows:
            del self._workflows[workflow_id]
            logger.info(f"Removed workflow: {workflow_id}")
            return True
        return False
    
    async def start_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> bool:
        """
        Start a workflow by sending initial request to AI agent system.
        
        Args:
            workflow_id (str): ID of the workflow to start
            input_data (Dict[str, Any]): Input data for the workflow
            
        Returns:
            bool: True if the workflow was started successfully, False otherwise
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_id}")
            return False
            
        return await workflow.start(input_data)
    
    def add_transaction(self, workflow_id: str, transaction: TransactionInput) -> Optional[Dict]:
        """
        Add a transaction to a workflow.
        
        Args:
            workflow_id (str): ID of the workflow to add the transaction to
            transaction (TransactionInput): Transaction data to add
            
        Returns:
            Optional[Dict]: The created edge data if successful, None if workflow not found
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_id}")
            return None
            
        try:
            edge = workflow.add_transaction(transaction)
            return edge.model_dump()
        except Exception as e:
            logger.error(f"Error adding transaction to workflow {workflow_id}: {str(e)}")
            return None

    async def add_transaction_event(self, event: Dict[str, Any]) -> Optional[Dict]:
        """
        Process a transaction event from the MongoDB change stream.
        
        This method is called when a new transaction is added to the database
        or an existing transaction is updated. It extracts the transaction data
        and forwards it to the appropriate workflow.
        
        Args:
            event (Dict[str, Any]): Change event from MongoDB change stream
            
        Returns:
            Optional[Dict]: The created edge data if successful, None if workflow not found or error
        """
        try:
            # Extract the full document from the event
            document = event.get('fullDocument')
            if not document:
                logger.warning("Received change event with no fullDocument")
                return None
            
            # Extract workflow_id from the document
            workflow_id = document.get('workflow_id')
            if not workflow_id:
                logger.warning("Transaction document has no workflow_id field")
                return None
            
            # Convert MongoDB document to TransactionInput
            transaction = TransactionInput(
                from_blockchain=document.get('from_blockchain'),
                from_wallet=document.get('from_wallet'),
                to_blockchain=document.get('to_blockchain'),
                to_wallet=document.get('to_wallet'),
                hash=document.get('hash'),
                sum=document.get('sum'),
                ticker_token=document.get('ticker_token'),
                date=document.get('date'),
                prev_hash=document.get('prev_hash')
            )
            
            # Add the transaction to the workflow
            result = self.add_transaction(workflow_id, transaction)
            if result:
                logger.info(f"Successfully processed transaction event for workflow {workflow_id}")
            else:
                logger.warning(f"Failed to process transaction event for workflow {workflow_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing transaction event: {str(e)}")
            return None
