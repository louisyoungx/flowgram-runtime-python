"""
Task report API implementation.
This module provides the TaskReportAPI function for getting workflow task reports.
"""
import json
import logging
from typing import Any, Dict, Optional

from ..interface.schema import TaskReportInput
from ..interface.context import IReport
from ..application.workflow_application import WorkflowApplication


async def TaskReportAPI(input_data: TaskReportInput) -> Dict[str, Any]:
    """
    Get the report of a workflow task with the given input.
    
    Args:
        input_data: The input data containing the task ID.
        
    Returns:
        The report of the workflow task as a dictionary.
    """
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Get the task first to ensure we have access to the latest state
    task = app.tasks.get(task_id)
    
    # Create a default report structure
    report_dict = {
        "id": task_id,
        "inputs": {},
        "outputs": {},
        "workflowStatus": {
            "status": "processing",
            "terminated": False,
            "startTime": 0,
            "endTime": 0,
            "timeCost": 0
        },
        "reports": {}
    }
    
    # Get the report directly from the task context if available
    # This ensures we get the latest state
    if task and hasattr(task, 'context') and hasattr(task.context, 'reporter'):
        try:
            report_data = task.context.reporter.export()
            logging.info(f"Got report directly from task context for task {task_id}")
        except Exception as e:
            logging.error(f"Error getting report from task context: {e}")
            # Fall back to app.report if direct access fails
            report_data = app.report(task_id)
    else:
        # Fall back to app.report if task or context is not available
        report_data = app.report(task_id)
        
    # Always get the latest workflow status directly from the task
    if task and hasattr(task, 'context') and hasattr(task.context, 'status_center'):
        workflow_status = task.context.status_center.workflow
        if hasattr(workflow_status, 'export') and callable(workflow_status.export):
            status_dict = workflow_status.export()
            # Update the report with the latest status
            report_dict["workflowStatus"] = status_dict
            logging.info(f"Updated workflow status directly from task: {status_dict}")
    
    # Update with actual report data if available
    if report_data:
        # Always use the provided task ID for consistency
        report_dict["id"] = task_id
        
        # Get inputs, outputs, workflowStatus, and reports
        report_dict["inputs"] = getattr(report_data, "inputs", {}) or {}
        report_dict["outputs"] = getattr(report_data, "outputs", {}) or {}
        report_dict["workflowStatus"] = getattr(report_data, "workflowStatus", {}) or report_dict["workflowStatus"]
        report_dict["reports"] = getattr(report_data, "reports", {}) or {}
        
        # Normalize node status in reports to lowercase
        for node_id, node_report in report_dict["reports"].items():
            if "status" in node_report:
                status = node_report["status"]
                if status == "Success" or status == "Succeeded":
                    node_report["status"] = "succeeded"
                elif status == "Failure" or status == "Failed":
                    node_report["status"] = "failed"
                elif status == "Cancel" or status == "Cancelled":
                    node_report["status"] = "cancelled"
        
        # Try to get additional data directly from the task if available
        try:
            task = app.tasks.get(task_id)
            if task:
                # Update inputs from task context or start node snapshots if not already set
                if not report_dict["inputs"] or len(report_dict["inputs"]) == 0:
                    # First try to get inputs from io_center
                    if hasattr(task.context, "io_center"):
                        if hasattr(task.context.io_center, "inputs"):
                            report_dict["inputs"] = task.context.io_center.inputs
                        elif hasattr(task.context.io_center, "_inputs"):
                            report_dict["inputs"] = task.context.io_center._inputs
                    
                    # If still empty, try to get inputs from start_0 node snapshots
                    if not report_dict["inputs"] or len(report_dict["inputs"]) == 0:
                        if "reports" in report_dict and "start_0" in report_dict["reports"]:
                            start_node = report_dict["reports"]["start_0"]
                            if "snapshots" in start_node and len(start_node["snapshots"]) > 0:
                                for snapshot in start_node["snapshots"]:
                                    if "outputs" in snapshot and snapshot["outputs"]:
                                        report_dict["inputs"] = snapshot["outputs"]
                                        break
                
                # Update outputs from end node snapshots if not already set
                if not report_dict["outputs"] and "reports" in report_dict:
                    reports = report_dict["reports"]
                    if "end_0" in reports and "snapshots" in reports["end_0"]:
                        for snapshot in reports["end_0"]["snapshots"]:
                            if "outputs" in snapshot and snapshot["outputs"]:
                                report_dict["outputs"] = snapshot["outputs"]
                                break
                
                # Update workflowStatus from task context if available
                if hasattr(task.context, "status_center") and hasattr(task.context.status_center, "workflow"):
                    workflow_status = task.context.status_center.workflow
                    if hasattr(workflow_status, "export") and callable(workflow_status.export):
                        status_dict = workflow_status.export()
                        # Normalize status to lowercase "succeeded", "failed", or "cancelled"
                        status = status_dict.get("status", "")
                        if status == "success" or "Success" in status or status == "Succeeded":
                            status_dict["status"] = "succeeded"
                        elif status == "failure" or "Fail" in status or status == "Failed":
                            status_dict["status"] = "failed"
                        elif status == "cancel" or "Cancel" in status or status == "Cancelled":
                            status_dict["status"] = "cancelled"
                        report_dict["workflowStatus"] = status_dict
        except Exception as e:
            logging.error(f"Error getting additional data from task: {e}")
    
    # Log the output for debugging
    try:
        logging.info(f"> TaskReportAPI - output: {json.dumps(report_dict)}")
    except Exception as e:
        logging.error(f"> TaskReportAPI - error: {str(e)}")
        logging.info(f"> TaskReportAPI - output: {report_dict}")
    
    return report_dict
