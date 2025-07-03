"""
Test LLM API client with real API calls.
"""
import asyncio
import logging
from src.nodes.llm.llm_client import LLMClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_llm_client():
    """Test LLM client with a real API call."""
    # Create LLM client
    client = LLMClient()
    
    # Set up parameters for API call
    model_name = "ep-20250206192339-nnr9m"
    api_key = "7fe5b737-1fc1-43b4-a8ae-cf35491e7220"
    api_host = "https://ark.cn-beijing.volces.com/api/v3"
    temperature = 0
    prompt = "Just give me the answer of '1+1=?', just one number, no other words"
    system_prompt = "You are a helpful AI assistant."
    
    # Make API call
    logger.info("Making API call to %s with model %s", api_host, model_name)
    try:
        response = await client.call({
            "modelName": model_name,
            "apiKey": api_key,
            "apiHost": api_host,
            "temperature": temperature,
            "prompt": prompt,
            "systemPrompt": system_prompt
        })
        logger.info("API response: %s", response)
        return response
    except Exception as e:
        logger.error("API call failed: %s", str(e))
        raise

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_llm_client())
    print(f"Result: {result}")