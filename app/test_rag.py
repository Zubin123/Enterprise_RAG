from app.retrieval.retriever import Retriever
from app.generation.context_builder import build_context
from app.generation.llm import LLMGenerator
from app.core.logger import logger


def test():
    # ✅ Create instances (IMPORTANT)
    retriever = Retriever()
    llm = LLMGenerator()

    question = "What risks does apple mention?"

    # ✅ Call retrieve() on the INSTANCE
    docs = retriever.retrieve(
        query=question,
        k=5,
    )

    context = build_context(docs)

    answer = llm.generate(
        context=context,
        question=question,
    )

    logger.info(f"FINAL ANSWER: {answer}")


if __name__ == "__main__":
    test()
