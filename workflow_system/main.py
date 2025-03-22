from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import uuid
import asyncio
from typing import Dict, List
import requests
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for workflow states
workflows: Dict[str, Dict] = {}

class WorkflowUpdate(BaseModel):
    status: str
    message: str

@app.post("/workflow/start")
async def start_workflow():
    workflow_id = str(uuid.uuid4())
    workflows[workflow_id] = {
        "status": "initialized",
        "messages": [],
        "completed": False
    }
    
    # Start the workflow process
    asyncio.create_task(process_workflow(workflow_id))
    
    return {"workflow_id": workflow_id}

@app.get("/workflow/{workflow_id}/events")
async def workflow_events(workflow_id: str):
    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    async def event_generator():
        while not workflows[workflow_id]["completed"]:
            if workflows[workflow_id]["messages"]:
                message = workflows[workflow_id]["messages"].pop(0)
                yield {
                    "event": "message",
                    "data": json.dumps({
                        "status": workflows[workflow_id]["status"],
                        "message": message
                    })
                }
            await asyncio.sleep(0.1)
    
    return EventSourceResponse(event_generator())

async def process_workflow(workflow_id: str):
    try:
        # Update workflow status
        workflows[workflow_id]["status"] = "processing"
        workflows[workflow_id]["messages"].append("Workflow started processing")
        
        # Send initial request to AI agent system
        response = requests.post(
            "http://localhost:8001/agent/start",
            json={"workflow_id": workflow_id}
        )
        
        if response.status_code != 200:
            raise Exception("Failed to start AI agent process")
        
        # Monitor AI agent progress
        while not workflows[workflow_id]["completed"]:
            agent_response = requests.get(
                f"http://localhost:8001/agent/{workflow_id}/status"
            )
            
            if agent_response.status_code == 200:
                agent_data = agent_response.json()
                workflows[workflow_id]["status"] = agent_data["status"]
                workflows[workflow_id]["messages"].append(agent_data["message"])
                
                if agent_data["completed"]:
                    workflows[workflow_id]["completed"] = True
                    break
            
            await asyncio.sleep(1)
        
        workflows[workflow_id]["messages"].append("Workflow completed successfully")
        
    except Exception as e:
        workflows[workflow_id]["status"] = "error"
        workflows[workflow_id]["messages"].append(f"Error: {str(e)}")
        workflows[workflow_id]["completed"] = True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 