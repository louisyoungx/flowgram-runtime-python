"""
Test script for the real LLM client implementation.
"""
import asyncio
import logging
from src.nodes.llm.llm_client import LLMClient

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_llm_client():
    """Test the LLM client with a real API call."""
    # API parameters - these should match the ones used in the workflow
    model_name = "ep-20250206192339-nnr9m"
    api_key = "7fe5b737-1fc1-43b4-a8ae-cf35491e7220"
    api_host = "https://ark.cn-beijing.volces.com/api/v3"
    prompt = "Just give me the answer of '1+1=?', just one number, no other words"
    system_prompt = "You are a helpful AI assistant."
    
    logger.info(f"Testing LLM client with model: {model_name}, host: {api_host}")
    
    # Create the LLM client
    client = LLMClient(
        model_name=model_name,
        api_key=api_key,
        api_host=api_host,
        temperature=0
    )
    
    try:
        # Generate text
        logger.info("Sending request to LLM API...")
        response = await client.generate(prompt=prompt, system_prompt=system_prompt)
        
        # Log the response
        logger.info(f"LLM API response: {response}")
        
        # Verify the response is as expected
        if response.strip() == "2":
            logger.info("Test PASSED: Response matches expected output")
        else:
            logger.warning(f"Test WARNING: Response '{response}' does not exactly match expected '2'")
            
    except Exception as e:
        logger.error(f"Test FAILED: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_llm_client())