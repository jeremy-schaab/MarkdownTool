"""
Configuration settings for Markdown Manager.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for the application."""
    
    # Application settings
    APP_NAME = "Markdown Manager"
    VERSION = "1.2.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server settings
    DEFAULT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    HOST = os.getenv("STREAMLIT_HOST", "localhost")
    
    # File settings
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    SUPPORTED_EXTENSIONS = [".md", ".markdown", ".txt"]
    
    # Azure OpenAI settings
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4")
    AZURE_OPENAI_MAX_TOKENS = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "128000"))
    AZURE_OPENAI_TEMPERATURE = float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.25"))
    AZURE_OPENAI_REQUEST_TIMEOUT = int(os.getenv("AZURE_OPENAI_REQUEST_TIMEOUT", "180"))
    
    # Azure Storage settings
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    SESSIONS_DIR = PROJECT_ROOT / "sessions"
    
    @classmethod
    def is_ai_enabled(cls) -> bool:
        """Check if AI features are properly configured."""
        return bool(
            cls.AZURE_OPENAI_ENDPOINT and 
            cls.AZURE_OPENAI_API_KEY and 
            cls.AZURE_OPENAI_CHAT_DEPLOYMENT
        )
    
    @classmethod
    def is_azure_storage_enabled(cls) -> bool:
        """Check if Azure storage is properly configured."""
        return bool(cls.AZURE_STORAGE_CONNECTION_STRING)
    
    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories."""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.SESSIONS_DIR.mkdir(exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    # Override with test values
    AZURE_OPENAI_ENDPOINT = "https://test.openai.azure.com/"
    AZURE_OPENAI_API_KEY = "test-key"


# Configuration mapping
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}


def get_config(env: Optional[str] = None) -> Config:
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv("ENVIRONMENT", "development")
    
    return config_map.get(env, DevelopmentConfig)