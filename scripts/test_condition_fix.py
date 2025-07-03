"""
Test script for debugging and fixing condition node handling of array types.
"""
import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

# Add the current directory to the path so we can import from src
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer
from src.domain.state.workflow_runtime_state import WorkflowRuntimeState

# Test schema for empty array condition
EMPTY_ARRAY_SCHEMA = {
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
                        "array_value": {
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
                            "left": {"type": "ref", "content": ["start_0", "array_value"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array_value"]},
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

class ConditionArrayTest(unittest.TestCase):
    """Test condition node handling of array types."""

    def setUp(self):
        """Set up the test environment."""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    def test_parse_ref_with_empty_array(self):
        """Test that parse_ref correctly handles empty arrays."""
        # Create a state instance
        state = WorkflowRuntimeState()
        
        # Set up a variable store with an empty array
        state.variable_store.set("test_array", [])
        
        # Parse the reference
        result = state.parse_ref("test_array")
        
        # Check that the result has the correct type and items_type
        self.assertEqual(result.get("type"), "array")
        self.assertIn("items_type", result, "items_type should be present for empty arrays")
        
        # Set up a variable store with a non-empty array
        state.variable_store.set("test_array_non_empty", ["item1", "item2"])
        
        # Parse the reference
        result = state.parse_ref("test_array_non_empty")
        
        # Check that the result has the correct type and items_type
        self.assertEqual(result.get("type"), "array")
        self.assertIn("items_type", result)
        self.assertEqual(result.get("items_type"), "string")

    async def test_empty_array_condition(self):
        """Test condition node with empty array."""
        # Test with empty array
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_SCHEMA,
            "inputs": {
                "array_value": []
            }
        })
        
        # Wait for the task to complete
        result = await task.processing
        
        # Check that the result is correct
        self.assertEqual(result, {"result": "数组为空"})
        
        # Test with non-empty array
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_SCHEMA,
            "inputs": {
                "array_value": ["item1", "item2"]
            }
        })
        
        # Wait for the task to complete
        result = await task.processing
        
        # Check that the result is correct
        self.assertEqual(result, {"result": "数组不为空"})

def run_tests():
    """Run the tests."""
    # Run the parse_ref test
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ConditionArrayTest)
    unittest.TextTestRunner().run(test_suite)
    
    # Run the async test
    async def run_async_test():
        test = ConditionArrayTest()
        test.setUp()
        await test.test_empty_array_condition()
    
    asyncio.run(run_async_test())

if __name__ == "__main__":
    run_tests()