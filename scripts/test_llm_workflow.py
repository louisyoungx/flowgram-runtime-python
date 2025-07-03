"""
Test script to verify that the LLM node in the workflow actually makes API calls.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any

from src.domain.container import WorkflowRuntimeContainer
from src.interface import IEngine, WorkflowStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schema for a simple workflow with LLM node
WORKFLOW_SCHEMA = {
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
                        "model_name": {"key": 14, "name": "model_name", "type": "string", "extra": {"index": 1}, "isPropertyRequired": True},
                        "prompt": {"key": 5, "name": "prompt", "type": "string", "extra": {"index": 3}, "isPropertyRequired": True},
                        "api_key": {"key": 19, "name": "api_key", "type": "string", "extra": {"index": 4}, "isPropertyRequired": True},
                        "api_host": {"key": 20, "name": "api_host", "type": "string", "extra": {"index": 5}, "isPropertyRequired": True}
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

# Inputs for the workflow
WORKFLOW_INPUTS = {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
}

async def run_workflow():
    """Run the workflow and monitor its execution."""
    # Get the workflow engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Invoke the workflow
    logger.info("Starting workflow execution...")
    task = engine.invoke({
        "schema": WORKFLOW_SCHEMA,
        "inputs": WORKFLOW_INPUTS
    })
    
    # Get the context for monitoring
    context = task.context
    
    # Print initial status
    logger.info(f"Initial workflow status: {context.status_center.workflow.status}")
    
    # Monitor the workflow execution
    start_time = time.time()
    timeout = 30  # 30 seconds timeout
    
    while not context.status_center.workflow.terminated:
        await asyncio.sleep(1)
        logger.info(f"Current workflow status: {context.status_center.workflow.status}")
        
        # Check for timeout
        if time.time() - start_time > timeout:
            logger.error("Workflow execution timed out")
            return
    
    # Wait for the processing to complete
    result = await task.processing
    
    # Print the final status and result
    logger.info(f"Final workflow status: {context.status_center.workflow.status}")
    logger.info(f"Workflow result: {result}")
    
    # Print the report
    report = context.reporter.export()
    logger.info(f"Workflow report ID: {report.id}")
    logger.info(f"Workflow report status: {report.workflowStatus}")
    
    # Print node reports
    for node_id, node_report in report.reports.items():
        logger.info(f"Node {node_id} status: {node_report['status']}")
        if node_id == "llm_0" and len(node_report['snapshots']) > 0:
            logger.info(f"LLM node inputs: {node_report['snapshots'][0].get('inputs', {})}")
            logger.info(f"LLM node outputs: {node_report['snapshots'][0].get('outputs', {})}")
    
    return result, report

if __name__ == "__main__":
    # Run the workflow
    result, report = asyncio.run(run_workflow())
    
    # Print the final result in a structured format
    print("\n===== FINAL RESULT =====")
    if isinstance(result, dict) and "answer" in result:
        print(f"Answer: {result['answer']}")
    else:
        print(f"Result: {result}")
    
    # Print report summary
    print("\n===== REPORT SUMMARY =====")
    print(f"Workflow status: {report.workflowStatus.get('status', 'unknown')}")
    print(f"Execution time: {report.workflowStatus.get('timeCost', 0)} ms")
    
    # Check if LLM node executed successfully
    llm_node = report.reports.get("llm_0", {})
    if llm_node:
        print(f"LLM node status: {llm_node.get('status', 'unknown')}")
        snapshots = llm_node.get('snapshots', [])
        if snapshots and len(snapshots) > 0:
            outputs = snapshots[0].get('outputs', {})
            if 'result' in outputs:
                print(f"LLM response: {outputs['result']}")
            else:
                print("LLM did not return a result")
        else:
            print("No snapshots found for LLM node")