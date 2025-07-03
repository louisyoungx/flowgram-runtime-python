"""
Implementation of a real LLM client that makes API calls to LLM services.
"""
import json
import logging
from typing import Dict, Any, List, Optional

import httpx

logger = logging.getLogger(__name__)

class LLMClient:
    """
    A client for making API calls to LLM services.
    This client is designed to be used with the LLM executor.
    """
    
    def __init__(
        self, 
        model_name: str, 
        api_key: str, 
        api_host: str, 
        temperature: float = 0.7,
        timeout: int = 60
    ):
        """
        Initialize a new LLM client.
        
        Args:
            model_name: The name of the model to use.
            api_key: The API key to use for authentication.
            api_host: The host URL of the API service.
            temperature: The temperature to use for generation.
            timeout: The timeout for API requests in seconds.
        """
        self.model_name = model_name
        self.api_key = api_key
        self.api_host = api_host
        self.temperature = temperature
        self.timeout = timeout
        
        # Normalize API host URL
        if not self.api_host.endswith('/'):
            self.api_host = self.api_host + '/'
        
        # Remove 'api/v3' suffix if present, as we'll add it in the request URL
        if self.api_host.endswith('api/v3/'):
            self.api_host = self.api_host[:-7]
        
        logger.debug(f"Initialized LLM client with model: {model_name}, host: {api_host}")
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using the LLM API.
        
        Args:
            prompt: The user prompt to generate from.
            system_prompt: Optional system prompt to set the context.
            
        Returns:
            The generated text response.
            
        Raises:
            Exception: If the API call fails or returns an error.
        """
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature
        }
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Prepare URL
        url = f"{self.api_host}api/v3/chat/completions"
        
        logger.debug(f"Sending request to {url}")
        logger.debug(f"Request payload: {payload}")
        
        try:
            # Make the API call
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload
                )
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the response
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                
                # Extract the generated text
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    message = response_data["choices"][0].get("message", {})
                    content = message.get("content", "")
                    return content
                else:
                    raise Exception(f"Invalid response format: {response_data}")
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exception(f"API request failed with status code {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise