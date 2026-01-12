from app.core.logger import logger


def build_context(docs):
    """
    Convert retrieved documents into a clean context block with citations.
    """
    logger.info(f"Building context from {len(docs)} documents")

    context_blocks = []

    for i, doc in enumerate(docs, 1):
        meta = doc.metadata

        citation = (
            f"[Source: {meta.get('company')} 10-K {meta.get('year')}, "
            f"{meta.get('item')}, Page {meta.get('page')}]"
        )

        block = (
            f"[Document {i}]\n"
            f"{doc.page_content}\n\n"
            f"{citation}"
        )

        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    logger.debug(
        {
            "context_length": len(context),
            "context_preview": context[:500],
        }
    )

    return context
