"""
API module for the workflow runtime.
This module provides the API functions for the workflow runtime.
"""
from typing import Any, Callable, Dict

from ..interface.schema import FlowGramAPIName
from .task_run_api import TaskRunAPI
from .task_result_api import TaskResultAPI
from .task_report_api import TaskReportAPI
from .task_cancel_api import TaskCancelAPI

__all__ = ['TaskRunAPI', 'TaskResultAPI', 'TaskReportAPI', 'TaskCancelAPI', 'WorkflowRuntimeAPIs']

# Dictionary mapping API names to API functions
WorkflowRuntimeAPIs: Dict[FlowGramAPIName, Callable[[Any], Any]] = {
    FlowGramAPIName.TaskRun: TaskRunAPI,
    FlowGramAPIName.TaskReport: TaskReportAPI,
    FlowGramAPIName.TaskResult: TaskResultAPI,
    FlowGramAPIName.TaskCancel: TaskCancelAPI,
    FlowGramAPIName.ServerInfo: lambda _: None,  # TODO
    FlowGramAPIName.Validation: lambda _: None,  # TODO
}