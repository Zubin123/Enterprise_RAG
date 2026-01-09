from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.logger import logger
from app.core.config import settings
from pathlib import Path

def build_vector_store(chunks):
    """
    Embed chunks and store them in FAISS
    """
    logger.info("Initializing embedding model")

    embeddings = HuggingFaceEmbeddings(
        model_name = settings.EMBEDDING_MODEL
    )

    logger.info("Creating FAISS vector store")
    vector_store = FAISS.from_documents(chunks,embeddings)

    vector_path = Path(settings.VECTOR_DB_PATH)
    vector_path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(vector_path))

    logger.info(f"vector store created and saved at {vector_path}"
                f"with {len(chunks)} embeddings")
    
    return vector_store

def load_vector_store():
    """
    Load existing FAISS vector_store from disk
    """
    logger.info("Loading FAISS vector store from disk")

    embeddings = HuggingFaceEmbeddings(
        model_name = settings.EMBEDDING_MODEL
    )

    vectorstore = FAISS.load_local(
        settings.VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    logger.info("Vector store loaded successfully")
    return vectorstore