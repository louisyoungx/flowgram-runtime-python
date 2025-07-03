"""
Implementation of the workflow runtime reporter.

This module contains the implementation of the reporter, which is responsible
for generating reports about the workflow execution. It collects data from
the workflow context and generates a report that can be used for debugging,
monitoring, and analysis purposes.
"""
from typing import Dict, Any

from ...interface.context import IReporter, IReport, IIOCenter, ISnapshotCenter, IStatusCenter
from ...infrastructure.utils import uuid


class WorkflowRuntimeReport(IReport):
    """
    Implementation of the workflow runtime report.
    This class represents a report about the workflow execution.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a new instance of the WorkflowRuntimeReport class.
        
        Args:
            data: The report data.
        """
        self.id = data.get("id", "workflow-report")
        self.inputs = data.get("inputs", {})
        self.outputs = data.get("outputs", {})
        self.workflowStatus = data.get("workflowStatus", {})
        self.reports = data.get("reports", {})


class WorkflowRuntimeReporter(IReporter):
    """
    Implementation of the workflow runtime reporter.
    This class is responsible for generating reports about the workflow execution.
    """

    def __init__(self, io_center: IIOCenter, snapshot_center: ISnapshotCenter, status_center: IStatusCenter):
        """
        Initialize a new instance of the WorkflowRuntimeReporter class.
        
        Args:
            io_center: The IO center.
            snapshot_center: The snapshot center.
            status_center: The status center.
        """
        self._io_center = io_center
        self._snapshot_center = snapshot_center
        self._status_center = status_center

    def init(self) -> None:
        """
        Initialize the reporter.
        """
        pass

    def dispose(self) -> None:
        """
        Dispose the reporter and release resources.
        """
        pass

    def export(self) -> IReport:
        """
        Export the report.
        
        Returns:
            The exported report.
        """
        # Get workflow status
        workflow_status = self._status_center.workflow
        
        # Get all node statuses
        status_data = self._status_center.export()
        node_statuses = status_data.get("nodes", {})
        
        # Get all snapshots
        snapshots_by_node = self._snapshot_center.export()
        
        # Create node reports
        reports = {}
        for node_id, node_status in node_statuses.items():
            node_snapshots = snapshots_by_node.get(node_id, [])
            
            reports[node_id] = {
                "id": node_id,
                "status": node_status.get("status", "unknown"),
                "terminated": node_status.get("terminated", False),
                "startTime": node_status.get("startTime", 0),
                "endTime": node_status.get("endTime", 0),
                "timeCost": node_status.get("timeCost", 0),
                "snapshots": node_snapshots
            }
        
        # Create the report data
        task_id = "workflow-report"
        if hasattr(self._io_center, '_context') and hasattr(self._io_center._context, '_task_id'):
            task_id = self._io_center._context._task_id
        
        report_data = {
            "id": task_id,
            "inputs": self._io_center.inputs,
            "outputs": self._io_center.outputs,
            "workflowStatus": {
                "status": workflow_status.status,
                "terminated": workflow_status.terminated,
                "startTime": workflow_status.startTime,
                "endTime": workflow_status.endTime,
                "timeCost": workflow_status.timeCost
            },
            "reports": reports
        }
        
        return WorkflowRuntimeReport(report_data)
