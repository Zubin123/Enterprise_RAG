from fastapi import FastAPI
from app.core.logger import logger
from pydantic import BaseModel
from app.retrieval.retriever import Retriever
from app.generation.context_builder import build_context
from app.generation.llm import LLMGenerator


app = FastAPI(title="Enterprise RAG",description= "Research-grade SEC Filing Intelligence Engine",version="1.0.0")

retriever = Retriever()
generator = LLMGenerator()

#Request Schema
class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Response Schema
# -----------------------------
class AnswerResponse(BaseModel):
    question: str
    answer: str


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    logger.info(f"Received query: {request.question}")

    # Step 1: Retrieve documents (auto company, year, section)
    docs = retriever.retrieve(
        query=request.question,
        k=5,
    )

    # Step 2: Build context
    context = build_context(docs)

    # Step 3: Generate answer
    answer = generator.generate(
        context=context,
        question=request.question
    )

    return AnswerResponse(
        question=request.question,
        answer=answer
    ) 