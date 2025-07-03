"""
Test script for debugging condition node handling of array types and is_empty/is_not_empty operators.
"""
import os
import sys
import asyncio
import json
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Define test schemas
SIMPLE_WORKFLOW_SCHEMA = {
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
                        "array_input": {
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
                            "left": {"type": "ref", "content": ["start_0", "array_input"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array_input"]},
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
        },
        {
            "id": "end_empty",
            "type": "end",
            "meta": {"position": {"x": 1449.3, "y": 100}},
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
            "meta": {"position": {"x": 1449.3, "y": 200}},
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
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "end_empty", "sourcePortID": "if_OVHXT"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "end_not_empty", "sourcePortID": "if_pTr8_"}
    ]
}

async def test_empty_array():
    """Test condition node with empty array."""
    print("\n=== Testing condition node with empty array ===")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Invoke workflow with empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_input": []
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Result: {result}")
    
    # Check workflow status
    status = task.context.status_center.workflow.status
    print(f"Workflow status: {status}")
    
    # Check if the correct branch was taken
    assert result.get("result") == "数组为空", f"Expected '数组为空', got {result}"
    
    return True

async def test_non_empty_array():
    """Test condition node with non-empty array."""
    print("\n=== Testing condition node with non-empty array ===")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Invoke workflow with non-empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_input": ["item1", "item2"]
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Result: {result}")
    
    # Check workflow status
    status = task.context.status_center.workflow.status
    print(f"Workflow status: {status}")
    
    # Check if the correct branch was taken
    assert result.get("result") == "数组不为空", f"Expected '数组不为空', got {result}"
    
    return True

async def test_complex_workflow_empty_array():
    """Test complex workflow with empty array."""
    print("\n=== Testing complex workflow with empty array ===")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Invoke workflow with empty array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host",
            "modelName": "test-model"
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Result: {result}")
    
    # Check workflow status
    status = task.context.status_center.workflow.status
    print(f"Workflow status: {status}")
    
    # Check if the correct branch was taken
    assert result.get("result") == "数组为空", f"Expected '数组为空', got {result}"
    
    return True

async def test_complex_workflow_non_empty_array():
    """Test complex workflow with non-empty array."""
    print("\n=== Testing complex workflow with non-empty array ===")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Invoke workflow with non-empty array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["theme1", "theme2"],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host",
            "modelName": "test-model"
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Result: {result}")
    
    # Check workflow status
    status = task.context.status_center.workflow.status
    print(f"Workflow status: {status}")
    
    # Check if the correct branch was taken
    assert result.get("result") == "数组不为空", f"Expected '数组不为空', got {result}"
    
    return True

async def run_tests():
    """Run all tests."""
    try:
        await test_empty_array()
        print("✅ Empty array test passed")
    except Exception as e:
        print(f"❌ Empty array test failed: {e}")
    
    try:
        await test_non_empty_array()
        print("✅ Non-empty array test passed")
    except Exception as e:
        print(f"❌ Non-empty array test failed: {e}")
    
    try:
        await test_complex_workflow_empty_array()
        print("✅ Complex workflow empty array test passed")
    except Exception as e:
        print(f"❌ Complex workflow empty array test failed: {e}")
    
    try:
        await test_complex_workflow_non_empty_array()
        print("✅ Complex workflow non-empty array test passed")
    except Exception as e:
        print(f"❌ Complex workflow non-empty array test failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())