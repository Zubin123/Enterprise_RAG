import os
from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from app.core.logger import logger
from app.core.config import settings

INGEST_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -------------------------------------------------------------------
# INGESTION (LOCAL MACHINE ONLY)
# -------------------------------------------------------------------

def build_vector_store(
    chunks: List,
    vector_path: Optional[str] = None,
):
    """
    Build FAISS vector store using SentenceTransformers.
    This function MUST NOT be used inside Docker.

    Args:
        chunks: List of LangChain Document objects
        vector_path: Optional custom path

    Returns:
        FAISS vector store
    """
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as e:
        raise ImportError(
            "HuggingFaceEmbeddings not installed. "
            "Install ingestion dependencies locally."
        ) from e

    logger.info("Initializing ingestion embedding model")

    embeddings = HuggingFaceEmbeddings(
        model_name=INGEST_EMBEDDING_MODEL
    )

    logger.info("Creating FAISS vector store")
    vector_store = FAISS.from_documents(chunks, embeddings)

    path = Path(vector_path or settings.VECTOR_DB_PATH)
    path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(path))

    logger.info(
        f"Vector store created at {path} "
        f"with {len(chunks)} embeddings"
    )

    return vector_store


def load_vector_store(
    vector_path: Optional[str] = None,
):
    """
    Load FAISS vector store for query-time retrieval.
    Uses HuggingFace Inference API embeddings (NO torch).
    """
    try:
        from langchain_huggingface import HuggingFaceEndpointEmbeddings
    except ImportError as e:
        raise ImportError(
            "langchain-huggingface not installed. "
            "Install production requirements."
        ) from e

    if not settings.HF_TOKEN:
        raise EnvironmentError(
            "HF_TOKEN not set. Please set HuggingFace API token."
        )

    # 🔑 HF client reads THIS env var internally
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HF_TOKEN

    logger.info("Loading FAISS vector store using HuggingFace Inference API")

    embeddings = HuggingFaceEndpointEmbeddings(
        model=INGEST_EMBEDDING_MODEL
    )

    path = Path(vector_path or settings.VECTOR_DB_PATH)

    if not path.exists():
        raise FileNotFoundError(
            f"Vector store not found at {path}. "
            "Run ingestion first."
        )

    vector_store = FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    logger.info("Vector store loaded successfully")

    return vector_store

