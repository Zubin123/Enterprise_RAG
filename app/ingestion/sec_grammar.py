import re
from app.core.logger import logger

# Strict PART header: full line only
PART_PATTERN = re.compile(r"^\s*PART\s+(I|II|III|IV)\s*$", re.IGNORECASE)

# Strict ITEM header with title (no bare "ITEM 1")
ITEM_PATTERN = re.compile(
    r"^\s*ITEM\s+(\d+[A-Z]?)\.\s+(.+)$",
    re.IGNORECASE
)

def normalize(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def assign_sec_structure(documents):
    """
    Robust SEC section parser.
    Handles:
    - Apple-style single headers
    - Microsoft-style repeating headers
    - Page running headers
    - Footer noise
    """

    logger.info("Assigning SEC Part & Item structure")

    current_part = "Unknown"
    current_item = "Unknown"
    current_title = ""

    last_detected_item = None
    last_detected_page = None

    for doc in documents:
        text = doc.page_content
        page_num = doc.metadata.get("page")

        lines = [normalize(l) for l in text.split("\n") if l.strip()]

        # Only scan top portion of page (real headers appear there)
        scan_lines = lines[:12]

        for line in scan_lines:

            # ---------------------
            # Detect PART header
            # ---------------------
            part_match = PART_PATTERN.fullmatch(line)
            if part_match:
                roman = part_match.group(1).upper()
                new_part = f"Part {roman}"

                if new_part != current_part:
                    current_part = new_part
                    logger.debug(f"Detected {current_part}")
                continue

            # ---------------------
            # Detect ITEM header
            # ---------------------
            item_match = ITEM_PATTERN.fullmatch(line)
            if item_match:
                item_number = item_match.group(1)
                item_title = item_match.group(2).strip()

                new_item = f"Item {item_number}"

                # Ignore running headers (same item on next page)
                if new_item == last_detected_item and page_num == last_detected_page + 1:
                    continue

                # Prevent overwrite with same item
                if new_item != current_item:
                    current_item = new_item
                    current_title = item_title
                    last_detected_item = new_item
                    last_detected_page = page_num

                    logger.debug(f"Detected {current_item}: {current_title}")
                continue

        # Attach structure metadata to this page
        doc.metadata["part"] = current_part
        doc.metadata["item"] = current_item
        doc.metadata["title"] = current_title
        doc.metadata["section"] = f"{current_part} - {current_item}: {current_title}"

    logger.info("SEC grammar assignment complete")
    return documents
