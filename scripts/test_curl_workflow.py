"""
Test script to simulate the curl workflow and verify the TaskReport API response.
"""
import json
import asyncio
import logging
import time
from typing import Dict, Any

from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test data matching the curl command
TEST_INPUT = {
    "inputs": {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    },
    "schema": """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
}

async def run_workflow_test():
    """Run the workflow test to verify TaskReport API."""
    try:
        # Step 1: Run the task
        logger.info("Running TaskRunAPI...")
        task_run_result = await TaskRunAPI(TEST_INPUT)
        task_id = task_run_result["taskID"]
        logger.info(f"Task started with ID: {task_id}")
        
        # Step 2: Wait for 5 seconds (as per requirements)
        logger.info("Waiting for 5 seconds...")
        await asyncio.sleep(5)
        
        # Step 3: Get the task report
        logger.info(f"Getting task report for task ID: {task_id}")
        report_result = await TaskReportAPI({"taskID": task_id})
        
        # Step 4: Get the task result
        logger.info(f"Getting task result for task ID: {task_id}")
        result = await TaskResultAPI({"taskID": task_id})
        
        # Log the results
        logger.info(f"Task Result: {json.dumps(result, indent=2)}")
        logger.info(f"Task Report: {json.dumps(report_result, indent=2)}")
        
        # Verify the report structure
        verify_report_structure(report_result)
        
        return task_id, report_result, result
    
    except Exception as e:
        logger.error(f"Error in workflow test: {str(e)}")
        raise

def verify_report_structure(report: Dict[str, Any]):
    """Verify the report has the expected structure."""
    # Check top-level keys
    expected_keys = ["id", "inputs", "outputs", "workflowStatus", "reports"]
    for key in expected_keys:
        if key not in report:
            logger.error(f"Missing expected key in report: {key}")
            return False
    
    # Check workflowStatus
    workflow_status = report.get("workflowStatus", {})
    if not workflow_status.get("status"):
        logger.error("Missing status in workflowStatus")
        return False
    
    # Check if reports contains node reports
    reports = report.get("reports", {})
    expected_nodes = ["start_0", "llm_0", "end_0"]
    for node_id in expected_nodes:
        if node_id not in reports:
            logger.warning(f"Missing node report for: {node_id}")
    
    # Check if any node has snapshots
    has_snapshots = False
    for node_id, node_report in reports.items():
        if "snapshots" in node_report and node_report["snapshots"]:
            has_snapshots = True
            break
    
    if not has_snapshots:
        logger.warning("No snapshots found in any node report")
    
    logger.info("Report structure verification completed")
    return True

if __name__ == "__main__":
    asyncio.run(run_workflow_test())