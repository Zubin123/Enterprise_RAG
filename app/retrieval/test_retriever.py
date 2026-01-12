from app.retrieval.retriever import Retriever
from app.core.logger import logger

def test():
    retriever = Retriever()

    query = "What are the main risk factors for the company?"

    docs = retriever.retrieve(
        query=query,
        company="AAPL",
        year=2023,
        part=None,
        item=None,
        k=5,
    )
    logger.info(f"Final documents returned:{len(docs)}")

    for doc in docs:
        logger.info(doc.metadata)
        logger.info(doc.page_content[:300])

if __name__ == "__main__":
    test()