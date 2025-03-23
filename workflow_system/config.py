from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the root directory (path to workflow-system folder)
ROOT_DIR = Path(__file__).parent

class FrontendConfig(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 3000
    
    @property
    def url(self) -> str:
        """Get the full URL for the frontend."""
        return f"http://{self.HOST}:{self.PORT}"

class WorkflowConfig(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000
    MAX_DURATION: int = 3600  # 1 hour in seconds

class AIAgentConfig(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8001
    
    @property
    def url(self) -> str:
        """Get the full URL for the AI agent system."""
        return f"http://{self.HOST}:{self.PORT}"

class MongoDBConfig(BaseSettings):
    URI: str
    DB_NAME: str
    CONNECTION_TIMEOUT: int = 5000  # ms
    
    @property
    def connection_string(self) -> str:
        """Get the MongoDB connection string."""
        return self.URI

class Configs(BaseSettings):
    # System-wide settings
    LOG_LEVEL: str = "INFO"
    ENV: str = "local"
    
    # Nested configurations
    FRONTEND: FrontendConfig = FrontendConfig()
    WORKFLOW: WorkflowConfig = WorkflowConfig()
    AI_AGENT: AIAgentConfig = AIAgentConfig()
    MONGODB: MongoDBConfig = MongoDBConfig()
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter='__'
    )

# Create a global instance of the Configs class
CONFIGS = Configs() 