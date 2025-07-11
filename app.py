import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

class BlogRequest(BaseModel):
    topic: str

# API
@app.post("/blogs")
async def create_blog(request: BlogRequest):
    topic = request.topic

    # get the llm object

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    # get the graph
    graph_builder = GraphBuilder(llm)
    if topic:
        graph = graph_builder.setup_graph(uscase="topic")
        state = graph.invoke({"topic": topic})

    return {"data":state}

if __name__=="__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)