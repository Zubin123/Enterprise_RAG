from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import logger
from app.ingestion.navigation_detector import assign_navigation_flag
from app.ingestion.sec_grammar import assign_sec_structure


def chunk_documents(documents):
    """
    Convert page-level documents into semantic chunks.

    Args:
        documents: List of documents to be chunked.
    """
    logger.info("Starting document chunking")

    documents = assign_navigation_flag(documents)
    documents = assign_sec_structure(documents)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks = splitter.split_documents(documents)
    # 🔒 Enforce section metadata on every chunk
    for chunk in chunks:
        chunk.metadata["is_navigation"] = chunk.metadata.get("is_navigation", False)
        chunk.metadata["part"] = chunk.metadata.get("part", "Unknown")
        chunk.metadata["item"] = chunk.metadata.get("item", "Unknown")
        chunk.metadata["title"] = chunk.metadata.get("title", "")
        chunk.metadata["section"] = chunk.metadata.get("section", "")

    logger.info(f"Created {len(chunks)} chunks")

    # Log sample chunk for debugging
    sample = chunks[0]
    logger.debug(
        {
            "chunk_length": len(sample.page_content),
            "metadata": sample.metadata,
            "page": sample.metadata.get("page"),
            "is_navigation": sample.metadata.get("is_navigation"),
            "part": sample.metadata.get("part"),
            "item": sample.metadata.get("item"),
            "title": sample.metadata.get("title"),
            "section": sample.metadata.get("section"),
            "preview": sample.page_content[:300],
        }
    )

    return chunks