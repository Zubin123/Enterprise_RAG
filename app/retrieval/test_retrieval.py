from app.retrieval.vector_store import load_vector_store
from app.core.logger import logger

def test():
    vector_store = load_vector_store()

    query = "what are the main risk factors mentioned by apple?"
    docs = vector_store.similarity_search(query,k=3)

    logger.info("Retrieved documents:")
    for i,doc in enumerate(docs,1):
        logger.info(f"---Result{i}---")
        logger.info(doc.metadata)
        logger.info(doc.page_content[:300])

if __name__ == "__main__":
    test()