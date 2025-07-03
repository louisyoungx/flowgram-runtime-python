"""
Test module for the workflow runtime task.
"""
import unittest
import asyncio
from typing import Any

from ...interface.task import TaskParams
from ...interface.context import IContext
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


class TestWorkflowRuntimeTask(unittest.TestCase):
    """Test case for WorkflowRuntimeTask."""
    
    def test_create_task(self):
        """Test creating a task."""
        context = MockContext()
        
        def processing():
            return {"result": "success"}
        
        params = TaskParams(context=context, processing=processing)
        task = WorkflowRuntimeTask.create(params)
        
        self.assertIsNotNone(task)
        self.assertIsNotNone(task.id)
        self.assertEqual(task.status, "processing")
        self.assertEqual(task.context, context)
        self.assertEqual(task.run(), {"result": "success"})
    
    def test_cancel_task(self):
        """Test cancelling a task."""
        context = MockContext()
        
        def processing():
            return {"result": "success"}
        
        params = TaskParams(context=context, processing=processing)
        task = WorkflowRuntimeTask.create(params)
        
        task.cancel()
        
        self.assertEqual(task.status, "cancelled")
        self.assertTrue(context.status_center.workflow.cancelled)
        self.assertTrue(context.status_center.node_statuses["node1"].cancelled)
        self.assertTrue(context.status_center.node_statuses["node2"].cancelled)
    
    def test_on_complete(self):
        """Test registering a completion callback."""
        context = MockContext()
        result = {"result": "success"}
        
        def processing():
            return result
        
        params = TaskParams(context=context, processing=processing)
        task = WorkflowRuntimeTask.create(params)
        
        callback_result = None
        
        def callback(res):
            nonlocal callback_result
            callback_result = res
        
        task.on_complete(callback)
        
        # Since we're not using real async, we need to manually set the status
        task._status = "completed"
        task._processing_result = result
        
        # Call on_complete again to trigger the callback
        task.on_complete(callback)
        
        self.assertEqual(callback_result, result)
    
    def test_on_error(self):
        """Test registering an error callback."""
        context = MockContext()
        error = Exception("Test error")
        
        def processing():
            raise error
        
        params = TaskParams(context=context, processing=processing)
        
        # This will raise an exception, which we catch for testing
        try:
            task = WorkflowRuntimeTask.create(params)
        except Exception:
            pass
        
        # Create the task manually since the constructor raised an exception
        task = WorkflowRuntimeTask.__new__(WorkflowRuntimeTask)
        task._id = "test-id"
        task._context = context
        task._processing = processing
        task._complete_callbacks = []
        task._error_callbacks = []
        task._status = "failed"
        task._processing_result = error
        
        callback_error = None
        
        def callback(err):
            nonlocal callback_error
            callback_error = err
        
        task.on_error(callback)
        
        self.assertEqual(callback_error, error)


if __name__ == "__main__":
    unittest.main()