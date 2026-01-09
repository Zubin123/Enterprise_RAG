from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logger import logger
from app.generation.prompt import SYSTEM_PROMPT, USER_PROMPT

class LLMGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model= "gpt-4o-mini",
            temperature= 0,
            api_key= settings.OPENAI_API_KEY,
        )

    def generate(self,context: str, question: str) -> str:
        logger.info("Sending prompt to llm")

        prompt = USER_PROMPT.format(
            context = context,
            question = question,
        )

        response = self.llm.invoke(
            [
                {"role": "system","content":SYSTEM_PROMPT},
                {"role": "user","content":prompt},
            ]
        )

        logger.info("LLM response generated")
        return response.content