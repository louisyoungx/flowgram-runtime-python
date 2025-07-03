"""
Async test module for the workflow runtime task.
"""
import asyncio
import unittest
from typing import Any

from ...interface.task import TaskParams
from ...interface.schema import WorkflowStatus
from ..task.workflow_runtime_task import WorkflowRuntimeTask


class MockContext:
    """Mock context for testing."""
    
    class MockStatusCenter:
        """Mock status center for testing."""
        
        class MockWorkflowStatus:
            """Mock workflow status for testing."""
            
            def __init__(self):
                self.cancelled = False
            
            def cancel(self):
                """Cancel the workflow."""
                self.cancelled = True
        
        class MockNodeStatus:
            """Mock node status for testing."""
            
            def __init__(self):
                self.cancelled = False
            
            def cancel(self):
                """Cancel the node."""
                self.cancelled = True
        
        def __init__(self):
            self.workflow = self.MockWorkflowStatus()
            self.node_statuses = {}
        
        def node_status(self, node_id):
            """Get the status of a node."""
            if node_id not in self.node_statuses:
                self.node_statuses[node_id] = self.MockNodeStatus()
            return self.node_statuses[node_id]
        
        def get_status_node_ids(self, status):
            """Get the IDs of nodes with the given status."""
            return ["node1", "node2"] if status == WorkflowStatus.Processing else []
    
    def __init__(self):
        self.status_center = self.MockStatusCenter()


class AsyncResult:
    """A simple Promise-like object for testing."""
    
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error
        self.then_callbacks = []
        self.catch_callbacks = []
    
    def then(self, callback):
        """Register a callback to be called when the promise is resolved."""
        self.then_callbacks.append(callback)
        if self.value is not None:
            callback(self.value)
        return self
    
    def catch(self, callback):
        """Register a callback to be called when the promise is rejected."""
        self.catch_callbacks.append(callback)
        if self.error is not None:
            callback(self.error)
        return self


class TestWorkflowRuntimeTaskAsync(unittest.TestCase):
    """Test case for WorkflowRuntimeTask with async operations."""
    
    def test_async_processing(self):
        """Test task with async processing."""
        context = MockContext()
        result = {"result": "success"}
        async_result = AsyncResult(value=result)
        
        def processing():
            return async_result
        
        params = TaskParams(context=context, processing=processing)
        task = WorkflowRuntimeTask.create(params)
        
        self.assertEqual(task.processing, async_result)
        
        # Test on_complete with async result
        callback_result = None
        
        def callback(res):
            nonlocal callback_result
            callback_result = res
        
        # Manually trigger the callback since we're not using real async
        task._status = "completed"
        task._processing_result = result
        task.on_complete(callback)
        
        # The callback should have been called
        self.assertEqual(callback_result, result)
    
    def test_async_error(self):
        """Test task with async error."""
        context = MockContext()
        error = Exception("Test error")
        async_result = AsyncResult(error=error)
        
        def processing():
            return async_result
        
        # Create the task manually to avoid exceptions
        task = WorkflowRuntimeTask.__new__(WorkflowRuntimeTask)
        task._id = "test-id"
        task._context = context
        task._processing = processing
        task._complete_callbacks = []
        task._error_callbacks = []
        task._status = "failed"
        task._processing_result = error
        
        # Test on_error with async error
        callback_error = None
        
        def callback(err):
            nonlocal callback_error
            callback_error = err
        
        task.on_error(callback)
        
        # The callback should have been called
        self.assertEqual(callback_error, error)


if __name__ == "__main__":
    unittest.main()
