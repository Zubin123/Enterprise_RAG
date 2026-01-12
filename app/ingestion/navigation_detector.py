import re
from app.core.logger import logger

TOC_PATTERN = re.compile(r"(table of contents|index)", re.IGNORECASE)
ITEM_LINE_PATTERN = re.compile(r"^\s*Item\s+\d+[A-Z]?", re.IGNORECASE)
PART_LINE_PATTERN = re.compile(r"^\s*Part\s+[IVX]+", re.IGNORECASE)


def is_navigation_page(text: str) -> bool:
    """
    Reliable SEC navigation / TOC page detection.
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Must contain TOC or INDEX
    if not TOC_PATTERN.search(text):
        return False

    # Must contain many Part/Item references
    part_lines = [l for l in lines if PART_LINE_PATTERN.match(l)]
    item_lines = [l for l in lines if ITEM_LINE_PATTERN.match(l)]

    if len(part_lines) >= 2 and len(item_lines) >= 5:
        return True

    return False


def assign_navigation_flag(documents):
    logger.info("Detecting navigation pages")

    nav_count = 0

    for doc in documents:
        nav = is_navigation_page(doc.page_content)
        doc.metadata["is_navigation"] = nav

        if nav:
            nav_count += 1

    logger.info(f"Navigation pages detected: {nav_count}")
    return documents
