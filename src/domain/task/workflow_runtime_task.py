"""
Implementation of the workflow runtime task.
This module contains the implementation of the workflow runtime task.
"""
import asyncio
import logging
from typing import Any, Callable

from ...interface.context import IContext
from ...interface.task import ITask, TaskParams
from ...interface.schema import WorkflowOutputs, WorkflowStatus
from ...infrastructure.utils import uuid


class WorkflowRuntimeTask(ITask):
    """
    Implementation of the workflow runtime task.
    
    A task represents a running workflow instance. It provides methods to
    control the workflow execution and register callbacks for completion and error events.
    """
    
    def __init__(self, params: TaskParams):
        """
        Initialize a new workflow runtime task.
        
        Args:
            params: The parameters for creating the task.
        """
        self._id = uuid()
        
        # Handle both dictionary and TaskParams object
        if isinstance(params, dict):
            self._context = params["context"]
            self._processing = params["processing"]
        else:
            self._context = params.context
            self._processing = params.processing
            
        # Set task ID in context for later use in reporting
        if hasattr(self._context, '_task_id'):
            self._context._task_id = self._id
            
        self._complete_callbacks = []
        self._error_callbacks = []
        self._status = WorkflowStatus.Processing  # Initial status
        
        # Set up completion and error handling
        def handle_complete(result):
            # Update status based on workflow status
            if self._context.status_center.workflow.status == WorkflowStatus.Success:
                self._status = WorkflowStatus.Success
            elif self._context.status_center.workflow.status == WorkflowStatus.Failed:
                self._status = WorkflowStatus.Failed
            else:
                self._status = WorkflowStatus.Success  # Default to completed if workflow status is not set
                
            for callback in self._complete_callbacks:
                callback(result)
            return result
        
        def handle_error(error):
            self._status = WorkflowStatus.Failed
            for callback in self._error_callbacks:
                callback(error)
            raise error
        
        # Chain the processing promise with completion and error handlers
        self._processing_result = None
        try:
            # Handle different types of processing objects
            if asyncio.iscoroutine(self._processing):
                # If it's a coroutine object, we need to run it with asyncio
                self._processing_result = self._processing
                # Create a task to run the coroutine and update status when done
                async def run_coroutine():
                    try:
                        result = await self._processing
                        self._processing_result = result
                        # Ensure workflow status is updated to success when task completes
                        if not self._context.status_center.workflow.terminated:
                            self._context.status_center.workflow.success()
                        handle_complete(result)
                        return result
                    except Exception as e:
                        self._processing_result = e
                        # Ensure workflow status is updated to failed when task fails
                        self._context.status_center.workflow.fail()
                        handle_error(e)
                
                # Schedule the coroutine to run in the background
                asyncio.create_task(run_coroutine())
            elif callable(self._processing):
                # If it's a callable, call it
                try:
                    result = self._processing()
                    # If result is a coroutine, await it
                    if asyncio.iscoroutine(result):
                        async def handle_coroutine_result():
                            try:
                                final_result = await result
                                self._processing_result = final_result
                                # Ensure workflow status is updated to success when task completes
                                if not self._context.status_center.workflow.terminated:
                                    self._context.status_center.workflow.success()
                                handle_complete(final_result)
                                return final_result
                            except Exception as e:
                                self._processing_result = e
                                # Ensure workflow status is updated to failed when task fails
                                self._context.status_center.workflow.fail()
                                handle_error(e)
                        
                        asyncio.create_task(handle_coroutine_result())
                    else:
                        self._processing_result = result
                        if hasattr(result, 'then'):  # If it's a Promise-like object
                            result.then(lambda r: self._handle_promise_complete(r, handle_complete)).catch(lambda e: self._handle_promise_error(e, handle_error))
                        else:
                            # Ensure workflow status is updated to success for direct results
                            if not self._context.status_center.workflow.terminated:
                                self._context.status_center.workflow.success()
                            handle_complete(result)
                except Exception as e:
                    self._processing_result = e
                    # Ensure workflow status is updated to failed when task fails
                    self._context.status_center.workflow.fail()
                    handle_error(e)
            else:
                # If it's something else, just use it as is
                self._processing_result = self._processing
                # If it's a direct result, mark as completed
                # Ensure workflow status is updated to success for direct results
                if not self._context.status_center.workflow.terminated:
                    self._context.status_center.workflow.success()
                handle_complete(self._processing_result)
        except Exception as e:
            # Handle any unexpected errors during initialization
            self._processing_result = e
            self._context.status_center.workflow.fail()
            handle_error(e)
                
    def _handle_promise_complete(self, result: Any, callback: callable) -> Any:
        """
        Handle Promise completion and update workflow status.
        
        Args:
            result: The result of the Promise.
            callback: The callback to call with the result.
            
        Returns:
            The result.
        """
        self._processing_result = result
        # Ensure workflow status is updated to success
        if not self._context.status_center.workflow.terminated:
            self._context.status_center.workflow.success()
        callback(result)
        return result
        
    def _handle_promise_error(self, error: Exception, callback: callable) -> None:
        """
        Handle Promise error and update workflow status.
        
        Args:
            error: The error that occurred.
            callback: The callback to call with the error.
        """
        self._processing_result = error
        # Ensure workflow status is updated to failed
        self._context.status_center.workflow.fail()
        try:
            callback(error)
        except Exception as e:
            # Log the error but don't re-raise to avoid breaking the Promise chain
            logging.error(f"Error in Promise error callback: {e}")
    
    @property
    def id(self) -> str:
        """
        Get the task ID.
        
        Returns:
            The unique identifier of the task.
        """
        return self._id
    
    @property
    def status(self) -> str:
        """
        Get the task status.
        
        Returns:
            The current status of the task (e.g., 'processing', 'completed', 'failed', 'cancelled').
        """
        return self._status
    
    @property
    def context(self) -> IContext:
        """
        Get the task context.
        
        Returns:
            The context object associated with this task.
        """
        return self._context
    
    @property
    def processing(self) -> Any:
        """
        Get the processing promise.
        
        Returns:
            The promise that represents the task processing.
        """
        return self._processing_result
    
    def run(self) -> Any:
        """
        Run the task and return the result.
        
        Returns:
            The result of the task execution.
        """
        return self._processing_result
    
    def cancel(self) -> None:
        """
        Cancel the task execution.
        
        This method stops the workflow execution associated with this task.
        """
        self._status = WorkflowStatus.Cancelled
        self._context.status_center.workflow.cancel()
        cancel_node_ids = self._context.status_center.get_status_node_ids(WorkflowStatus.Processing)
        for node_id in cancel_node_ids:
            self._context.status_center.node_status(node_id).cancel()
    
    def on_complete(self, callback: Callable[[Any], None]) -> None:
        """
        Register a callback to be called when the task is completed.
        
        Args:
            callback: A function that takes the task result as an argument.
        """
        if self._status == WorkflowStatus.Success and self._processing_result:
            callback(self._processing_result)
        else:
            self._complete_callbacks.append(callback)
    
    def on_error(self, callback: Callable[[Exception], None]) -> None:
        """
        Register a callback to be called when the task encounters an error.
        
        Args:
            callback: A function that takes the exception as an argument.
        """
        if self._status == WorkflowStatus.Failed and isinstance(self._processing_result, Exception):
            callback(self._processing_result)
        else:
            self._error_callbacks.append(callback)
    
    @staticmethod
    def create(params: TaskParams) -> 'WorkflowRuntimeTask':
        """
        Create a new workflow runtime task.
        
        Args:
            params: The parameters for creating the task.
            
        Returns:
            A new workflow runtime task instance.
        """
        return WorkflowRuntimeTask(params)
