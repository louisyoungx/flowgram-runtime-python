"""
Task interfaces for the workflow runtime.
This module contains the interfaces for workflow runtime tasks.
"""
from typing import Any, Dict, Optional, Callable
from abc import ABC, abstractmethod


class ITask(ABC):
    """
    Interface for workflow runtime tasks.
    
    A task represents a running workflow instance. It provides methods to
    control the workflow execution and register callbacks for completion and error events.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the task ID.
        
        Returns:
            The unique identifier of the task.
        """
        pass
    
    @property
    @abstractmethod
    def status(self) -> str:
        """
        Get the task status.
        
        Returns:
            The current status of the task (e.g., 'running', 'completed', 'failed', 'cancelled').
        """
        pass
    
    @property
    @abstractmethod
    def context(self) -> 'IContext':
        """
        Get the task context.
        
        Returns:
            The context object associated with this task.
        """
        pass
    
    @abstractmethod
    def run(self) -> Any:
        """
        Run the task and return the result.
        
        Returns:
            The result of the task execution.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Cancel the task execution.
        
        This method stops the workflow execution associated with this task.
        """
        pass
    
    @abstractmethod
    def on_complete(self, callback: Callable[[Any], None]) -> None:
        """
        Register a callback to be called when the task is completed.
        
        Args:
            callback: A function that takes the task result as an argument.
        """
        pass
    
    @abstractmethod
    def on_error(self, callback: Callable[[Exception], None]) -> None:
        """
        Register a callback to be called when the task encounters an error.
        
        Args:
            callback: A function that takes the exception as an argument.
        """
        pass


class TaskParams:
    """
    Parameters for creating a task.
    
    This class represents the parameters needed to create a workflow runtime task.
    """
    
    def __init__(self, context: 'IContext', processing: Callable[[], Any]):
        """
        Initialize task parameters.
        
        Args:
            context: The context object for the task.
            processing: The function that processes the task.
        """
        self.context = context
        self.processing = processing


# Forward reference for IContext
from .context import IContext
