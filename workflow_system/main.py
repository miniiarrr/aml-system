from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import uuid
import asyncio
from typing import Dict
import json
from src.models import TransactionInput, WorkflowStatus, InitNodeInput
from src.workflow_manager import WorkflowManager
from src.workflow import Workflow
from src.database import db, setup_transaction_watcher

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow manager
workflow_manager = WorkflowManager()

# In-memory storage for workflow states
workflows: Dict[str, Dict] = {}

class WorkflowUpdate(BaseModel):
    status: str
    message: str

@app.on_event("startup")
async def startup_event():
    """
    Initialize connections and services on application startup.
    """
    # Connect to MongoDB
    connected = await db.connect()
    if not connected:
        raise Exception("Failed to connect to MongoDB")
    
    # Set up transaction watcher
    watcher_setup = await setup_transaction_watcher(workflow_manager)
    if not watcher_setup:
        raise Exception("Failed to set up transaction watcher")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up connections and resources on application shutdown.
    """
    # Disconnect from MongoDB
    await db.disconnect()

@app.post("/workflow/start")
async def start_workflow(request: Request):
    """
    Start a new workflow.
    
    Args:
        request (Request): The incoming request containing workflow input data
        background_tasks (BackgroundTasks): FastAPI background tasks
        
    Returns:
        Dict: Contains the workflow ID if successful
        
    Raises:
        HTTPException: If workflow creation fails
    """
    try:
        data = await request.json()
        workflow_id = str(uuid.uuid4()) if not data.get("workflow_id", None) else data.get("workflow_id")
        
        # Create new workflow
        workflow = Workflow(
            workflow_id=workflow_id,
            name=data.get("name", "Unnamed Workflow"),
            parameters=data.get("parameters", {}),
        )
        
        # Add workflow to manager
        workflow_manager.add_workflow(workflow)
        
        # Start the workflow
        success = await workflow_manager.start_workflow(workflow_id, data.get("input", {}))
        if not success:
            raise HTTPException(status_code=500, detail="Failed to start workflow")
        
        return {"workflow_id": workflow_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/{workflow_id}/init_node")
async def init_node(workflow_id: str, node_data: InitNodeInput):
    """
    Initialize a workflow with a node.
    
    Args:
        workflow_id (str): ID of the workflow to add the node to
        node_data (InitNodeInput): Node data to add
        
    Returns:
        Dict: The created node data if successful
        
    Raises:
        HTTPException: If workflow not found or node creation fails
    """
    try:
        workflow = workflow_manager.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
            
        # Add node to workflow
        node = workflow.add_node(
            wallet=node_data.wallet,
            blockchain=node_data.blockchain,
            link_etherscan=node_data.link_etherscan
        )
        
        # Return node data
        return {
            "internal_id": node.internal_id,
            "wallet": node.wallet,
            "blockchain": node.blockchain,
            "link_etherscan": node.link_etherscan
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/{workflow_id}/add_transaction")
async def add_transaction(workflow_id: str, transaction: TransactionInput):
    """
    Add a transaction to a workflow.
    
    Args:
        workflow_id (str): ID of the workflow to add the transaction to
        transaction (TransactionInput): Transaction data to add
        
    Returns:
        Dict: The created edge data if successful
        
    Raises:
        HTTPException: If workflow not found or transaction addition fails
    """
    result = workflow_manager.add_transaction(workflow_id, transaction)
    if result is None:
        raise HTTPException(status_code=404, detail="Workflow not found or transaction addition failed")
    return result

@app.get("/workflow/{workflow_id}/events")
async def workflow_events(workflow_id: str):
    workflow = workflow_manager.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    async def event_generator():
        while workflow.status not in [WorkflowStatus.COMPLETED, WorkflowStatus.ERROR, WorkflowStatus] or workflow.has_changes():
            if workflow.has_changes():
                data = workflow.get_buffer()
                yield {
                    "event": "message",
                    "data": json.dumps(data)
                }
            await asyncio.sleep(1)
    
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 