"""
Local embeddings using sentence-transformers.
Provides embeddings without requiring external API calls.
"""
from typing import List
from src.utils.logger import logger

try:
    from langchain_core.embeddings import Embeddings
except ImportError:
    # Fallback base class if langchain_core not available
    class Embeddings:
        def embed_documents(self, texts: List[str]) -> List[List[float]]:
            raise NotImplementedError
        
        def embed_query(self, text: str) -> List[float]:
            raise NotImplementedError


class SentenceTransformersEmbeddings(Embeddings):
    """Lightweight wrapper that provides embeddings using sentence-transformers.
    
    This provides the LangChain Embeddings interface:
    - embed_documents(list[str]) -> list[list[float]]
    - embed_query(str) -> list[float]
    
    Falls back to deterministic dummy embeddings if sentence-transformers is unavailable.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embeddings model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        logger.info("Initializing embeddings model: %s", model_name)
        
        try:
            from sentence_transformers import SentenceTransformer

            logger.info("Loading SentenceTransformer model '%s'...", model_name)
            self.model = SentenceTransformer(model_name)
            
            try:
                self.dim = self.model.get_sentence_embedding_dimension()
            except Exception:
                self.dim = 384
                
            logger.info("Successfully loaded SentenceTransformer model '%s' (dim=%d)", model_name, self.dim)
        except Exception as exc:
            logger.warning(
                "Could not load sentence-transformers (model=%s): %s. Falling back to dummy embeddings.",
                model_name,
                exc,
            )
            self.model = None
            self.dim = 384

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents/texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        logger.info("Embedding %d documents using %s", len(texts), "SentenceTransformer" if self.model else "fallback")
        
        if self.model is not None:
            # Batch processing with optimizations for speed
            vectors = self.model.encode(
                texts, 
                convert_to_numpy=True, 
                show_progress_bar=False,
                batch_size=32,  # Process in batches for efficiency
                normalize_embeddings=True  # Faster cosine similarity
            )
            logger.debug("Embedded %d documents to vectors of dim %d", len(texts), self.dim)
            return vectors.tolist()
        
        # Deterministic fallback using sha256 -> bytes -> float vector
        logger.debug("Using deterministic hash-based fallback embeddings")
        import hashlib

        result = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            nums = [b / 255.0 for b in h]
            
            # Expand to desired dimension
            if len(nums) < self.dim:
                times = (self.dim + len(nums) - 1) // len(nums)
                nums = (nums * times)[: self.dim]
            else:
                nums = nums[: self.dim]
            result.append(nums)
            
        logger.debug("Fallback embeddings generated for %d documents", len(result))
        return result

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        logger.info("Embedding single query text (length=%d chars)", len(text))
        return self.embed_documents([text])[0]
