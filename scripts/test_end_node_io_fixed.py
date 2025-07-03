"""
Test script to verify the data flow through the end node and IO center.
"""
import asyncio
import json
import logging
from typing import Dict, Any

from src.interface import IEngine, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.application.workflow_application import WorkflowApplication

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_end_node_io():
    """Test the data flow through the end node and IO center."""
    # Create the workflow schema
    schema = {
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
                    "inputsValues": {
                        "answer": {"type": "constant", "content": "42"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "answer": {"type": "string"}
                        }
                    }
                }
            }
        ],
        "edges": [
            {"sourceNodeID": "start_0", "targetNodeID": "end_0"}
        ]
    }

    # Create the workflow inputs
    inputs = {
        "model_name": "test-model",
        "api_key": "test-api-key",
        "api_host": "test-api-host",
        "prompt": "test-prompt"
    }

    # Get the engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)

    # Invoke the workflow
    task = engine.invoke({
        "schema": schema,
        "inputs": inputs
    })

    context = task.context
    logger.info(f"Task ID: {task.id}")
    logger.info(f"Initial workflow status: {context.status_center.workflow.status}")

    # Wait for the workflow to complete
    while not context.status_center.workflow.terminated:
        logger.info("Waiting for workflow to complete...")
        await asyncio.sleep(0.1)

    # Log the final status
    logger.info(f"Final workflow status: {context.status_center.workflow.status}")
    
    # Check the end node inputs
    snapshots = context.snapshot_center.export_all()
    end_node_snapshots = [s for s in snapshots if s.get('nodeID') == "end_0"]
    if end_node_snapshots:
        end_snapshot = end_node_snapshots[0]
        logger.info(f"End node inputs: {end_snapshot.get('inputs', {})}")
    else:
        logger.error("No end node snapshot found")
    
    # Check the IO center outputs
    logger.info(f"IO center outputs: {context.io_center.outputs}")
    
    # Check if the outputs match the end node inputs
    if end_node_snapshots and context.io_center.outputs == end_snapshot.get('inputs', {}):
        logger.info("SUCCESS: End node inputs correctly set as IO center outputs")
    else:
        logger.error("FAILURE: End node inputs not correctly set as IO center outputs")
        logger.error(f"End node inputs: {end_snapshot.get('inputs', {}) if end_node_snapshots else 'N/A'}")
        logger.error(f"IO center outputs: {context.io_center.outputs}")

    # Test the WorkflowApplication.result method
    app = WorkflowApplication.instance()
    result = app.result(task.id)
    logger.info(f"WorkflowApplication.result: {result}")
    
    # Check if the result matches the IO center outputs
    if result == context.io_center.outputs:
        logger.info("SUCCESS: WorkflowApplication.result matches IO center outputs")
    else:
        logger.error("FAILURE: WorkflowApplication.result does not match IO center outputs")
        logger.error(f"WorkflowApplication.result: {result}")
        logger.error(f"IO center outputs: {context.io_center.outputs}")

if __name__ == "__main__":
    asyncio.run(test_end_node_io())