from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import logger

def chunk_documents(documents):
    """
    Convert page-level documents into semantic chunks.

    Args:
        documents: List of documents to be chunked.
    """
    logger.info("Starting document chunking")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks = splitter.split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    # Log sample chunk for debugging
    sample = chunks[0]
    logger.debug(
        {
            "chunk_length": len(sample.page_content),
            "metadata": sample.metadata,
            "preview": sample.page_content[:300],
        }
    )

    return chunks