"""
Workflow application implementation.
This module provides the WorkflowApplication class which is the main entry point for running workflows.
"""
import logging
from typing import Dict, Optional, Any

from ..interface.engine import IEngine
from ..interface.task import ITask
from ..interface.context import IReport
from ..interface.schema import InvokeParams, WorkflowOutputs
from ..domain.container import WorkflowRuntimeContainer


class WorkflowApplication:
    """
    Main application class for running workflows.
    This class provides methods to run, cancel, and get reports and results from workflows.
    """
    # 单例模式实现
    _instance = None

    def __init__(self):
        """Initialize a new workflow application."""
        self.container = WorkflowRuntimeContainer.instance()
        self.tasks: Dict[str, ITask] = {}

    def run(self, params: InvokeParams) -> str:
        """
        Run a workflow with the given parameters.
        
        Args:
            params: The parameters to invoke the workflow with.
            
        Returns:
            The ID of the created task.
        """
        engine = self.container.get(IEngine)
        task = engine.invoke(params)
        self.tasks[task.id] = task
        logging.info(f"> POST TaskRun - taskID: {task.id}")
        logging.info(params.get("inputs"))
        
        # 使用回调函数处理任务完成
        def on_task_finished(output: Any) -> None:
            logging.info(f"> LOG Task finished: {task.id}")
            logging.info(output)
        
        task.on_complete(on_task_finished)
        
        return task.id

    def cancel(self, task_id: str) -> bool:
        """
        Cancel a running task.
        
        Args:
            task_id: The ID of the task to cancel.
            
        Returns:
            True if the task was found and cancelled, False otherwise.
        """
        logging.info(f"> PUT TaskCancel - taskID: {task_id}")
        task = self.tasks.get(task_id)
        if not task:
            return False
        task.cancel()
        return True

    def report(self, task_id: str) -> Optional[IReport]:
        """
        Get the report for a task.
        
        Args:
            task_id: The ID of the task to get the report for.
            
        Returns:
            The report for the task, or None if the task was not found.
        """
        task = self.tasks.get(task_id)
        logging.info(f"> GET TaskReport - taskID: {task_id}")
        if not task:
            return None
        return task.context.reporter.export()

    def result(self, task_id: str) -> Optional[WorkflowOutputs]:
        """
        Get the result of a task.
        
        Args:
            task_id: The ID of the task to get the result for.
            
        Returns:
            The outputs of the workflow, or None if the task was not found or not terminated.
        """
        logging.info(f"> GET TaskResult - taskID: {task_id}")
        task = self.tasks.get(task_id)
        if not task:
            return None
        if not task.context.status_center.workflow.terminated:
            return None
        return task.context.io_center.outputs

    @classmethod
    def instance(cls) -> 'WorkflowApplication':
        """
        Get the singleton instance of the workflow application.
        This is a class method to match the JavaScript static getter.
        
        Returns:
            The singleton instance of the workflow application.
        """
        if cls._instance is None:
            cls._instance = WorkflowApplication()
        return cls._instance
