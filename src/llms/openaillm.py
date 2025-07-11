from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

class OpenAILLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        try:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key = os.getenv("OPENAI_API_KEY")
            llm = ChatOpenAI(
                api_key=self.openai_api_key,
                model="gpt-4o-mini",
            )
            return llm
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAILLM: {e}")