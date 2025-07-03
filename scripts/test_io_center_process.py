"""
Debug script for IO center issues in the workflow process.
"""
import asyncio
import logging
import json
import time
from typing import Dict, Any

from src.interface import IEngine, IExecutor, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.application.workflow_application import WorkflowApplication
from src.domain.engine.workflow_runtime_engine import WorkflowRuntimeEngine
from src.domain.io_center.workflow_runtime_io_center import WorkflowRuntimeIOCenter
from src.domain.context.workflow_runtime_context import WorkflowRuntimeContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_io_center_process():
    """Test the IO center in the workflow process method."""
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

    # Create a context
    context = WorkflowRuntimeContext.create()
    context.init({"schema": schema, "inputs": inputs})

    # Get the engine
    container = WorkflowRuntimeContainer.instance()
    executor = container.get(IExecutor)
    engine_service = {"Executor": executor}
    engine = WorkflowRuntimeEngine(engine_service)

    # Create a custom process method to monitor IO center outputs
    async def monitored_process(context):
        logger.info("Before process, IO center outputs: %s", context.io_center.outputs)
        
        # Get the start node
        start_node = context.document.start
        logger.info(f"Starting workflow execution with start node: {start_node.id}")
        
        # Set workflow status to processing and record start time
        context.status_center.workflow.process()
        context.status_center.workflow._start_time = int(time.time() * 1000)
        
        try:
            # Execute the start node
            await engine.execute_node({"node": start_node, "context": context})
            logger.info("After start node execution, IO center outputs: %s", context.io_center.outputs)
            
            # Check if workflow is already terminated
            if context.status_center.workflow.terminated:
                logger.info("Workflow terminated early")
                return context.io_center.outputs
            
            # Get the outputs
            outputs = context.io_center.outputs
            logger.info(f"Workflow execution completed with outputs: {outputs}")
            
            # Set workflow status to success if not already terminated
            if not context.status_center.workflow.terminated:
                context.status_center.workflow.success()
            
            # Log workflow execution time
            time_cost = context.status_center.workflow.timeCost
            logger.info(f"Workflow execution time: {time_cost}ms")
            
            # Check the outputs again
            logger.info("Final IO center outputs: %s", context.io_center.outputs)
            
            return outputs
        
        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}")
            context.status_center.workflow.fail()
            time_cost = context.status_center.workflow.timeCost
            logger.error(f"Workflow execution failed, time cost: {time_cost}ms")
            raise e

    # Run the monitored process
    result = await monitored_process(context)
    logger.info(f"Process result: {result}")
    
    # Check the end node execution
    snapshots = context.snapshot_center.export_all()
    end_node_snapshots = [s for s in snapshots if s.get('nodeID') == "end_0"]
    if end_node_snapshots:
        end_snapshot = end_node_snapshots[0]
        logger.info(f"End node inputs: {end_snapshot.get('inputs', {})}")
        logger.info(f"End node outputs: {end_snapshot.get('outputs', {})}")
    else:
        logger.error("No end node snapshot found")
    
    # Check the IO center outputs directly
    logger.info(f"Direct IO center outputs: {context.io_center.outputs}")
    
    # Create a new IO center and test set_outputs
    test_io = WorkflowRuntimeIOCenter()
    test_io.init({})
    logger.info(f"New IO center outputs before set: {test_io.outputs}")
    test_io.set_outputs({"test": "value"})
    logger.info(f"New IO center outputs after set: {test_io.outputs}")

if __name__ == "__main__":
    asyncio.run(test_io_center_process())
