from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from app.core.logger import logger 

def load_sec_filing(
    file_path: Path,
    company: str,
    year: int,
    form: str = "10-K",):
    """
    Load SEC filing from a PDF file and attach metadata.

    Args:
        file_path: Path to the PDF file.
        company: Name of the company.
        year: Year of the filing.
        form: Type of SEC filing (default is "10-K").
    """
    logger.info(f"Loading SEC filing: {company} {year} {form}")

    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    for doc in documents:
        doc.metadata.update(
            {
                "company": company,
                "year": year,
                "form": form,
                "source": "sec-edgar",
            }
        )
    logger.info(f"Loaded {len(documents)} pages from {file_path.name}")
    return documents