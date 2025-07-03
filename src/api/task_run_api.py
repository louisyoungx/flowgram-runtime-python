"""
Task run API implementation.
This module provides the TaskRunAPI function for running workflow tasks.
"""
import json
from typing import Any, Dict

from ..interface.schema import TaskRunInput, TaskRunOutput
from ..application.workflow_application import WorkflowApplication


async def TaskRunAPI(input_data: TaskRunInput) -> TaskRunOutput:
    """
    Run a workflow task with the given input.
    
    Args:
        input_data: The input data for running the task.
        
    Returns:
        The output data with the task ID.
    """
    app = WorkflowApplication.instance()
    schema_str = input_data["schema"]
    inputs = input_data["inputs"]
    
    # Parse the schema string to a dictionary
    schema = json.loads(schema_str)
    
    # Run the workflow with the schema and inputs
    task_id = app.run({
        "schema": schema,
        "inputs": inputs,
    })
    
    # Create the output with the task ID
    output: TaskRunOutput = {
        "taskID": task_id,
    }
    
    return output