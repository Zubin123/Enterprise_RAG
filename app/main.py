from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.retrieval.retriever import Retriever
from app.generation.llm import LLMGenerator
from app.generation.context_builder import build_context
import uvicorn
import os

app = FastAPI()
retriever = Retriever()
llm = LLMGenerator()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    docs = retriever.retrieve(query=question, k=5)
    context = build_context(docs)
    answer = llm.generate(context, question)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": question,
            "answer": answer,
        },
    )
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
