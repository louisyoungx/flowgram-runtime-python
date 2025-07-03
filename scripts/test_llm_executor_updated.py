"""
Test script for the updated LLM executor implementation.
"""
import asyncio
import logging
from typing import Dict, Any

from src.nodes.llm.llm_executor import LLMExecutor
from src.interface.executor import ExecutionContext, ExecutionResult

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockContext:
    """Mock execution context for testing."""
    def __init__(self, inputs: Dict[str, Any]):
        self.inputs = inputs
        self.node = {"id": "test_llm_node"}

async def test_llm_executor():
    """Test the updated LLM executor with a real API call."""
    # API parameters - these should match the ones used in the workflow
    model_name = "ep-20250206192339-nnr9m"
    api_key = "7fe5b737-1fc1-43b4-a8ae-cf35491e7220"
    api_host = "https://ark.cn-beijing.volces.com/api/v3"
    prompt = "Just give me the answer of '1+1=?', just one number, no other words"
    system_prompt = "You are a helpful AI assistant."
    
    # Create the inputs for the executor
    inputs = {
        "modelName": model_name,
        "apiKey": api_key,
        "apiHost": api_host,
        "temperature": 0,
        "prompt": prompt,
        "systemPrompt": system_prompt
    }
    
    # Create the context
    context = MockContext(inputs)
    
    # Create the executor
    executor = LLMExecutor()
    
    try:
        # Execute the LLM node
        logger.info("Executing LLM node...")
        result = await executor.execute(context)
        
        # Log the result
        logger.info(f"LLM executor result: {result.outputs}")
        
        # Verify the result
        if "result" in result.outputs and result.outputs["result"].strip() == "2":
            logger.info("Test PASSED: Result matches expected output")
        else:
            logger.warning(f"Test WARNING: Result '{result.outputs.get('result', '')}' does not exactly match expected '2'")
            
    except Exception as e:
        logger.error(f"Test FAILED: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_llm_executor())