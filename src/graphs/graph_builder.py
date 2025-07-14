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
    
    def build_language_graph(self):
        """
        Builds a graph to generate blog based on language.
        """
        # Nodes
        self.blog_node_obj = BlogNode(self.llm)

        # Add nodes 
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_node("french_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "french"}))
        self.graph.add_node("hindi_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}))
        self.graph.add_node("route", self.blog_node_obj.route)

        # Add edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        # Conditional edges
        self.graph.add_conditional_edges(
            "route", 
            self.blog_node_obj.route_decision,
            {
                "french": "french_translation",
                "hindi": "hindi_translation"
            }
        )
        self.graph.add_edge("french_translation", END)
        self.graph.add_edge("hindi_translation", END)

        return self.graph
    
    def setup_graph(self, uscase):
        if uscase == "topic":
            self.build_topic_graph()
        elif uscase == "language":
            self.build_language_graph()
        return self.graph.compile()
    
## Bellow code is for the langsmith studio
llm = GroqLLM().get_llm()

## Get the graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile() #simple graph for language
#graph = graph_builder.build_topic_graph().compile() #simple graph for topic
