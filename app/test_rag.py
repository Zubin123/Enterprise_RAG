from app.retrieval.retriever import Retriever
from app.generation.context_builder import build_context
from app.generation.llm import LLMGenerator
from app.core.logger import logger


def test():
    # ✅ Create instances (IMPORTANT)
    retriever = Retriever()
    llm = LLMGenerator()

    question = "What are the main risk factors mentioned by Apple in 2023?"

    # ✅ Call retrieve() on the INSTANCE
    docs = retriever.retrieve(
        query=question,
        company="AAPL",
        year=2023,
        k=5,
    )

    context = build_context(docs)

    answer = llm.generate(
        context=context,
        question=question,
    )

    logger.info("FINAL ANSWER:")
    logger.info(answer)


if __name__ == "__main__":
    test()
