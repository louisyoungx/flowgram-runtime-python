"""
Test script for condition node handling of array types with is_empty/is_not_empty operators.
"""
import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

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

# Complex workflow with nested conditions and loops
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
            "id": "llm_empty",
            "type": "llm",
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "LLM Empty",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "主题数组为空"}
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
            "id": "loop_not_empty",
            "type": "loop",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "Loop Not Empty",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "llm_loop_1",
                    "type": "llm",
                    "meta": {"position": {"x": 189.65, "y": 0}},
                    "data": {
                        "title": "LLM Loop 1",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "处理主题数组中的项目"},
                            "prompt": {"type": "ref", "content": ["loop_not_empty_locals", "item"]}
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
            "edges": []
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "llm_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "loop_not_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "llm_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "loop_not_empty", "sourcePortID": "if_not_empty"}
    ]
}

class ConditionArrayTest(unittest.TestCase):
    """Test class for condition node handling of array types."""
    
    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)
    
    async def test_empty_array_condition(self):
        """Test condition node with empty array."""
        # Create task with empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": []  # Empty array
            }
        })
        
        # Wait for task to complete
        result = await task.processing
        
        # Verify the result
        self.assertEqual(result, {"result": "数组为空"})
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Success)
        
        # Verify the branch taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot)
        self.assertEqual(condition_snapshot.branch, "if_empty")
    
    async def test_non_empty_array_condition(self):
        """Test condition node with non-empty array."""
        # Create task with non-empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": ["item1", "item2"]  # Non-empty array
            }
        })
        
        # Wait for task to complete
        result = await task.processing
        
        # Verify the result
        self.assertEqual(result, {"result": "数组不为空"})
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Success)
        
        # Verify the branch taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot)
        self.assertEqual(condition_snapshot.branch, "if_not_empty")
    
    async def test_complex_workflow_empty_array(self):
        """Test complex workflow with empty array."""
        # Create task with empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],  # Empty array
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            }
        })
        
        try:
            # Wait for task to complete
            await task.processing
            
            # Verify the branch taken
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshot = None
            for snapshot in snapshots:
                if snapshot.node_id == "condition_0":
                    condition_snapshot = snapshot
                    break
            
            self.assertIsNotNone(condition_snapshot)
            self.assertEqual(condition_snapshot.branch, "if_empty")
            
        except Exception as e:
            print(f"❌ Error in complex workflow test with empty array: {e}")
            # Even if there's an error in the LLM execution, we still want to verify the condition branch
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshot = None
            for snapshot in snapshots:
                if snapshot.node_id == "condition_0":
                    condition_snapshot = snapshot
                    break
            
            if condition_snapshot:
                print(f"Branch taken: {condition_snapshot.branch}")
                self.assertEqual(condition_snapshot.branch, "if_empty")
            else:
                self.fail("Condition snapshot not found")
    
    async def test_complex_workflow_non_empty_array(self):
        """Test complex workflow with non-empty array."""
        # Create task with non-empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],  # Non-empty array
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            }
        })
        
        try:
            # Wait for task to complete
            await task.processing
            
            # Verify the branch taken
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshot = None
            for snapshot in snapshots:
                if snapshot.node_id == "condition_0":
                    condition_snapshot = snapshot
                    break
            
            self.assertIsNotNone(condition_snapshot)
            self.assertEqual(condition_snapshot.branch, "if_not_empty")
            
        except Exception as e:
            print(f"❌ Error in complex workflow test with non-empty array: {e}")
            # Even if there's an error in the LLM execution, we still want to verify the condition branch
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshot = None
            for snapshot in snapshots:
                if snapshot.node_id == "condition_0":
                    condition_snapshot = snapshot
                    break
            
            if condition_snapshot:
                print(f"Branch taken: {condition_snapshot.branch}")
                self.assertEqual(condition_snapshot.branch, "if_not_empty")
            else:
                self.fail("Condition snapshot not found")

def run_tests():
    """Run all tests."""
    # Set up the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(ConditionArrayTest('test_empty_array_condition'))
    suite.addTest(ConditionArrayTest('test_non_empty_array_condition'))
    suite.addTest(ConditionArrayTest('test_complex_workflow_empty_array'))
    suite.addTest(ConditionArrayTest('test_complex_workflow_non_empty_array'))
    
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    print("Testing condition node handling of array types with is_empty/is_not_empty operators...")
    run_tests()