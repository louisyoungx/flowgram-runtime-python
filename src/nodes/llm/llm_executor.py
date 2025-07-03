"""
LLM Node Executor for the workflow runtime.
This module provides the executor for LLM (Language Learning Model) nodes.
"""
from typing import Any, Dict, List, Optional, TypedDict, Union
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from ...interface.executor import INodeExecutor, ExecutionContext, ExecutionResult
from ...interface.node import FlowGramNode

# Import the mock LLM implementation for testing
from .mock_llm import MockChatOpenAI
# Import our real LLM client implementation
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class LLMExecutorInputs(TypedDict, total=False):
    """
    Inputs for the LLM executor.
    
    Attributes:
        modelName: The name of the model to use.
        apiKey: The API key for the LLM service.
        apiHost: The host URL for the LLM service.
        temperature: The temperature parameter for the LLM.
        systemPrompt: Optional system prompt to set context.
        prompt: The prompt to send to the LLM.
    """
    modelName: str
    apiKey: str
    apiHost: str
    temperature: float
    systemPrompt: Optional[str]
    prompt: str


class LLMExecutor(INodeExecutor):
    """
    Executor for LLM nodes.
    
    This executor handles the execution of LLM nodes in a workflow.
    It uses LangChain's ChatOpenAI to interact with language models.
    """
    
    @property
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        return FlowGramNode.LLM
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute an LLM node with the given context and return the result.
        
        Args:
            context: The execution context containing the node, inputs, runtime, and container.
            
        Returns:
            The execution result containing the LLM response.
        """
        inputs = context.inputs  # type: LLMExecutorInputs
        self._check_inputs(inputs)
        
        model_name = inputs["modelName"]
        temperature = inputs["temperature"]
        api_key = inputs["apiKey"]
        api_host = inputs["apiHost"]
        system_prompt = inputs.get("systemPrompt")
        prompt = inputs["prompt"]
        
        # Use mock implementation for testing environments
        if "mock-ai-url" in api_host:
            logger.debug(f"Using mock LLM implementation for {model_name}")
            model = MockChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                api_key=api_key,
                openai_api_base=api_host
            )
            
            messages: List[BaseMessage] = []
            
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            api_message = await model.ainvoke(messages)
            result = api_message.content
        else:
            # Use our real LLM client for actual API calls
            logger.debug(f"Using real LLM client for {model_name} with host {api_host}")
            try:
                llm_client = LLMClient(
                    model_name=model_name,
                    api_key=api_key,
                    api_host=api_host,
                    temperature=temperature
                )
                
                result = await llm_client.generate(prompt=prompt, system_prompt=system_prompt)
                logger.debug(f"LLM client returned result: {result[:50]}...")
            except Exception as e:
                logger.error(f"Error calling LLM API: {str(e)}")
                raise ValueError(f"LLM API call failed: {str(e)}")
        return ExecutionResult(
            outputs={
                "result": result
            }
        )
    
    def _check_inputs(self, inputs: LLMExecutorInputs) -> None:
        """
        Check if all required inputs are provided.
        
        Args:
            inputs: The inputs to check.
            
        Raises:
            ValueError: If any required input is missing.
        """
        missing_inputs = []
        
        if "modelName" not in inputs or inputs["modelName"] is None:
            missing_inputs.append("modelName")
        if "temperature" not in inputs or inputs["temperature"] is None:
            missing_inputs.append("temperature")
        if "apiKey" not in inputs or inputs["apiKey"] is None:
            missing_inputs.append("apiKey")
        if "apiHost" not in inputs or inputs["apiHost"] is None:
            missing_inputs.append("apiHost")
        if "prompt" not in inputs or inputs["prompt"] is None:
            missing_inputs.append("prompt")
        
        if missing_inputs:
            raise ValueError(f"LLM node missing required inputs: {', '.join(missing_inputs)}")
