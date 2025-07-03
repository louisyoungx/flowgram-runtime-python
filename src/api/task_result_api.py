"""
Task result API implementation.
This module provides the TaskResultAPI function for getting workflow task results.
"""
import logging
from typing import Any, Dict, Optional

from ..interface.schema import TaskResultInput, WorkflowOutputs
from ..application.workflow_application import WorkflowApplication


async def TaskResultAPI(input_data: TaskResultInput) -> WorkflowOutputs:
    """
    Get the result of a workflow task with the given input.
    
    Args:
        input_data: The input data containing the task ID.
        
    Returns:
        The output data with the workflow results.
    """
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Get the task first
    task = app.tasks.get(task_id)
    output = {}
    
    # Only proceed if task exists
    if task and hasattr(task, 'context'):
        # First check if the task is terminated (following JS implementation)
        if not task.context.status_center.workflow.terminated:
            logging.info(f"TaskResultAPI: Task {task_id} is not terminated yet, returning empty result")
            return {}
            
        logging.info(f"TaskResultAPI: Getting result for terminated task {task_id}")
        
        # Strategy 1: Try to get outputs directly from io_center (primary source, as in JS implementation)
        if hasattr(task.context, 'io_center'):
            # Try both public and private attributes
            io_outputs = None
            if hasattr(task.context.io_center, 'outputs'):
                io_outputs = task.context.io_center.outputs
            elif hasattr(task.context.io_center, '_outputs'):
                io_outputs = task.context.io_center._outputs
                
            if io_outputs and len(io_outputs) > 0:
                logging.info(f"TaskResultAPI: Found outputs in io_center: {io_outputs}")
                output = io_outputs
                return output
        
        # Strategy 2: Try to get from end node snapshot if io_center didn't have results
        if not output or len(output) == 0:
            if hasattr(task.context, 'snapshot_center') and hasattr(task.context.snapshot_center, 'export_all'):
                # Get snapshots for the end node
                snapshots = task.context.snapshot_center.export_all()
                end_node_snapshots = [s for s in snapshots if s.get("nodeID") == "end_0"]
                
                if end_node_snapshots:
                    # Get the last snapshot of the end node
                    last_snapshot = end_node_snapshots[-1]
                    if "outputs" in last_snapshot and last_snapshot["outputs"]:
                        logging.info(f"TaskResultAPI: Found outputs in end node snapshot: {last_snapshot['outputs']}")
                        output = last_snapshot["outputs"]
                        return output
        
        # Strategy 3: Fall back to app.result as last resort
        if not output or len(output) == 0:
            app_result = app.result(task_id)
            if app_result and len(app_result) > 0:
                logging.info(f"TaskResultAPI: Found outputs from app.result: {app_result}")
                output = app_result
                return output
    else:
        # If task doesn't exist, fall back to app.result
        output = app.result(task_id)
    
    return output or {}
