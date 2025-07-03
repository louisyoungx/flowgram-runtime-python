"""
Debug script for IO center issues.
"""
import asyncio
import logging
import json
from typing import Dict, Any

from src.interface import IEngine, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.application.workflow_application import WorkflowApplication
from src.domain.io_center.workflow_runtime_io_center import WorkflowRuntimeIOCenter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_io_center_debug():
    """Test the IO center with a simple workflow."""
    # Create a simple workflow schema with start and end nodes
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
                            "test_value": {"type": "string"}
                        }
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
                        "result": {"type": "constant", "content": "test_result"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
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
        "test_value": "test_input"
    }

    # Get the engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)

    # Create a test IO center
    test_io_center = WorkflowRuntimeIOCenter()
    test_io_center.init(inputs)
    logger.info(f"Initial IO center inputs: {test_io_center.inputs}")
    logger.info(f"Initial IO center outputs: {test_io_center.outputs}")

    # Test set_outputs directly
    test_outputs = {"test_output": "test_value"}
    test_io_center.set_outputs(test_outputs)
    logger.info(f"After set_outputs, IO center outputs: {test_io_center.outputs}")

    # Reset the IO center
    test_io_center.init(inputs)
    logger.info(f"Reset IO center inputs: {test_io_center.inputs}")
    logger.info(f"Reset IO center outputs: {test_io_center.outputs}")

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
        logger.info(f"End node outputs: {end_snapshot.get('outputs', {})}")
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

    # Debug the end executor by directly calling it
    from src.nodes.end.end_executor import EndExecutor
    from src.interface.executor import ExecutionContext, ExecutionResult
    
    # Create a test context
    test_inputs = {"test_result": "direct_test"}
    test_executor = EndExecutor()
    
    # Create a mock node
    class MockNode:
        def __init__(self):
            self.id = "test_end"
            self.type = "end"
    
    # Create a mock execution context
    mock_context = ExecutionContext(
        node=MockNode(),
        inputs=test_inputs,
        runtime=context,  # Use the real context
        container=container
    )
    
    # Execute the end executor directly
    logger.info("Executing end executor directly...")
    result = await test_executor.execute(mock_context)
    logger.info(f"Direct execution result: {result.outputs}")
    
    # Check the IO center outputs after direct execution
    logger.info(f"IO center outputs after direct execution: {context.io_center.outputs}")
    
    # Check if the outputs match the direct execution inputs
    if context.io_center.outputs == test_inputs:
        logger.info("SUCCESS: Direct execution inputs correctly set as IO center outputs")
    else:
        logger.error("FAILURE: Direct execution inputs not correctly set as IO center outputs")
        logger.error(f"Direct execution inputs: {test_inputs}")
        logger.error(f"IO center outputs: {context.io_center.outputs}")

if __name__ == "__main__":
    asyncio.run(test_io_center_debug())