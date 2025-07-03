"""
Test script for the workflow API functions.
This script tests the TaskRun, TaskReport, and TaskResult API functions.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any

from src.application.workflow_application import WorkflowApplication
from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_workflow_api():
    """Test the workflow API functions."""
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
    
    # Step 1: Run the workflow using TaskRunAPI
    logger.info("Step 1: Running workflow using TaskRunAPI...")
    task_run_input = {
        "schema": schema_str,
        "inputs": inputs
    }
    task_run_output = await TaskRunAPI(task_run_input)
    task_id = task_run_output["taskID"]
    logger.info(f"Task ID: {task_id}")
    
    # Step 2: Wait a bit for the workflow to complete
    logger.info("Step 2: Waiting for workflow to complete...")
    await asyncio.sleep(5)  # Wait 5 seconds for the workflow to complete
    
    # Step 3: Get the workflow report using TaskReportAPI
    logger.info("Step 3: Getting workflow report using TaskReportAPI...")
    task_report_input = {
        "taskID": task_id
    }
    report = await TaskReportAPI(task_report_input)
    
    logger.info(f"Report: {json.dumps(report, indent=2)}")
    
    # Step 4: Get the workflow result using TaskResultAPI
    logger.info("Step 4: Getting workflow result using TaskResultAPI...")
    task_result_input = {
        "taskID": task_id
    }
    result = await TaskResultAPI(task_result_input)
    
    logger.info(f"Result: {json.dumps(result, indent=2)}")
    
    # Step 5: Verify the result
    if result and "answer" in result and result["answer"].strip() == "2":
        logger.info("Test PASSED: Workflow executed successfully and result matches expected output")
    else:
        logger.error(f"Test FAILED: Result does not match expected output: {result}")
    
    # Step 6: Verify the report
    if (report and 
        "workflowStatus" in report and 
        "status" in report["workflowStatus"] and 
        report["workflowStatus"]["status"] == "succeeded"):
        logger.info("Test PASSED: Workflow report status is 'succeeded'")
    else:
        logger.error(f"Test FAILED: Workflow report status is not 'succeeded': {report}")
    
    return task_id, result, report

if __name__ == "__main__":
    task_id, result, report = asyncio.run(test_workflow_api())
    print(f"\nTask ID: {task_id}")
    print(f"Result: {json.dumps(result, indent=2)}")
    print(f"Report: {json.dumps(report, indent=2)}")