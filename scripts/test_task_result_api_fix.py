"""
Test script to verify and fix the TaskResultAPI issue.
"""
import asyncio
import logging
import time
from typing import Dict, Any

from src.api.task_run_api import TaskRunAPI
from src.api.task_result_api import TaskResultAPI
from src.api.task_report_api import TaskReportAPI
from src.domain.task.workflow_runtime_task import WorkflowRuntimeTask
from src.interface.schema import WorkflowStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test workflow schema (simple workflow with start, LLM, and end nodes)
TEST_SCHEMA = """
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
                "inputsValues": {"answer": {"type": "ref", "content": ["llm_0", "result"]}},
                "inputs": {"type": "object", "properties": {"answer": {"type": "string"}}}
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
                "outputs": {"type": "object", "properties": {"result": {"type": "string"}}}
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "llm_0"},
        {"sourceNodeID": "llm_0", "targetNodeID": "end_0"}
    ]
}
"""

# Test inputs
TEST_INPUTS = {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
}

async def test_task_result_api():
    """Test the TaskResultAPI and fix any issues."""
    logger.info("Starting TaskResultAPI test")
    
    # Step 1: Run a workflow using TaskRunAPI
    task_run_input = {
        "schema": TEST_SCHEMA,
        "inputs": TEST_INPUTS
    }
    
    task_run_output = await TaskRunAPI(task_run_input)
    task_id = task_run_output["taskID"]
    logger.info(f"TaskRunAPI succeeded, taskID: {task_id}")
    
    # Step 2: Wait for the workflow to complete (with timeout)
    max_wait_time = 30  # seconds
    wait_interval = 0.5  # seconds
    total_waited = 0
    
    while total_waited < max_wait_time:
        # Check task status using TaskReportAPI
        task_report_input = {"taskID": task_id}
        report = await TaskReportAPI(task_report_input)
        
        if report and report.get("workflowStatus", {}).get("terminated", False):
            logger.info(f"Workflow terminated with status: {report.get('workflowStatus', {}).get('status', 'unknown')}")
            break
            
        logger.info(f"Waiting for workflow to complete... ({total_waited}s)")
        await asyncio.sleep(wait_interval)
        total_waited += wait_interval
    
    if total_waited >= max_wait_time:
        logger.warning("Timeout waiting for workflow to complete")
    
    # Step 3: Get the task result using TaskResultAPI
    task_result_input = {"taskID": task_id}
    result = await TaskResultAPI(task_result_input)
    
    logger.info(f"TaskResultAPI response: {result}")
    
    # Check if the result contains the expected output
    if result and "answer" in result and result["answer"] == "2":
        logger.info("TaskResultAPI succeeded with expected output")
    else:
        logger.error("TaskResultAPI failed: result does not contain expected output")
        
        # Debug information
        logger.info("Getting detailed report...")
        report = await TaskReportAPI(task_report_input)
        logger.info(f"TaskReportAPI response: {report}")
        
        # Check if the report contains the expected output in end_0 node snapshots
        if report and "reports" in report and "end_0" in report["reports"]:
            end_node = report["reports"]["end_0"]
            if "snapshots" in end_node and end_node["snapshots"]:
                end_snapshot = end_node["snapshots"][-1]
                logger.info(f"End node snapshot: {end_snapshot}")
                if "outputs" in end_snapshot and "answer" in end_snapshot["outputs"]:
                    logger.info(f"End node output found: {end_snapshot['outputs']['answer']}")
                    
                    # Implement fix for TaskResultAPI
                    logger.info("Implementing fix for TaskResultAPI...")
                    # The fix will be to extract the outputs from the end node snapshot
                    # and return them as the task result
                    
                    # This is a simulation of the fix that would be implemented in task_result_api.py
                    from src.application.workflow_application import WorkflowApplication
                    app = WorkflowApplication.instance()
                    task = app.tasks.get(task_id)
                    
                    if task and task.context and task.context.status_center.workflow.terminated:
                        # Check if there are any snapshots for the end node
                        snapshots = task.context.snapshot_center.export_all()
                        end_node_snapshots = [s for s in snapshots if s.get("nodeID") == "end_0"]
                        
                        if end_node_snapshots:
                            # Get the last snapshot of the end node
                            last_snapshot = end_node_snapshots[-1]
                            if "outputs" in last_snapshot:
                                # Use the outputs from the end node snapshot as the task result
                                logger.info(f"Fixed result would be: {last_snapshot['outputs']}")
                                return
    
    logger.info("TaskResultAPI test completed")

async def main():
    """Main function to run the tests."""
    await test_task_result_api()

if __name__ == "__main__":
    asyncio.run(main())