"""
Test script for validating condition node handling of array types with is_empty/is_not_empty operators
in a complex workflow scenario.
"""
import os
import sys
import json
import asyncio
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Complex workflow schema with condition nodes testing array emptiness
COMPLEX_WORKFLOW_SCHEMA = {
    "nodes": [
        {
            "id": "start_0",
            "type": "start",
            "meta": {"position": {"x": 180, "y": 346}},
            "data": {
                "title": "Start",
                "outputs": {
                    "type": "object",
                    "properties": {
                        "themes": {
                            "key": 5,
                            "name": "themes",
                            "isPropertyRequired": True,
                            "type": "array",
                            "extra": {"index": 0},
                            "items": {"type": "string"}
                        },
                        "apiKey": {
                            "key": 7,
                            "name": "apiKey",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 1}
                        },
                        "apiHost": {
                            "key": 8,
                            "name": "apiHost",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 2}
                        },
                        "modelName": {
                            "key": 12,
                            "name": "modelName",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 3}
                        }
                    },
                    "required": ["themes", "apiKey", "apiHost", "modelName"]
                }
            }
        },
        {
            "id": "end_0",
            "type": "end",
            "meta": {"position": {"x": 2258.6, "y": 346}},
            "data": {
                "title": "End",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        },
        {
            "id": "condition_0",
            "type": "condition",
            "meta": {"position": {"x": 640, "y": 282.5}},
            "data": {
                "title": "Condition",
                "conditions": [
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "themes"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "themes"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_not_empty"
                    }
                ]
            }
        },
        {
            "id": "llm_1",
            "type": "llm",
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "LLM_1",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "数组为空"}
                },
                "inputs": {
                    "type": "object",
                    "required": ["modelName", "apiKey", "apiHost", "temperature", "prompt"],
                    "properties": {
                        "modelName": {"type": "string"},
                        "apiKey": {"type": "string"},
                        "apiHost": {"type": "string"},
                        "temperature": {"type": "number"},
                        "systemPrompt": {"type": "string"},
                        "prompt": {"type": "string"}
                    }
                },
                "outputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        },
        {
            "id": "llm_2",
            "type": "llm",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "LLM_2",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.6},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "数组不为空"}
                },
                "inputs": {
                    "type": "object",
                    "required": ["modelName", "apiKey", "apiHost", "temperature", "prompt"],
                    "properties": {
                        "modelName": {"type": "string"},
                        "apiKey": {"type": "string"},
                        "apiHost": {"type": "string"},
                        "temperature": {"type": "number"},
                        "systemPrompt": {"type": "string"},
                        "prompt": {"type": "string"}
                    }
                },
                "outputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "llm_1", "targetNodeID": "end_0"},
        {"sourceNodeID": "llm_2", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "llm_1", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "llm_2", "sourcePortID": "if_not_empty"}
    ]
}

async def test_empty_array_condition():
    """Test condition node with empty array."""
    print("\nTesting condition node with empty array...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a task with empty themes array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    # Verify initial status
    assert task.context.status_center.workflow.status == WorkflowStatus.Processing
    
    # Wait for task to complete
    result = await task.processing
    
    # Verify final status and result
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
    
    # Check that the empty array condition branch was taken
    branch = None
    for snapshot in task.context.snapshot_center.export_all():
        if snapshot.node_id == "condition_0":
            branch = snapshot.branch
            break
    
    print(f"Condition branch taken: {branch}")
    assert branch == "if_empty", f"Expected branch 'if_empty', got '{branch}'"
    print("✅ Empty array condition test passed")

async def test_non_empty_array_condition():
    """Test condition node with non-empty array."""
    print("\nTesting condition node with non-empty array...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a task with non-empty themes array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    # Verify initial status
    assert task.context.status_center.workflow.status == WorkflowStatus.Processing
    
    # Wait for task to complete
    result = await task.processing
    
    # Verify final status and result
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
    
    # Check that the non-empty array condition branch was taken
    branch = None
    for snapshot in task.context.snapshot_center.export_all():
        if snapshot.node_id == "condition_0":
            branch = snapshot.branch
            break
    
    print(f"Condition branch taken: {branch}")
    assert branch == "if_not_empty", f"Expected branch 'if_not_empty', got '{branch}'"
    print("✅ Non-empty array condition test passed")

async def run_tests():
    """Run all tests."""
    print("Testing condition node handling of array types with is_empty/is_not_empty operators in complex workflow...")
    await test_empty_array_condition()
    await test_non_empty_array_condition()
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(run_tests())