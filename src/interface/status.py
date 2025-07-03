"""
Status interfaces for the runtime.
This module contains the interfaces for status related types.
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
from enum import Enum


class StatusType(str, Enum):
    """
    Enum for status types.
    
    This enum represents the possible status types of a workflow or node.
    """
    Idle = "idle"
    Processing = "processing"
    Succeeded = "succeeded"
    Failed = "failed"
    Cancelled = "cancelled"


class IStatus(ABC):
    """
    Interface for status.
    
    A status represents the current state of a workflow or node.
    """
    
    @property
    @abstractmethod
    def status(self) -> str:
        """
        Get the status.
        
        Returns:
            The current status (e.g., 'idle', 'processing', 'succeeded', 'failed', 'cancelled').
        """
        pass
    
    @property
    @abstractmethod
    def terminated(self) -> bool:
        """
        Check if the status is terminated.
        
        Returns:
            True if the status is terminated (succeeded, failed, or cancelled), False otherwise.
        """
        pass
    
    @property
    @abstractmethod
    def start_time(self) -> int:
        """
        Get the start time.
        
        Returns:
            The start time in milliseconds since the Unix epoch.
        """
        pass
    
    @property
    @abstractmethod
    def end_time(self) -> Optional[int]:
        """
        Get the end time.
        
        Returns:
            The end time in milliseconds since the Unix epoch, or None if the status is not terminated.
        """
        pass
    
    @property
    @abstractmethod
    def time_cost(self) -> int:
        """
        Get the time cost.
        
        Returns:
            The time cost in milliseconds.
        """
        pass
    
    @abstractmethod
    def process(self) -> None:
        """
        Set the status to processing.
        """
        pass
    
    @abstractmethod
    def success(self) -> None:
        """
        Set the status to succeeded.
        """
        pass
    
    @abstractmethod
    def fail(self) -> None:
        """
        Set the status to failed.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Set the status to cancelled.
        """
        pass


class IWorkflowStatus(IStatus):
    """
    Interface for workflow status.
    
    A workflow status represents the current state of a workflow.
    """
    pass


class INodeStatus(IStatus):
    """
    Interface for node status.
    
    A node status represents the current state of a node.
    """
    pass


class IStatusCenter(ABC):
    """
    Interface for status center.
    
    The status center manages the status of the workflow and its nodes.
    """
    
    @property
    @abstractmethod
    def workflow(self) -> IWorkflowStatus:
        """
        Get the workflow status.
        
        Returns:
            The workflow status.
        """
        pass
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the status center.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the status center and release resources.
        """
        pass
    
    @abstractmethod
    def node_status(self, node_id: str) -> INodeStatus:
        """
        Get the status of a node.
        
        Args:
            node_id: The ID of the node.
            
        Returns:
            The status of the node.
        """
        pass
    
    @abstractmethod
    def export(self) -> Dict[str, Any]:
        """
        Export the status center.
        
        Returns:
            The exported status center data.
        """
        pass
