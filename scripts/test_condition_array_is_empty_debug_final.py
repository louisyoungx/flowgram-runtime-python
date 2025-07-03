"""
Test script for debugging condition node handling of array types and is_empty/is_not_empty operators.
"""
import os
import sys
import json
import asyncio
import unittest
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Define test workflow schemas
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
            "meta": {"position": {"x": 500, "y": 0}},
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
            "meta": {"position": {"x": 1000, "y": -200}},
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
            "meta": {"position": {"x": 1000, "y": 200}},
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
            "id": "loop_2OD2p",
            "type": "loop",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "Loop_1",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "832659",
                    "type": "llm",
                    "meta": {"position": {"x": 189.65, "y": 0}},
                    "data": {
                        "title": "LLM_1",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {
                                "type": "constant",
                                "content": "用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题，例如输入\"露营\"，返回\"在瑞士阿尔卑斯山的露营之旅\""
                            },
                            "prompt": {"type": "ref", "content": ["loop_2OD2p_locals", "item"]}
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
                    "id": "llm_KYkc0",
                    "type": "llm",
                    "meta": {"position": {"x": 668.95, "y": 0}},
                    "data": {
                        "title": "LLM_4",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {
                                "type": "constant",
                                "content": "用户传入的是一个标题，你需要根据这个标题生成一个小于50字的简短的介绍"
                            },
                            "prompt": {"type": "ref", "content": ["832659", "result"]}
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
            "edges": [{"sourceNodeID": "832659", "targetNodeID": "llm_KYkc0"}]
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "loop_2OD2p", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "loop_2OD2p", "sourcePortID": "if_pTr8_"}
    ]
}

async def test_empty_array_condition():
    """Test condition node with empty array."""
    print("\nTesting condition node with empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a workflow with an empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": []  # Empty array
        }
    })
    
    # Wait for the workflow to complete
    result = await task.processing
    
    # Verify that the condition node selected the "if_empty" branch
    print(f"Task status: {task.context.status_center.workflow.status}")
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "数组为空"}
    
    return True

async def test_non_empty_array_condition():
    """Test condition node with non-empty array."""
    print("\nTesting condition node with non-empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a workflow with a non-empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2"]  # Non-empty array
        }
    })
    
    # Wait for the workflow to complete
    result = await task.processing
    
    # Verify that the condition node selected the "if_not_empty" branch
    print(f"Task status: {task.context.status_center.workflow.status}")
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "数组不为空"}
    
    return True

async def test_complex_workflow_empty_array():
    """Test complex workflow with empty array."""
    print("\nTesting complex workflow with empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a workflow with an empty array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],  # Empty array
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host.com",
            "modelName": "test-model"
        }
    })
    
    try:
        # Wait for the workflow to complete
        result = await task.processing
        
        # Verify that the condition node selected the "if_OVHXT" branch (empty array)
        print(f"Task status: {task.context.status_center.workflow.status}")
        branch = None
        for snapshot in task.context.snapshot_center.export_all():
            if snapshot.node_id == "condition_Ts3zx":
                branch = snapshot.branch
                break
        
        print(f"Selected branch: {branch}")
        assert branch == "if_OVHXT"
        
        return True
    except Exception as e:
        print(f"Error in complex workflow test: {e}")
        return False

async def test_complex_workflow_non_empty_array():
    """Test complex workflow with non-empty array."""
    print("\nTesting complex workflow with non-empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create a workflow with a non-empty array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],  # Non-empty array
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host.com",
            "modelName": "test-model"
        }
    })
    
    try:
        # Wait for the workflow to complete
        result = await task.processing
        
        # Verify that the condition node selected the "if_pTr8_" branch (non-empty array)
        print(f"Task status: {task.context.status_center.workflow.status}")
        branch = None
        for snapshot in task.context.snapshot_center.export_all():
            if snapshot.node_id == "condition_Ts3zx":
                branch = snapshot.branch
                break
        
        print(f"Selected branch: {branch}")
        assert branch == "if_pTr8_"
        
        return True
    except Exception as e:
        print(f"Error in complex workflow test: {e}")
        return False

async def run_tests():
    """Run all tests."""
    print("Testing condition node handling of array types with is_empty/is_not_empty operators...")
    
    results = []
    
    # Test simple workflows
    results.append(await test_empty_array_condition())
    results.append(await test_non_empty_array_condition())
    
    # Test complex workflows
    results.append(await test_complex_workflow_empty_array())
    results.append(await test_complex_workflow_non_empty_array())
    
    # Print summary
    print("\nTest Results:")
    print(f"Empty array condition: {'✅ Passed' if results[0] else '❌ Failed'}")
    print(f"Non-empty array condition: {'✅ Passed' if results[1] else '❌ Failed'}")
    print(f"Complex workflow (empty array): {'✅ Passed' if results[2] else '❌ Failed'}")
    print(f"Complex workflow (non-empty array): {'✅ Passed' if results[3] else '❌ Failed'}")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_tests())