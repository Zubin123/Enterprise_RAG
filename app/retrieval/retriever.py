from app.retrieval.vector_store import load_vector_store
from app.core.logger import logger

class Retriever:
    def __init__(self):
        self.vectorstore = load_vector_store()

    def retrieve(
        self,
        query: str,
        company: str | None = None,
        year: int | None = None,
        k: int = 5,
    ):
        
        """
        Retrieve documents with optional metadata filtering.
        """
        logger.info(f"Retrival query: {query}")

        docs = self.vectorstore.similarity_search(query,k=k)

        logger.info(f"Initial retrieved docs: {len(docs)}")

        # ---- Metadata filtering ----
        if company or year:
            filtered =[]
            for doc in docs:
                meta = doc.metadata
                if company and meta.get("company")!= company:
                    continue
                if year and meta.get("year") != year:
                    continue
                filtered.append(doc)

            logger.info(f"Docs after filtering(company={company}, year={year}):{len(filtered)}")

            docs =filtered

            # ---- Log what we actually return ----
        for i, doc in enumerate(docs, 1):
            logger.debug(
                {
                    "rank": i,
                    "company": doc.metadata.get("company"),
                    "year": doc.metadata.get("year"),
                    "page": doc.metadata.get("page"),
                    "preview": doc.page_content[:200],
                }
            )

        return docs
