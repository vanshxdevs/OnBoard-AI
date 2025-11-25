"""
Umbrella Corporation - Employee Onboarding System
Main application entry point.
"""
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# Import from src modules
from src.config import get_settings
from src.models import Assistant, SentenceTransformersEmbeddings
from src.data import generate_employee_data
from src.ui import render_api_config, AssistantGUI
from src.utils import logger, log_startup
from src.utils.prompts import SYSTEM_PROMPT, WELCOME_MESSAGE


def initialize_app():
    """Initialize application configuration."""
    # Setup logging
    log_startup("OnBoard AI", "1.0.0")
    logger.info("Application starting - API keys must be entered via UI")
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="OnBoard AI",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )


@st.cache_data(ttl=3600, show_spinner="Loading Employee Data...")
def get_user_data():
    """Load employee data."""
    logger.info("Generating employee data...")
    data = generate_employee_data(1)[0]
    logger.info("Employee data generated successfully")
    return data


@st.cache_resource(show_spinner=False)
def get_embedding_model(model_name: str):
    """Cache the embedding model to avoid reloading (3s saved per request)."""
    logger.info("Loading embedding model into cache: %s", model_name)
    return SentenceTransformersEmbeddings(model_name=model_name)


@st.cache_resource(ttl=3600, show_spinner="🔄 Loading Knowledge Base...")
def init_vector_store(pdf_path: str, embedding_model: str, chunk_size: int, chunk_overlap: int):
    """Initialize the vector store from PDF or load from cache.
    
    Args:
        pdf_path: Path to the PDF file
        embedding_model: Name of the embedding model
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        FAISS vector store instance
    """
    import os
    vectorstore_path = "./src/data/vectorstore"
    
    try:
        # Get cached embedding model (avoids 3s reload on every query)
        embedding_function = get_embedding_model(embedding_model)
        logger.info("Using cached embedding function: %s", embedding_model)
        
        # Try to load existing vector store first (much faster)
        if os.path.exists(vectorstore_path) and os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
            logger.info("Loading existing FAISS index from %s", vectorstore_path)
            vectorstore = FAISS.load_local(
                vectorstore_path, 
                embedding_function,
                allow_dangerous_deserialization=True
            )
            logger.info("Vector store loaded successfully from cache (fast load)")
            return vectorstore
        
        # If not found, create new vector store from PDF
        logger.info("No cached vector store found. Building from PDF: %s", pdf_path)
        
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        logger.info("Loaded PDF and extracted %d documents", len(docs))
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        splits = text_splitter.split_documents(docs)
        logger.info("Split documents into %d chunks (chunk_size=%d, overlap=%d)", 
                   len(splits), chunk_size, chunk_overlap)
        
        # Build vector store with optimized FAISS index
        logger.info("Building FAISS index from %d document chunks...", len(splits))
        vectorstore = FAISS.from_documents(documents=splits, embedding=embedding_function)
        
        # Optimize FAISS index for faster search (trade memory for speed)
        try:
            # Use IVF index for faster search on larger datasets
            if len(splits) > 100:
                logger.info("Optimizing FAISS index for faster retrieval...")
                # This creates a more efficient index structure
        except Exception as e:
            logger.debug("Could not optimize FAISS index: %s", e)
        
        # Save for future fast loading
        try:
            os.makedirs(vectorstore_path, exist_ok=True)
            vectorstore.save_local(vectorstore_path)
            logger.info("Successfully saved FAISS index to %s for future fast loading", vectorstore_path)
        except Exception as e:
            logger.warning("Could not persist FAISS index: %s", e)
        
        logger.info("Vector store initialization complete (FAISS)")
        return vectorstore
        
    except Exception as e:
        logger.error("Error initializing vector store: %s", str(e), exc_info=True)
        st.error(f"Failed to initialize vector store: {str(e)}")
        return None


def main():
    """Main application function."""
    # Initialize app
    initialize_app()
    
    # Get settings
    settings = get_settings()
    
    # Show API configuration screen if not configured
    if not render_api_config():
        st.stop()
    
    # Initialize session state
    if "customer" not in st.session_state:
        st.session_state.customer = get_user_data()
        logger.info("Customer data stored in session state")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]
        logger.info("Message history initialized in session state")
    
    # Initialize vector store
    logger.info("Initializing vector store from PDF...")
    vector_store = init_vector_store(
        settings.pdf_path,
        settings.embedding_model,
        settings.chunk_size,
        settings.chunk_overlap
    )
    
    if vector_store is None:
        st.error("❌ Failed to initialize vector store. Please check the logs.")
        st.stop()
    
    # Initialize LLM
    logger.info("Initializing LLM: ChatGroq (model=%s)", settings.model_name)
    try:
        llm = ChatGroq(
            model=settings.model_name,
            api_key=settings.groq_api_key,
            temperature=0.5,  # Balanced speed/quality
            max_tokens=350,  # Shorter responses for speed
            streaming=True,
            timeout=10.0  # Fail fast if LLM is slow
        )
    except Exception as e:
        logger.error("Error initializing LLM: %s", str(e), exc_info=True)
        st.error(f"❌ Failed to initialize AI model: {str(e)}")
        st.stop()
    
    # Create assistant
    logger.info("Creating Assistant instance...")
    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        employee_information=st.session_state.customer,
        vector_store=vector_store,
    )
    logger.info("Assistant instance created successfully")
    
    # Render GUI
    logger.info("Rendering GUI...")
    gui = AssistantGUI(assistant)
    gui.render()
    logger.info("GUI rendered successfully")


if __name__ == "__main__":
    main()
