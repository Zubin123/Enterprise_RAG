from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_DB_PATH: str = "data/vectorstore"

settings = Settings()