"""
Tests for node executors.
This module contains tests for all node executors.
"""
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio

from src.interface.executor import ExecutionContext, ExecutionResult
from src.interface.node import FlowGramNode, WorkflowVariableType
from src.nodes.start.start_executor import StartExecutor
from src.nodes.end.end_executor import EndExecutor
from src.nodes.llm.llm_executor import LLMExecutor
from src.nodes.condition.condition_executor import ConditionExecutor
from src.nodes.loop.loop_executor import LoopExecutor


class TestNodeExecutors(unittest.TestCase):
    """Test cases for node executors."""
    
    def test_start_executor_type(self):
        """Test that the start executor has the correct type."""
        executor = StartExecutor()
        self.assertEqual(executor.type, FlowGramNode.Start)
    
    def test_end_executor_type(self):
        """Test that the end executor has the correct type."""
        executor = EndExecutor()
        self.assertEqual(executor.type, FlowGramNode.End)
    
    def test_llm_executor_type(self):
        """Test that the LLM executor has the correct type."""
        executor = LLMExecutor()
        self.assertEqual(executor.type, FlowGramNode.LLM)
    
    def test_condition_executor_type(self):
        """Test that the condition executor has the correct type."""
        executor = ConditionExecutor()
        self.assertEqual(executor.type, FlowGramNode.Condition)
    
    def test_loop_executor_type(self):
        """Test that the loop executor has the correct type."""
        executor = LoopExecutor()
        self.assertEqual(executor.type, FlowGramNode.Loop)
    
    async def async_test_start_executor_execute(self):
        """Test that the start executor executes correctly."""
        executor = StartExecutor()
        
        # Mock the execution context
        context = MagicMock()
        context.runtime.io_center.inputs = {"test": "value"}
        
        # Execute the start node
        result = await executor.execute(context)
        
        # Check the result
        self.assertEqual(result.outputs, {"test": "value"})
        self.assertIsNone(result.branch)
    
    async def async_test_end_executor_execute(self):
        """Test that the end executor executes correctly."""
        executor = EndExecutor()
        
        # Mock the execution context
        context = MagicMock()
        context.inputs = {"test": "value"}
        
        # Execute the end node
        result = await executor.execute(context)
        
        # Check the result
        self.assertEqual(result.outputs, {"test": "value"})
        self.assertIsNone(result.branch)
        context.runtime.io_center.set_outputs.assert_called_once_with({"test": "value"})
    
    async def async_test_llm_executor_execute(self):
        """Test that the LLM executor executes correctly."""
        executor = LLMExecutor()
        
        # Mock the execution context
        context = MagicMock()
        context.inputs = {
            "modelName": "test-model",
            "temperature": 0.7,
            "apiKey": "test-api-key",
            "apiHost": "https://test-api-host",
            "prompt": "Hello, world!"
        }
        
        # Mock the ChatOpenAI class
        with patch("langchain_openai.ChatOpenAI") as mock_chat_openai:
            # Mock the invoke method
            mock_instance = mock_chat_openai.return_value
            mock_instance.ainvoke = AsyncMock()
            mock_instance.ainvoke.return_value.content = "Hello, human!"
            
            # Execute the LLM node
            result = await executor.execute(context)
            
            # Check the result
            self.assertEqual(result.outputs, {"result": "Hello, human!"})
            self.assertIsNone(result.branch)
            
            # Check that the ChatOpenAI class was called with the correct arguments
            mock_chat_openai.assert_called_once_with(
                model_name="test-model",
                temperature=0.7,
                api_key="test-api-key",
                openai_api_base="https://test-api-host"
            )
    
    async def async_test_condition_executor_execute(self):
        """Test that the condition executor executes correctly."""
        executor = ConditionExecutor()
        
        # Mock the execution context
        context = MagicMock()
        context.node.data = {
            "conditions": [
                {
                    "key": "true_branch",
                    "value": {
                        "left": {"type": "ref", "value": "test_var"},
                        "operator": "eq",
                        "right": {"type": "constant", "value": "test_value"}
                    }
                }
            ]
        }
        
        # Mock the state.parse_ref method
        context.runtime.state.parse_ref.return_value = {
            "value": "test_value",
            "type": WorkflowVariableType.String
        }
        
        # Mock the state.parse_value method
        context.runtime.state.parse_value.return_value = {
            "value": "test_value",
            "type": WorkflowVariableType.String
        }
        
        # Execute the condition node
        result = await executor.execute(context)
        
        # Check the result
        self.assertEqual(result.outputs, {})
        self.assertEqual(result.branch, "true_branch")
    
    async def async_test_loop_executor_execute(self):
        """Test that the loop executor executes correctly."""
        executor = LoopExecutor()
        
        # Mock the execution context
        context = MagicMock()
        context.node.id = "test_node"
        context.node.data = {"batchFor": {"type": "ref", "value": "test_array"}}
        context.node.children = [MagicMock()]
        context.node.children[0].prev = []
        
        # Mock the state.parse_ref method
        context.runtime.state.parse_ref.return_value = {
            "value": ["item1", "item2", "item3"],
            "type": WorkflowVariableType.Array,
            "items_type": WorkflowVariableType.String
        }
        
        # Mock the container.get method
        engine = MagicMock()
        engine.execute_node = AsyncMock()
        context.container.get.return_value = engine
        
        # Mock the runtime.sub method
        sub_context = MagicMock()
        context.runtime.sub.return_value = sub_context
        
        # Execute the loop node
        result = await executor.execute(context)
        
        # Check the result
        self.assertEqual(result.outputs, {})
        self.assertIsNone(result.branch)
        
        # Check that the sub context was created for each item
        self.assertEqual(context.runtime.sub.call_count, 3)
        
        # Check that the variable was set for each item
        self.assertEqual(sub_context.variable_store.set_variable.call_count, 3)
        
        # Check that the engine.execute_node was called for each item
        self.assertEqual(engine.execute_node.call_count, 3)


def run_async_test(test_func):
    """Run an async test function."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_func())


if __name__ == "__main__":
    # Run the async tests
    test_case = TestNodeExecutors()
    run_async_test(test_case.async_test_start_executor_execute)
    run_async_test(test_case.async_test_end_executor_execute)
    run_async_test(test_case.async_test_llm_executor_execute)
    run_async_test(test_case.async_test_condition_executor_execute)
    run_async_test(test_case.async_test_loop_executor_execute)
    
    # Run the sync tests
    unittest.main()
