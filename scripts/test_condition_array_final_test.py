import os
import sys
import unittest
import asyncio
from typing import Dict, Any, List

# Add the parent directory to the path to import from runtime-py-core
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# Define a simple workflow schema for testing array conditions
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
                        "array": {
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
                            "left": {"type": "ref", "content": ["start_0", "array"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_not_empty"
                    }
                ]
            }
        },
        {
            "id": "end_0",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 0}},
            "data": {
                "title": "End",
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
            "id": "end_1",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 300}},
            "data": {
                "title": "End",
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
        {"sourceNodeID": "condition_0", "targetNodeID": "end_0", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_1", "sourcePortID": "if_not_empty"}
    ]
}

# Define a complex workflow schema for testing array conditions in a real-world scenario
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
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": ""}
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
                            "systemPrompt": {"type": "constant", "content": "用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题，例如输入\"露营\"，返回\"在瑞士阿尔卑斯山的露营之旅\""},
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

class ConditionArrayTest(unittest.TestCase):
    """Test for condition node handling array types and is_empty/is_not_empty operators."""

    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_empty_array_condition(self):
        """Test condition node with empty array."""
        # Invoke the engine with an empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array": []
            }
        })
        
        # Check initial status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # Wait for the task to complete
        result = await task.processing
        
        # Verify final status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # Verify the result - should take the "is_empty" branch
        self.assertEqual(result, {"result": "数组为空"})
        
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
        # Invoke the engine with a non-empty array
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array": ["item1", "item2"]
            }
        })
        
        # Check initial status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # Wait for the task to complete
        result = await task.processing
        
        # Verify final status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # Verify the result - should take the "is_not_empty" branch
        self.assertEqual(result, {"result": "数组不为空"})
        
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
        # Invoke the engine with an empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            }
        })
        
        # Check initial status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # Wait for the task to complete
        await task.processing
        
        # Verify final status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # Verify the branch taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_Ts3zx":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot)
        self.assertEqual(condition_snapshot.branch, "if_OVHXT")  # Should take the "is_empty" branch

    async def test_complex_workflow_non_empty_array(self):
        """Test complex workflow with non-empty array."""
        # Invoke the engine with a non-empty themes array
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            }
        })
        
        # Check initial status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # Wait for the task to complete
        await task.processing
        
        # Verify final status
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # Verify the branch taken
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_Ts3zx":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot)
        self.assertEqual(condition_snapshot.branch, "if_pTr8_")  # Should take the "is_not_empty" branch

def run_async_test(test_case):
    """Run an async test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_case)
    finally:
        loop.close()

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(ConditionArrayTest("test_empty_array_condition"))
    test_suite.addTest(ConditionArrayTest("test_non_empty_array_condition"))
    test_suite.addTest(ConditionArrayTest("test_complex_workflow_empty_array"))
    test_suite.addTest(ConditionArrayTest("test_complex_workflow_non_empty_array"))
    
    # Run tests with custom runner that handles async tests
    for test in test_suite:
        # Create a fresh instance of the test class
        test_class = test.__class__()
        # Set up the test instance
        test_class.setUp()
        # Run the async test method
        test_method = getattr(test_class, test._testMethodName)
        run_async_test(test_method())
    
    print("All tests passed!")
