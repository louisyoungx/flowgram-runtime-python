"""
Test complete workflow execution with LLM node.
"""
import asyncio
import logging
import json
from typing import Dict, Any

from src.interface import IEngine, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.application.workflow_application import WorkflowApplication
from src.api.task_run_api import TaskRunAPI
from src.api.task_result_api import TaskResultAPI
from src.api.task_report_api import TaskReportAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_workflow_execution():
    """Test complete workflow execution with LLM node."""
    # Define test workflow schema
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
    
    # Define test inputs
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # Create task run input
    task_run_input = {
        "schema": schema_str,
        "inputs": inputs
    }
    
    # Run the task
    logger.info("Running task with LLM node...")
    task_run_output = await TaskRunAPI(task_run_input)
    task_id = task_run_output["taskID"]
    logger.info(f"Task started with ID: {task_id}")
    
    # Wait for the task to complete
    logger.info("Waiting for task to complete...")
    max_wait_seconds = 10
    wait_interval_seconds = 0.5
    elapsed_seconds = 0
    
    while elapsed_seconds < max_wait_seconds:
        # Check task report
        task_report_input = {"taskID": task_id}
        report = await TaskReportAPI(task_report_input)
        
        if report and "workflowStatus" in report:
            status = report["workflowStatus"].get("status")
            logger.info(f"Current workflow status: {status}")
            
            if status in [WorkflowStatus.Success, WorkflowStatus.Failed, WorkflowStatus.Cancelled]:
                logger.info("Task completed")
                break
        
        await asyncio.sleep(wait_interval_seconds)
        elapsed_seconds += wait_interval_seconds
    
    # Get task result
    logger.info("Getting task result...")
    task_result_input = {"taskID": task_id}
    result = await TaskResultAPI(task_result_input)
    logger.info(f"Task result: {result}")
    
    # Get detailed task report
    logger.info("Getting detailed task report...")
    report = await TaskReportAPI(task_report_input)
    logger.info(f"Task report: {json.dumps(report, indent=2)}")
    
    # Verify task result
    if not result:
        logger.error("Task result is empty")
    elif "answer" not in result:
        logger.error(f"Task result does not contain 'answer' field: {result}")
    elif result["answer"] != "2":
        logger.error(f"Unexpected task result: {result['answer']}, expected: 2")
    else:
        logger.info("Task result is correct: 2")
    
    # Verify task report
    if not report:
        logger.error("Task report is empty")
    elif "workflowStatus" not in report:
        logger.error("Task report does not contain workflowStatus")
    elif report["workflowStatus"].get("status") != WorkflowStatus.Success:
        logger.error(f"Unexpected workflow status: {report['workflowStatus'].get('status')}, expected: {WorkflowStatus.Success}")
    else:
        logger.info(f"Task report status is correct: {report['workflowStatus'].get('status')}")
    
    return task_id, result, report

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_workflow_execution())