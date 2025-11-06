"""Basic setup and environment tests."""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

def test_environment():
    """Test that environment variables are loaded."""
    load_dotenv()
    assert os.getenv('OPENAI_API_KEY'), "OpenAI API key not found in .env"
    assert os.getenv('TAVILY_API_KEY'), "Tavily API key not found in .env"
    print("✓ Environment variables loaded successfully")

def test_imports():
    """Test that all required packages are installed."""
    try:
        import langchain
        import langgraph
        import streamlit
        import chromadb
        import tavily
        from langchain_openai import ChatOpenAI
        from pydantic_settings import BaseSettings
        print("✓ All required packages imported successfully")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        raise

def test_config():
    """Test configuration loading."""
    from src.utils.config import settings
    assert settings.llm_model == 'gpt-4o-mini'
    assert settings.openai_api_key
    assert settings.tavily_api_key
    print("✓ Configuration loaded successfully")

def test_openai_connection():
    """Test OpenAI API connection."""
    from langchain_openai import ChatOpenAI
    load_dotenv()
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke("Say 'Connection successful!'")
    assert "successful" in response.content.lower()
    print("✓ OpenAI API connection successful")

if __name__ == "__main__":
    print("\n🧪 Running setup tests...\n")
    test_environment()
    test_imports()
    test_config()
    test_openai_connection()
    print("\n✅ All tests passed! Ready for weekend coding.\n")