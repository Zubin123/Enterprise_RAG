from pathlib import Path
from app.ingestion.sec_loader import load_sec_filing
from app.core.logger import logger
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import build_vector_store

DATA_DIR = Path("data/raw")

def run():
    all_docs = []

    all_docs.extend(
        load_sec_filing(
            DATA_DIR / "AAPL_2023_10K.pdf",
            company = "AAPL",
            year = 2023,
        )
    )

    all_docs.extend(
        load_sec_filing(
            DATA_DIR / "MSFT_2023_10K.pdf",
            company = "MSFT",
            year = 2023,
        )
    )

    logger.info(f"Total documents loaded: {len(all_docs)}")

    chunks = chunk_documents(all_docs)
    logger.info(f"Total chunks created: {len(chunks)}")

    build_vector_store(chunks)

if __name__ == "__main__":
    run()
    

 