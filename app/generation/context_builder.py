from app.core.logger import logger

def build_context(docs):
    """
    Convert retrieved documents into a clean context block.
    """
    logger.info(f"Building context from {len(docs)} documents")

    context_blocks = []

    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        block = (
            f"[Document {i}] "
            f"(Company: {meta.get('company')}, "
            f"Year: {meta.get('year')}, "
            f"Page: {meta.get('page')})\n"
            f"{doc.page_content}"
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