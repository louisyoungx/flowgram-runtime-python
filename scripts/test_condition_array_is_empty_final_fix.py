"""
Test for condition node handling of array types with is_empty/is_not_empty operators.
"""
import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

# Add the runtime-py-core directory to the Python path
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Define a simple workflow schema with a condition node that checks if an array is empty
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

# Define a complex workflow schema with a condition node that checks if an array is empty
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
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "apiKey": {"type": "string"},
                        "apiHost": {"type": "string"},
                        "modelName": {"type": "string"}
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
            "id": "llm_empty",
            "type": "llm",
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "LLM_Empty",
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
            "id": "llm_not_empty",
            "type": "llm",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "LLM_Not_Empty",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
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
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "llm_not_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_not_empty", "sourcePortID": "if_not_empty"}
    ]
}

class ConditionArrayTest:
    """Test class for condition node handling of array types."""
    
    def __init__(self):
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)
    
    async def test_empty_array_condition(self):
        """Test condition node with empty array."""
        print("\nTesting condition node with empty array...")
        
        # Create a task with an empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": []
            }
        })
        
        # Wait for the task to complete
        await task.processing
        
        # Check if the task completed successfully
        print(f"Task status: {task.context.status_center.workflow.status}")
        assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
        
        # Check if the correct branch was taken
        outputs = task.context.io_center.outputs
        print(f"Task outputs: {outputs}")
        assert outputs.get("result") == "数组为空"
        
        return True
    
    async def test_non_empty_array_condition(self):
        """Test condition node with non-empty array."""
        print("\nTesting condition node with non-empty array...")
        
        # Create a task with a non-empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": ["item1", "item2"]
            }
        })
        
        # Wait for the task to complete
        await task.processing
        
        # Check if the task completed successfully
        print(f"Task status: {task.context.status_center.workflow.status}")
        assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
        
        # Check if the correct branch was taken
        outputs = task.context.io_center.outputs
        print(f"Task outputs: {outputs}")
        assert outputs.get("result") == "数组不为空"
        
        return True
    
    async def test_complex_workflow_empty_array(self):
        """Test condition node in a complex workflow with empty array."""
        print("\nTesting condition node in complex workflow with empty array...")
        
        # Create a task with an empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],
                "apiKey": "test-api-key",
                "apiHost": "https://test-api-host.com",
                "modelName": "test-model"
            }
        })
        
        # Wait for the task to complete
        await task.processing
        
        # Check if the task completed successfully
        print(f"Task status: {task.context.status_center.workflow.status}")
        assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
        
        # Get the snapshot for the condition node to check which branch was taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"Condition node branch: {branch}")
            assert branch == "if_empty"
        else:
            print("No condition node snapshot found")
            assert False, "No condition node snapshot found"
        
        return True
    
    async def test_complex_workflow_non_empty_array(self):
        """Test condition node in a complex workflow with non-empty array."""
        print("\nTesting condition node in complex workflow with non-empty array...")
        
        # Create a task with a non-empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],
                "apiKey": "test-api-key",
                "apiHost": "https://test-api-host.com",
                "modelName": "test-model"
            }
        })
        
        # Wait for the task to complete
        await task.processing
        
        # Check if the task completed successfully
        print(f"Task status: {task.context.status_center.workflow.status}")
        assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded
        
        # Get the snapshot for the condition node to check which branch was taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"Condition node branch: {branch}")
            assert branch == "if_not_empty"
        else:
            print("No condition node snapshot found")
            assert False, "No condition node snapshot found"
        
        return True

async def run_tests():
    """Run all tests."""
    print("Testing condition node handling of array types with is_empty/is_not_empty operators...")
    
    test = ConditionArrayTest()
    
    results = []
    
    # Run all tests
    results.append(await test.test_empty_array_condition())
    results.append(await test.test_non_empty_array_condition())
    results.append(await test.test_complex_workflow_empty_array())
    results.append(await test.test_complex_workflow_non_empty_array())
    
    # Print summary
    print("\nTest Summary:")
    print(f"Total tests: {len(results)}")
    print(f"Passed tests: {sum(results)}")
    print(f"Failed tests: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    asyncio.run(run_tests())