"""
Engine interfaces for the workflow runtime.
This module contains the interfaces for the workflow runtime engine.
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from .task import ITask
from .schema import InvokeParams


class IEngine(ABC):
    """
    Interface for the workflow runtime engine.
    
    The engine is responsible for invoking workflows and managing their execution.
    It provides methods to invoke a workflow with parameters and cancel running workflows.
    """
    
    @abstractmethod
    def invoke(self, params: InvokeParams) -> ITask:
        """
        Invoke a workflow with the given parameters.
        
        Args:
            params: The parameters for invoking the workflow.
            
        Returns:
            A task object representing the running workflow.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Cancel the current workflow execution.
        
        This method stops all running workflows managed by this engine.
        """
        pass
