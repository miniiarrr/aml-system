from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# In-memory storage for agent states
agent_states: Dict[str, Dict] = {}

class AgentRequest(BaseModel):
    workflow_id: str
    task: Optional[str] = None

class AgentState(BaseModel):
    status: str
    message: str
    completed: bool
    current_agent: Optional[str] = None
    messages: List[Dict] = []

# Define tools for the agents
def search_tool(query: str) -> str:
    """Search for information about a topic."""
    return f"Searching for information about: {query}"

def analyze_tool(data: str) -> str:
    """Analyze the provided data."""
    return f"Analyzing data: {data}"

def summarize_tool(text: str) -> str:
    """Summarize the provided text."""
    return f"Summarizing text: {text}"

# Create tools
tools = [
    Tool(
        name="search",
        func=search_tool,
        description="Useful for searching for information about a topic"
    ),
    Tool(
        name="analyze",
        func=analyze_tool,
        description="Useful for analyzing data"
    ),
    Tool(
        name="summarize",
        func=summarize_tool,
        description="Useful for summarizing text"
    )
]

# Create the agent prompt
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI agent that collaborates with other agents to complete tasks."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessage(content="{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

@app.post("/agent/start")
async def start_agent(request: AgentRequest):
    workflow_id = request.workflow_id
    agent_states[workflow_id] = {
        "status": "initialized",
        "message": "Agent system initialized",
        "completed": False,
        "current_agent": "main",
        "messages": []
    }
    
    # Start the agent process
    asyncio.create_task(process_agent_task(workflow_id))
    
    return {"status": "success", "message": "Agent process started"}

@app.get("/agent/{workflow_id}/status")
async def get_agent_status(workflow_id: str):
    if workflow_id not in agent_states:
        raise HTTPException(status_code=404, detail="Agent state not found")
    
    return agent_states[workflow_id]

async def process_agent_task(workflow_id: str):
    try:
        state = agent_states[workflow_id]
        state["status"] = "processing"
        state["message"] = "Starting agent task processing"
        
        # Example task processing
        result = agent_executor.invoke({
            "input": "Analyze and summarize the following text: The quick brown fox jumps over the lazy dog."
        })
        
        state["messages"].append({
            "role": "agent",
            "content": result["output"]
        })
        
        # Simulate multiple agent interactions
        for i in range(3):
            await asyncio.sleep(1)
            state["message"] = f"Agent processing step {i + 1}"
            state["messages"].append({
                "role": "system",
                "content": f"Completed step {i + 1}"
            })
        
        state["status"] = "completed"
        state["message"] = "Agent task completed successfully"
        state["completed"] = True
        
    except Exception as e:
        state["status"] = "error"
        state["message"] = f"Error in agent processing: {str(e)}"
        state["completed"] = True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 