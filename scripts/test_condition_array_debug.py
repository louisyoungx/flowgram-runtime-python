"""
Test script to debug condition node handling of array types with is_empty/is_not_empty operators.
"""
import asyncio
import os
import sys
from typing import Dict, Any

# Import from runtime-py-core
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Define a simple workflow schema with condition node testing array emptiness
EMPTY_ARRAY_TEST_SCHEMA = {
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
                        "array_data": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        },
        {
            "id": "condition_0",
            "type": "condition",
            "meta": {"position": {"x": 300, "y": 0}},
            "data": {
                "title": "Condition",
                "conditions": [
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array_data"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array_data"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_not_empty"
                    }
                ]
            }
        },
        {
            "id": "end_empty",
            "type": "end",
            "meta": {"position": {"x": 600, "y": -100}},
            "data": {
                "title": "End Empty",
                "inputsValues": {
                    "result": {"type": "constant", "content": "数组为空"}
                },
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        },
        {
            "id": "end_not_empty",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 100}},
            "data": {
                "title": "End Not Empty",
                "inputsValues": {
                    "result": {"type": "constant", "content": "数组不为空"}
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
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_not_empty", "sourcePortID": "if_not_empty"}
    ]
}

# Define a complex workflow schema with condition node and loop node
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
            "id": "condition_Ts3zx",
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
                        "key": "if_OVHXT"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "themes"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_pTr8_"
                    }
                ]
            }
        },
        {
            "id": "llm_FKRbD",
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
                    "prompt": {"type": "constant", "content": "没填参数就失败了"}
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
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"},
    ]
}

async def test_empty_array():
    """Test condition node with empty array."""
    print("\n=== Testing Empty Array ===")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with empty array
    task = engine.invoke({
        "schema": EMPTY_ARRAY_TEST_SCHEMA,
        "inputs": {
            "array_data": []
        }
    })
    
    # Wait for the task to complete
    result = await task.processing
    print(f"Result: {result}")
    
    # Check if the condition node correctly identified the array as empty
    assert result.get("result") == "数组为空", f"Expected '数组为空', got {result}"
    print("✅ Empty array test passed")

async def test_non_empty_array():
    """Test condition node with non-empty array."""
    print("\n=== Testing Non-Empty Array ===")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with non-empty array
    task = engine.invoke({
        "schema": EMPTY_ARRAY_TEST_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2"]
        }
    })
    
    # Wait for the task to complete
    result = await task.processing
    print(f"Result: {result}")
    
    # Check if the condition node correctly identified the array as not empty
    assert result.get("result") == "数组不为空", f"Expected '数组不为空', got {result}"
    print("✅ Non-empty array test passed")

async def test_complex_workflow_empty_array():
    """Test complex workflow with empty array."""
    print("\n=== Testing Complex Workflow with Empty Array ===")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with empty themes array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    # Wait for the task to complete
    try:
        result = await task.processing
        print(f"Result: {result}")
        print("✅ Complex workflow with empty array test passed")
    except Exception as e:
        print(f"❌ Complex workflow test failed: {e}")
        # Print the task status and context information for debugging
        print(f"Task status: {task.status}")
        if hasattr(task, 'context') and task.context:
            print(f"Workflow status: {task.context.status_center.workflow.status}")
            # Print node statuses
            for node_id in ["start_0", "condition_Ts3zx", "llm_FKRbD"]:
                node_status = task.context.status_center.node_status(node_id)
                if node_status:
                    print(f"Node {node_id} status: {node_status.status}")

async def main():
    """Run all tests."""
    try:
        await test_empty_array()
        await test_non_empty_array()
        await test_complex_workflow_empty_array()
    except Exception as e:
        print(f"Tests failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())