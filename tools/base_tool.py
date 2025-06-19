from abc import ABC, abstractmethod

class BaseTool(ABC):
    
    @abstractmethod
    def name(self) -> str:
        """name of the tool"""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Description of the tool(important because it's how the llm will understand that it should use this tool)"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the tool with the given parameters"""
        pass
