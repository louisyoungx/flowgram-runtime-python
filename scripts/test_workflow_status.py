import asyncio
import time
import sys
import os

# Add the runtime-py-core directory to the Python path
sys.path.append(os.path.abspath('runtime-py-core'))

from src.interface.schema import WorkflowStatus
from src.domain.status.workflow_runtime_status_center import WorkflowRuntimeStatusCenter

def test_workflow_status():
    """Test the workflow status values and transitions."""
    status_center = WorkflowRuntimeStatusCenter()
    
    # Test workflow status
    print("Initial workflow status:", status_center.workflow.status)
    
    # Process workflow
    status_center.workflow.process()
    print("After process() workflow status:", status_center.workflow.status)
    
    # Success workflow
    status_center.workflow.success()
    print("After success() workflow status:", status_center.workflow.status)
    
    # Check if workflow is terminated
    print("Is workflow terminated?", status_center.workflow.terminated)
    
    # Export workflow status
    workflow_export = status_center.workflow.export()
    print("Workflow export:", workflow_export)
    
    # Export status center
    status_center_export = status_center.export()
    print("Status center export:", status_center_export)
    
    # Test node status
    node_status = status_center.node_status("test_node")
    
    # Process node
    node_status.process()
    print("After process() node status:", node_status.status)
    
    # Success node
    node_status.success()
    print("After success() node status:", node_status.status)
    
    # Check if node is terminated
    print("Is node terminated?", node_status.terminated)
    
    # Export node status
    node_export = node_status.export()
    print("Node export:", node_export)
    
    # Export node statuses
    node_statuses_export = status_center.export_node_status()
    print("Node statuses export:", node_statuses_export)
    
    return status_center

if __name__ == "__main__":
    test_workflow_status()
