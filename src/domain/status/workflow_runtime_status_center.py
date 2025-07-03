"""
Implementation of the workflow runtime status center.

The status center manages the status of the workflow and its nodes. It provides
methods to get and update the status of the workflow and individual nodes. The
status can be one of the following:
- idle: The workflow or node is not yet started
- processing: The workflow or node is currently being processed
- success: The workflow or node has completed successfully
- failed: The workflow or node has failed
- cancelled: The workflow or node has been cancelled

The status center is used by the workflow engine to track the progress of the
workflow execution and to determine when the workflow has completed.
"""
from typing import Dict, List, Optional, Any
import time

from ...interface.context import IStatusCenter, IWorkflowStatus, INodeStatus
from ...interface.node import WorkflowStatus


class WorkflowRuntimeWorkflowStatus(IWorkflowStatus):
    """
    Implementation of the workflow status.
    This class manages the status of the workflow.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeWorkflowStatus class.
        """
        self._status = WorkflowStatus.Idle
        self._start_time = 0
        self._end_time = 0

    @property
    def status(self) -> str:
        """
        Get the current workflow status.
        
        Returns:
            The current workflow status.
        """
        return self._status

    @property
    def terminated(self) -> bool:
        """
        Check if the workflow is terminated.
        
        Returns:
            True if the workflow is terminated, False otherwise.
        """
        return self._status in [WorkflowStatus.Succeeded, WorkflowStatus.Failed, WorkflowStatus.Cancelled]
        
    @property
    def startTime(self) -> int:
        """
        Get the start time of the workflow.
        
        Returns:
            The start time in milliseconds.
        """
        return self._start_time
        
    @property
    def endTime(self) -> int:
        """
        Get the end time of the workflow.
        
        Returns:
            The end time in milliseconds.
        """
        return self._end_time
        
    @property
    def timeCost(self) -> int:
        """
        Get the time cost of the workflow.
        
        Returns:
            The time cost in milliseconds.
        """
        if self._end_time > 0 and self._start_time > 0:
            return self._end_time - self._start_time
        return 0
        
    def export(self) -> Dict[str, Any]:
        """
        Export the workflow status.
        
        Returns:
            A dictionary containing the workflow status information.
        """
        # Extract the status name from the enum
        status_str = self._status
        if hasattr(self._status, 'name'):
            status_str = self._status.name
        elif self._status and isinstance(self._status, str) and '.' in self._status:
            status_str = self._status.split('.')[-1]
            
        return {
            "status": status_str if self._status else "unknown",
            "terminated": self.terminated,
            "startTime": self._start_time,
            "endTime": self._end_time,
            "timeCost": self.timeCost
        }

    def process(self) -> None:
        """
        Set the workflow status to processing.
        """
        self._status = WorkflowStatus.Processing
        self._start_time = int(time.time() * 1000)  # Current time in milliseconds

    def success(self) -> None:
        """
        Set the workflow status to succeeded.
        """
        self._status = WorkflowStatus.Succeeded
        if self._end_time == 0:  # Only set end time if not already set
            self._end_time = int(time.time() * 1000)  # Current time in milliseconds

    def fail(self) -> None:
        """
        Set the workflow status to failed.
        """
        self._status = WorkflowStatus.Failed
        if self._end_time == 0:  # Only set end time if not already set
            self._end_time = int(time.time() * 1000)  # Current time in milliseconds

    def cancel(self) -> None:
        """
        Set the workflow status to cancelled.
        """
        self._status = WorkflowStatus.Cancelled
        if self._end_time == 0:  # Only set end time if not already set
            self._end_time = int(time.time() * 1000)  # Current time in milliseconds


class WorkflowRuntimeNodeStatus(INodeStatus):
    """
    Implementation of the node status.
    This class manages the status of a node.
    """

    def __init__(self, node_id: str):
        """
        Initialize a new instance of the WorkflowRuntimeNodeStatus class.
        
        Args:
            node_id: The ID of the node.
        """
        self._node_id = node_id
        self._status = WorkflowStatus.Idle
        self._start_time = 0
        self._end_time = 0
        self._start_time = int(time.time() * 1000)  # Current time in milliseconds
        
    @property
    def id(self) -> str:
        """
        Get the node ID.
        
        Returns:
            The node ID.
        """
        return self._node_id
        
    @property
    def status(self) -> str:
        """
        Get the current node status.
        
        Returns:
            The current node status.
        """
        return self._status
        
    @property
    def terminated(self) -> bool:
        """
        Check if the node is terminated.
        
        Returns:
            True if the node is terminated, False otherwise.
        """
        return self._status in [WorkflowStatus.Succeeded, WorkflowStatus.Failed, WorkflowStatus.Cancelled]
        
    @property
    def startTime(self) -> int:
        """
        Get the start time of the node.
        
        Returns:
            The start time in milliseconds.
        """
        return self._start_time
        
    @property
    def endTime(self) -> int:
        """
        Get the end time of the node.
        
        Returns:
            The end time in milliseconds.
        """
        return self._end_time
        
    @property
    def timeCost(self) -> int:
        """
        Get the time cost of the node.
        
        Returns:
            The time cost in milliseconds.
        """
        if self._end_time > 0 and self._start_time > 0:
            return self._end_time - self._start_time
        return 0
        
    def export(self) -> Dict[str, Any]:
        """
        Export the node status.
        
        Returns:
            A dictionary containing the node status information.
        """
        # Extract the status name from the enum
        status_str = self._status
        if hasattr(self._status, 'name'):
            status_str = self._status.name
        elif self._status and isinstance(self._status, str) and '.' in self._status:
            status_str = self._status.split('.')[-1]
            
        return {
            "id": self._node_id,
            "status": status_str if self._status else "unknown",
            "terminated": self.terminated,
            "startTime": self._start_time,
            "endTime": self._end_time,
            "timeCost": self.timeCost
        }

    def process(self) -> None:
        """
        Set the node status to processing.
        """
        self._status = WorkflowStatus.Processing
        self._start_time = int(time.time() * 1000)  # Update start time

    def success(self) -> None:
        """
        Set the node status to succeeded.
        """
        self._status = WorkflowStatus.Succeeded
        self._end_time = int(time.time() * 1000)  # Set end time

    def fail(self) -> None:
        """
        Set the node status to failed.
        """
        self._status = WorkflowStatus.Failed
        self._end_time = int(time.time() * 1000)  # Set end time

    def cancel(self) -> None:
        """
        Set the node status to cancelled.
        """
        self._status = WorkflowStatus.Cancelled
        self._end_time = int(time.time() * 1000)  # Set end time


class WorkflowRuntimeStatusCenter(IStatusCenter):
    """
    Implementation of the status center.
    This class manages the status of the workflow and nodes.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeStatusCenter class.
        """
        self._workflow_status: IWorkflowStatus = WorkflowRuntimeWorkflowStatus()
        self._node_statuses: Dict[str, INodeStatus] = {}
        import time
        self._workflow_status._start_time = int(time.time() * 1000)

    @property
    def workflow(self) -> IWorkflowStatus:
        """
        Get the workflow status.
        
        Returns:
            The workflow status.
        """
        return self._workflow_status

    def init(self) -> None:
        """
        Initialize the status center.
        """
        self._workflow_status = WorkflowRuntimeWorkflowStatus()
        self._node_statuses = {}

    def dispose(self) -> None:
        """
        Dispose the status center and release resources.
        """
        # Because the data is not persisted, do not clear the execution result
        pass

    def node_status(self, node_id: str) -> INodeStatus:
        """
        Get the status of a node.
        
        Args:
            node_id: The node ID.
            
        Returns:
            The node status.
        """
        if node_id not in self._node_statuses:
            self._node_statuses[node_id] = WorkflowRuntimeNodeStatus(node_id)
        return self._node_statuses[node_id]

    def get_status_node_ids(self, status: str) -> List[str]:
        """
        Get the IDs of nodes with the given status.
        
        Args:
            status: The status.
            
        Returns:
            The list of node IDs.
        """
        return [
            node_id
            for node_id, node_status in self._node_statuses.items()
            if node_status._status == status
        ]
    
    def export(self) -> Dict[str, Any]:
        """
        Export the status center data.

        Returns:
            The exported status center data.
        """
        return {
            "workflow": self.workflow.export() if hasattr(self.workflow, 'export') and callable(self.workflow.export) else {
                "status": getattr(self.workflow, '_status', "unknown"),
                "terminated": getattr(self.workflow, '_status', "") in [WorkflowStatus.Succeeded, WorkflowStatus.Failed, WorkflowStatus.Cancelled],
                "startTime": getattr(self.workflow, '_start_time', 0),
                "endTime": getattr(self.workflow, '_end_time', 0),
                "timeCost": getattr(self.workflow, '_end_time', 0) - getattr(self.workflow, '_start_time', 0) if getattr(self.workflow, '_end_time', 0) > 0 else 0
            },
            "nodes": self.export_node_status()
        }

    def export_node_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Export the status of all nodes.
        
        Returns:
            A dictionary mapping node IDs to node status information.
        """
        result = {}
        for node_id, node_status in self._node_statuses.items():
            if hasattr(node_status, 'export') and callable(node_status.export):
                result[node_id] = node_status.export()
            else:
                # Fallback if export method is not available
                result[node_id] = {
                    "id": node_id,
                    "status": getattr(node_status, '_status', "unknown"),
                    "terminated": getattr(node_status, '_status', "") in [WorkflowStatus.Succeeded, WorkflowStatus.Failed, WorkflowStatus.Cancelled],
                    "startTime": getattr(node_status, '_start_time', 0),
                    "endTime": getattr(node_status, '_end_time', 0),
                    "timeCost": getattr(node_status, '_end_time', 0) - getattr(node_status, '_start_time', 0) if getattr(node_status, '_end_time', 0) > 0 else 0
                }
        return result
