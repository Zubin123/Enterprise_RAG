from fastapi import FastAPI
from app.core.logger import logger

app = FastAPI(title="Enterprise RAG")

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status":"ok"}


