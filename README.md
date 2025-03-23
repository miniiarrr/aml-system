# AML System

A comprehensive system that combines Next.js UI, Python workflow system, and AI agent system for automated task processing.

## Project Structure

- `frontend/` - Next.js UI application
- `workflow_system/` - Python workflow management system
- `ai_agents/` - Python AI agent system
- `shared/` - Shared types and utilities

## Setup Instructions

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### Workflow System
```bash
cd workflow_system
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### AI Agent System
```bash
cd ai_agents
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Architecture

The system consists of three main components:

1. **Frontend (Next.js)**
   - User interface for initiating workflows
   - Real-time updates via Server-Sent Events (SSE)
   - Workflow status monitoring

2. **Workflow System**
   - Manages workflow execution
   - Coordinates between UI and AI agents
   - Handles SSE updates to the frontend

3. **AI Agent System**
   - Contains multiple AI agents that collaborate
   - Processes tasks and updates workflow status
   - Communicates results back to the workflow system

## Communication Flow

1. UI initiates workflow → Workflow System
2. Workflow System creates workflow ID → UI
3. Workflow System coordinates with AI Agents
4. AI Agents process tasks and update Workflow System
5. Workflow System sends updates to UI via SSE 

Participant wallet: 0x9CeaC40E54573409F346257Ba941Fae408513028
