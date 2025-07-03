"""
Test WorkflowRuntimeTask with async processing.
"""
import asyncio
import logging
from src.domain.task.workflow_runtime_task import WorkflowRuntimeTask
from src.interface.schema import WorkflowStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockContext:
    """Mock context for testing."""
    
    class MockStatusCenter:
        """Mock status center."""
        
        class MockWorkflowStatus:
            """Mock workflow status."""
            
            def __init__(self):
                self.status = WorkflowStatus.Processing
                
            def success(self):
                """Mark as success."""
                self.status = WorkflowStatus.Success
                
            def fail(self):
                """Mark as failed."""
                self.status = WorkflowStatus.Failed
                
            def cancel(self):
                """Mark as cancelled."""
                self.status = WorkflowStatus.Cancelled
        
        def __init__(self):
            self.workflow = self.MockWorkflowStatus()
            self._node_statuses = {}
            
        def node_status(self, node_id):
            """Get node status."""
            if node_id not in self._node_statuses:
                self._node_statuses[node_id] = self.MockWorkflowStatus()
            return self._node_statuses[node_id]
            
        def get_status_node_ids(self, status):
            """Get node IDs with the given status."""
            return [node_id for node_id, node_status in self._node_statuses.items() 
                   if node_status.status == status]
    
    def __init__(self):
        self.status_center = self.MockStatusCenter()
        self._task_id = None

async def test_workflow_task_async():
    """Test WorkflowRuntimeTask with async processing."""
    # Create a mock context
    context = MockContext()
    
    # Create an async processing function
    async def async_processing():
        logger.info("Starting async processing...")
        await asyncio.sleep(1)  # Simulate some async work
        logger.info("Async processing completed")
        context.status_center.workflow.success()  # Mark workflow as success
        return {"result": "success"}
    
    # Create a task with async processing
    task = WorkflowRuntimeTask({
        "context": context,
        "processing": async_processing()
    })
    
    # Check initial status
    logger.info(f"Initial task status: {task.status}")
    logger.info(f"Initial workflow status: {context.status_center.workflow.status}")
    
    # Wait a bit to allow processing to complete
    logger.info("Waiting for processing to complete...")
    await asyncio.sleep(2)
    
    # Check final status
    logger.info(f"Final task status: {task.status}")
    logger.info(f"Final workflow status: {context.status_center.workflow.status}")
    
    # Check result
    logger.info(f"Task result: {task.processing}")
    
    # Test on_complete callback
    def on_complete_callback(result):
        logger.info(f"on_complete callback called with result: {result}")
    
    task.on_complete(on_complete_callback)
    
    return task

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_workflow_task_async())