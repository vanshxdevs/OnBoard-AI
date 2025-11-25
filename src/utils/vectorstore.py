"""
Vector store utilities for managing document embeddings.
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from src.utils.logger import logger


def load_pdf(pdf_path: str) -> list:
    """Load PDF documents.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of loaded documents
    """
    logger.info(f"Loading PDF from {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    logger.info(f"Loaded {len(docs)} pages from PDF")
    return docs


def split_documents(docs: list, chunk_size: int = 2000, chunk_overlap: int = 200) -> list:
    """Split documents into chunks.
    
    Args:
        docs: List of documents
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(docs)
    logger.info(f"Split into {len(splits)} chunks")
    return splits


def create_vectorstore(documents: list, embedding_function) -> FAISS:
    """Create FAISS vector store from documents.
    
    Args:
        documents: List of document chunks
        embedding_function: Embedding function instance to use
        
    Returns:
        FAISS vector store
    """
    vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_function)
    logger.info("Created FAISS vector store")
    return vectorstore
