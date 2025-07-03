"""
Task cancel API implementation.
This module provides the TaskCancelAPI function for cancelling workflow tasks.
"""
from typing import Dict, Any

from ..interface.schema import TaskCancelInput
from ..application.workflow_application import WorkflowApplication


async def TaskCancelAPI(input_data: TaskCancelInput) -> Dict[str, bool]:
    """
    Cancel a workflow task with the given input.
    
    Args:
        input_data: The input data containing the task ID.
        
    Returns:
        A dictionary with a success flag.
    """
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Cancel the task
    success = app.cancel(task_id)
    
    # Create the output with the success flag
    output = {
        "success": success
    }
    
    return output