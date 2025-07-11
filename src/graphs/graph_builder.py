from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.state.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Builds a graph to generate base on topic.
        """

        self.blog_node_obj = BlogNode(self.llm)

        # Add nodes 
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)

        # Add edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph

    def setup_graph(self, uscase):
        if uscase == "topic":
            self.build_topic_graph()
        return self.graph.compile()