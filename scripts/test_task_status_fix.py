"""
Test script to verify the fix for the TaskReport API always returning 'processing' status.
"""
import asyncio
import json
import time
from src.application.workflow_application import WorkflowApplication
from src.interface.schema import WorkflowStatus

# Test workflow schema - a simple workflow with start and end nodes
TEST_SCHEMA = {
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
                    "result": {"type": "ref", "content": ["start_0", "test_value"]}
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
        {
            "sourceNodeID": "start_0",
            "targetNodeID": "end_0"
        }
    ]
}

async def test_task_status_update():
    """Test that task status is correctly updated after workflow execution."""
    app = WorkflowApplication.instance()
    
    # Run a simple workflow
    task_id = app.run({
        "schema": TEST_SCHEMA,
        "inputs": {
            "test_value": "test_data"
        }
    })
    
    print(f"Task created with ID: {task_id}")
    
    # Wait a bit for the workflow to complete
    await asyncio.sleep(0.5)
    
    # Get the task report
    report = app.report(task_id)
    
    # Check the report status
    print(f"Task report status: {report.workflow_status.status}")
    print(f"Task report terminated: {report.workflow_status.terminated}")
    
    # Verify that the status is not 'processing'
    assert report.workflow_status.status == WorkflowStatus.Succeeded, \
        f"Expected status to be {WorkflowStatus.Succeeded}, but got {report.workflow_status.status}"
    
    # Verify that the workflow is marked as terminated
    assert report.workflow_status.terminated == True, \
        f"Expected terminated to be True, but got {report.workflow_status.terminated}"
    
    print("Test passed! TaskReport API now correctly updates status.")

if __name__ == "__main__":
    asyncio.run(test_task_status_update())