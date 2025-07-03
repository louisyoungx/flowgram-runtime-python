"""
Mock LLM implementation for testing.
"""
from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

class MockChatOpenAI:
    """
    Mock implementation of ChatOpenAI for testing.
    """
    
    def __init__(self, model_name: str, temperature: float, api_key: str, openai_api_base: str):
        """
        Initialize a new instance of the MockChatOpenAI class.
        
        Args:
            model_name: The name of the model to use.
            temperature: The temperature parameter for the LLM.
            api_key: The API key for the LLM service.
            openai_api_base: The host URL for the LLM service.
        """
        self.model_name = model_name
        # Handle temperature if it's a dict with temperature key
        if isinstance(temperature, dict) and 'temperature' in temperature:
            self.temperature = temperature['temperature']
        else:
            self.temperature = temperature
        self.api_key = api_key
        self.openai_api_base = openai_api_base
    
    async def ainvoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """
        Invoke the LLM with the given messages and return a response.
        
        Args:
            messages: The messages to send to the LLM.
            
        Returns:
            The response from the LLM.
        """
        system_prompt = "You are a helpful AI assistant."
        prompt = ""
        
        for message in messages:
            if message.type == "system":
                system_prompt = message.content
            elif message.type == "human":
                prompt = message.content
        
        # Create a mock response that matches the expected format in the tests
        # Format temperature as a simple float, not as a dictionary representation
        temperature_str = str(self.temperature)
        response = f"Hi, I'm an AI assistant, my name is {self.model_name}, temperature is {temperature_str}, system prompt is \"{system_prompt}\", prompt is \"{prompt}\""
        
        # Create a mock message with the response
        return MockAIMessage(content=response)


class MockAIMessage(BaseMessage):
    """
    Mock implementation of an AI message.
    """
    
    type: str = "ai"
    
    def __init__(self, content: str):
        """
        Initialize a new instance of the MockAIMessage class.
        
        Args:
            content: The content of the message.
        """
        super().__init__(content=content)
