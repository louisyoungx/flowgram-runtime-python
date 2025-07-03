"""
Test script for the complete LLM workflow execution.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any

from src.domain.container import WorkflowRuntimeContainer
from src.interface import IEngine, WorkflowStatus

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_llm_workflow():
    """Test the complete LLM workflow execution."""
    # Get the container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Define the workflow schema
    schema_str = """
    {
        "nodes": [
            {
                "id": "start_0",
                "type": "start",
                "meta": {"position": {"x": 0, "y": 0}},
                "data": {
                    "title": "Start",
                    "outputs": {
                        "type": "object",
                        "properties": {
                            "model_name": {"key": 14, "name": "model_name", "type": "string", "extra": {"index": 1}, "isPropertyRequired": true},
                            "prompt": {"key": 5, "name": "prompt", "type": "string", "extra": {"index": 3}, "isPropertyRequired": true},
                            "api_key": {"key": 19, "name": "api_key", "type": "string", "extra": {"index": 4}, "isPropertyRequired": true},
                            "api_host": {"key": 20, "name": "api_host", "type": "string", "extra": {"index": 5}, "isPropertyRequired": true}
                        },
                        "required": ["model_name", "prompt", "api_key", "api_host"]
                    }
                }
            },
            {
                "id": "end_0",
                "type": "end",
                "meta": {"position": {"x": 1000, "y": 0}},
                "data": {
                    "title": "End",
                    "inputsValues": {
                        "answer": {"type": "ref", "content": ["llm_0", "result"]}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "answer": {"type": "string"}
                        }
                    }
                }
            },
            {
                "id": "llm_0",
                "type": "llm",
                "meta": {"position": {"x": 500, "y": 0}},
                "data": {
                    "title": "LLM_0",
                    "inputsValues": {
                        "modelName": {"type": "ref", "content": ["start_0", "model_name"]},
                        "apiKey": {"type": "ref", "content": ["start_0", "api_key"]},
                        "apiHost": {"type": "ref", "content": ["start_0", "api_host"]},
                        "temperature": {"type": "constant", "content": 0},
                        "prompt": {"type": "ref", "content": ["start_0", "prompt"]},
                        "systemPrompt": {"type": "constant", "content": "You are a helpful AI assistant."}
                    },
                    "inputs": {
                        "type": "object",
                        "required": ["modelName", "temperature", "prompt"],
                        "properties": {
                            "modelName": {"type": "string"},
                            "apiKey": {"type": "string"},
                            "apiHost": {"type": "string"},
                            "temperature": {"type": "number"},
                            "systemPrompt": {"type": "string"},
                            "prompt": {"type": "string"}
                        }
                    },
                    "outputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    }
                }
            }
        ],
        "edges": [
            {"sourceNodeID": "start_0", "targetNodeID": "llm_0"},
            {"sourceNodeID": "llm_0", "targetNodeID": "end_0"}
        ]
    }
    """
    
    # Define the workflow inputs
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # Invoke the workflow
    logger.info("Invoking workflow...")
    task = engine.invoke({
        "schema": json.loads(schema_str),
        "inputs": inputs
    })
    
    # Get the task ID
    task_id = task.id
    logger.info(f"Task ID: {task_id}")
    
    # Wait for the workflow to complete
    logger.info("Waiting for workflow to complete...")
    start_time = time.time()
    timeout = 30  # seconds
    
    while not task.context.status_center.workflow.terminated:
        await asyncio.sleep(0.5)
        elapsed = time.time() - start_time
        if elapsed > timeout:
            logger.error(f"Workflow execution timed out after {timeout} seconds")
            break
            
    # Get the workflow status
    status = task.context.status_center.workflow.status
    logger.info(f"Workflow status: {status}")
    
    # Get the workflow result
    result = task.context.io_center.outputs
    logger.info(f"Workflow result: {result}")
    
    # Get the workflow report
    report = task.context.reporter.export()
    logger.info(f"Workflow report ID: {report.id}")
    logger.info(f"Workflow report status: {report.workflowStatus['status']}")
    
    # Verify the result
    if str(status) == "succeeded" and result and "answer" in result and result["answer"].strip() == "2":
        logger.info("Test PASSED: Workflow executed successfully and result matches expected output")
    else:
        logger.warning(f"Test WARNING: Workflow status: {status}, result: {result}")
    
    # Return the task ID for further testing
    return task_id

if __name__ == "__main__":
    task_id = asyncio.run(test_llm_workflow())
    print(f"\nTask ID for further testing: {task_id}")
