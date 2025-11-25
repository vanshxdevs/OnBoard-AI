"""
Settings and environment configuration management.
Handles API keys and application configuration.
"""
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings and API keys."""
    
    groq_api_key: Optional[str] = None
    langchain_api_key: Optional[str] = None
    model_name: str = "llama-3.1-8b-instant"
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000  # Reduced for faster processing
    chunk_overlap: int = 100  # Reduced proportionally
    temperature: float = 0.3  # Lower = faster, more focused responses
    pdf_path: str = "src/data/umbrella_corp_policies.pdf"
    vectorstore_path: str = "src/data/vectorstore"
    
    def __post_init__(self):
        """Do NOT load from environment variables - user must enter keys in UI."""
        pass
    
    def is_configured(self) -> bool:
        """Check if all required API keys are configured."""
        return bool(self.groq_api_key and self.langchain_api_key)
    
    def set_api_keys(self, groq_key: str, langchain_key: str):
        """Set API keys and update environment variables."""
        self.groq_api_key = groq_key
        self.langchain_api_key = langchain_key
        os.environ["GROQ_API_KEY"] = groq_key
        os.environ["LANGCHAIN_API_KEY"] = langchain_key


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
