import re
from collections import Counter
from app.retrieval.vector_store import load_vector_store
from app.core.logger import logger


ITEM_QUERY_PATTERN = re.compile(r"item\s+(\d+[a-z]?)", re.IGNORECASE)
PART_QUERY_PATTERN = re.compile(r"part\s+([ivx]+)", re.IGNORECASE)
COMPANY_PATTERN = re.compile(r"\b(msft|aapl|apple|microsoft)\b", re.IGNORECASE)


class Retriever:
    def __init__(self):
        self.vectorstore = load_vector_store()

    def retrieve(self, query: str, k: int = 5):
        """
        SEC-grade retrieval engine with:
        - Explicit section routing
        - Auto company detection
        - Auto year detection
        - Section locking
        - Semantic fallback
        """

        logger.info(f"Retrieval query: {query}")

        # ---------------------------------------------------
        # Phase 1 — Parse user intent
        # ---------------------------------------------------
        item = None
        part = None
        company = None

        item_match = ITEM_QUERY_PATTERN.search(query)
        if item_match:
            item = f"Item {item_match.group(1).upper()}"
            logger.info(f"Detected explicit section: {item}")

        part_match = PART_QUERY_PATTERN.search(query)
        if part_match:
            part = f"Part {part_match.group(1).upper()}"
            logger.info(f"Detected explicit part: {part}")

        company_match = COMPANY_PATTERN.search(query)
        if company_match:
            name = company_match.group(1).lower()
            if name in ["msft", "microsoft"]:
                company = "MSFT"
            elif name in ["aapl", "apple"]:
                company = "AAPL"

            logger.info(f"Detected company from query: {company}")

        # ---------------------------------------------------
        # Phase 2 — Semantic bootstrap
        # ---------------------------------------------------
        semantic_hits = self.vectorstore.similarity_search(query, k=80)
        logger.info(f"Initial semantic hits: {len(semantic_hits)}")

        if not semantic_hits:
            return []

        # ---------------------------------------------------
        # Phase 3 — Auto year detection
        # ---------------------------------------------------
        year_counts = Counter(
            doc.metadata.get("year") for doc in semantic_hits if doc.metadata.get("year")
        )
        year = max(year_counts) if year_counts else None
        if year:
            logger.info(f"Auto-detected year: {year}")

        # ---------------------------------------------------
        # Phase 4 — Hard section filter (if user requested)
        # ---------------------------------------------------
        if item:
            logger.info(f"Section lock enabled for {item}")

            section_docs = []

            for doc in semantic_hits:
                meta = doc.metadata

                if company and meta.get("company") != company:
                    continue
                if year and meta.get("year") != year:
                    continue
                if part and meta.get("part") != part:
                    continue
                if not meta.get("item", "").upper().startswith(item.upper()):
                    continue
                if meta.get("is_navigation") is True:
                    continue

                section_docs.append(doc)

            logger.info(f"Section-locked docs: {len(section_docs)}")

            # Expand full section if needed
            if len(section_docs) < k:
                logger.info("Expanding full section corpus")

                candidates = self.vectorstore.similarity_search(item, k=200)

                for doc in candidates:
                    meta = doc.metadata

                    if company and meta.get("company") != company:
                        continue
                    if year and meta.get("year") != year:
                        continue
                    if part and meta.get("part") != part:
                        continue
                    if not meta.get("item", "").upper().startswith(item.upper()):
                        continue
                    if meta.get("is_navigation") is True:
                        continue

                    section_docs.append(doc)

            return section_docs[:k]

        # ---------------------------------------------------
        # Phase 5 — General semantic mode
        # ---------------------------------------------------
        logger.info("Using general semantic retrieval")

        filtered = []

        for doc in semantic_hits:
            meta = doc.metadata

            if company and meta.get("company") != company:
                continue
            if year and meta.get("year") != year:
                continue
            if meta.get("is_navigation") is True:
                continue

            filtered.append(doc)

        return filtered[:k]
