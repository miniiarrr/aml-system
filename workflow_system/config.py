from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Define the root directory (path to workflow-system folder)
ROOT_DIR = Path(__file__).parent

class Configs(BaseSettings):
    # AI Agent System settings
    AI_AGENT_HOST: str = "localhost"
    AI_AGENT_PORT: int = 8001
    
    # Frontend settings
    FRONTEND_HOST: str = "localhost"
    FRONTEND_PORT: int = 3000
    
    # Workflow System settings
    WORKFLOW_HOST: str = "localhost"
    WORKFLOW_PORT: int = 8000
    
    # Optional settings that can be overridden by environment variables
    LOG_LEVEL: str = "INFO"
    MAX_WORKFLOW_DURATION: int = 3600  # 1 hour in seconds
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def ai_agent_url(self) -> str:
        """Get the full URL for the AI agent system."""
        return f"http://{self.AI_AGENT_HOST}:{self.AI_AGENT_PORT}"
    
    @property
    def frontend_url(self) -> str:
        """Get the full URL for the frontend."""
        return f"http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}"

# Create a global instance of the Configs class
CONFIGS = Configs() 