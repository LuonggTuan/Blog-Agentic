from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.state.blogstate import BlogState

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Builds a graph for topic selection.
        """
        # Add nodes 
        self.graph.add_node("title_creation","")
        self.graph.add_node("content_generation","")

        # Add edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph