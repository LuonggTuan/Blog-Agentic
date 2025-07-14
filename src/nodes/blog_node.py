from src.state.blogstate import BlogState
from langchain_core.messages import SystemMessage,HumanMessage
from src.state.blogstate import Blog

class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        Generates a title for the blog post based on the topic.
        """
        if "topic" in state and state["topic"]:
            prompt = """You are expoert blog content writer. 
                    Use Markdown formatting. Generate a blog title for the {topic}. 
                    This title should be creative and SEO friendly."""
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}
    
    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting. 
            Generate a blog content for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self, state: BlogState):
        """
        Translates the blog content to the specified language.
        """
        translation_prompt="""
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}

        """
        print(state["current_language"])
        blog_content = state["blog"]["content"]
        message = [
            HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_content=blog_content))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(message)
        return {"blog": {"content": translation_content}}

    def route(self, state: BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state: BlogState):
        """
        Determines the next step based on the current language.
        """
        if state["current_language"] == "french":
            return "french"
        elif state["current_language"] == "hindi":
            return "hindi"
        else:
            return state["current_language"]