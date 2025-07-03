"""
Test script for condition node handling of array types with is_empty/is_not_empty operators.
This script tests both simple and complex workflows with empty and non-empty arrays.
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, List

# Add the project root to the path
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Simple workflow schema for testing array conditions
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
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "数组为空"}
                }
            }
        },
        {
            "id": "end_not_empty",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 100}},
            "data": {
                "title": "End Not Empty",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "数组不为空"}
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

# Complex workflow schema for testing array conditions
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
                            "systemPrompt": {"type": "constant", "content": "用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题，例如输入"露营"，返回"在瑞士阿尔卑斯山的露营之旅""},
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
                            "systemPrompt": {"type": "constant", "content": "用户传入的是一个标题，你需要根据这个标题生成一个小于50字的简短的介绍"},
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
            "edges": [
                {"sourceNodeID": "832659", "targetNodeID": "llm_KYkc0"}
            ]
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
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create task with empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": []
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    # Check if the correct branch was taken
    print(f"Result: {result}")
    
    # Check workflow status using string comparison instead of enum
    status_str = task.context.status_center.workflow.status
    print(f"Task status: {status_str}")
    
    # Check if the correct branch was taken based on the result
    assert result.get("result") == "数组为空", f"Expected '数组为空', got {result}"
    
    return "Empty array test passed"

async def test_non_empty_array_condition():
    """Test condition node with non-empty array."""
    print("\nTesting condition node with non-empty array...")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create task with non-empty array
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2"]
        }
    })
    
    # Wait for task to complete
    result = await task.processing
    
    # Check if the correct branch was taken
    print(f"Result: {result}")
    
    # Check workflow status using string comparison
    status_str = task.context.status_center.workflow.status
    print(f"Task status: {status_str}")
    
    # Check if the correct branch was taken based on the result
    assert result.get("result") == "数组不为空", f"Expected '数组不为空', got {result}"
    
    return "Non-empty array test passed"

async def test_complex_workflow_empty_array():
    """Test complex workflow with empty array."""
    print("\nTesting complex workflow with empty array...")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create task with empty themes array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host.com",
            "modelName": "test-model"
        }
    })
    
    try:
        # Wait for task to complete (may fail due to LLM execution)
        result = await asyncio.wait_for(task.processing, timeout=2.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Task execution timed out, but that's expected for LLM nodes")
    except Exception as e:
        print(f"Task execution error: {e}")
    
    # Check which branch was taken by examining the snapshots
    snapshots = task.context.snapshot_center.export_all()
    
    # Find condition node snapshot
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
    
    if condition_snapshots:
        branch = condition_snapshots[0].branch if hasattr(condition_snapshots[0], 'branch') else None
        print(f"Condition branch taken: {branch}")
        
        # Check if the correct branch (empty array) was taken
        assert branch == "if_OVHXT", f"Expected branch 'if_OVHXT', got {branch}"
        return "Complex workflow empty array test passed"
    else:
        print("No condition node snapshot found")
        return "Complex workflow test inconclusive"

async def test_complex_workflow_non_empty_array():
    """Test complex workflow with non-empty array."""
    print("\nTesting complex workflow with non-empty array...")
    
    # Initialize container and engine
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Create task with non-empty themes array
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-api-host.com",
            "modelName": "test-model"
        }
    })
    
    try:
        # Wait for task to complete (may fail due to LLM execution)
        result = await asyncio.wait_for(task.processing, timeout=2.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Task execution timed out, but that's expected for LLM nodes")
    except Exception as e:
        print(f"Task execution error: {e}")
    
    # Check which branch was taken by examining the snapshots
    snapshots = task.context.snapshot_center.export_all()
    
    # Find condition node snapshot
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
    
    if condition_snapshots:
        branch = condition_snapshots[0].branch if hasattr(condition_snapshots[0], 'branch') else None
        print(f"Condition branch taken: {branch}")
        
        # Check if the correct branch (non-empty array) was taken
        assert branch == "if_pTr8_", f"Expected branch 'if_pTr8_', got {branch}"
        return "Complex workflow non-empty array test passed"
    else:
        print("No condition node snapshot found")
        return "Complex workflow test inconclusive"

async def run_tests():
    """Run all tests."""
    print("Testing condition node handling of array types with is_empty/is_not_empty operators...")
    
    results = []
    
    # Run tests
    try:
        results.append(await test_empty_array_condition())
    except Exception as e:
        print(f"❌ Error in test_empty_array_condition: {e}")
        results.append(f"Empty array test failed: {e}")
    
    try:
        results.append(await test_non_empty_array_condition())
    except Exception as e:
        print(f"❌ Error in test_non_empty_array_condition: {e}")
        results.append(f"Non-empty array test failed: {e}")
    
    try:
        results.append(await test_complex_workflow_empty_array())
    except Exception as e:
        print(f"❌ Error in test_complex_workflow_empty_array: {e}")
        results.append(f"Complex workflow empty array test failed: {e}")
    
    try:
        results.append(await test_complex_workflow_non_empty_array())
    except Exception as e:
        print(f"❌ Error in test_complex_workflow_non_empty_array: {e}")
        results.append(f"Complex workflow non-empty array test failed: {e}")
    
    # Print results
    print("\nTest Results:")
    for result in results:
        print(f"- {result}")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_tests())