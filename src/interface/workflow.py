"""
Workflow interfaces for the runtime.
This module contains the interfaces for workflow related types.
"""
from typing import Any, Dict, List, Optional, Union, TypedDict
from abc import ABC, abstractmethod
from enum import Enum


class WorkflowInputs(TypedDict):
    """
    Inputs for a workflow.
    
    This represents the input data provided to a workflow when it starts.
    """
    pass


class WorkflowOutputs(TypedDict):
    """
    Outputs from a workflow.
    
    This represents the output data produced by a workflow when it completes.
    """
    pass


class WorkflowStatusType(str, Enum):
    """
    Enum for workflow status types.
    
    This enum represents the possible status types of a workflow.
    """
    Idle = "idle"
    Processing = "processing"
    Succeeded = "succeeded"
    Failed = "failed"
    Cancelled = "cancelled"


class WorkflowStatus(TypedDict):
    """
    Status of a workflow.
    
    This represents the current status of a workflow execution.
    """
    status: str
    terminated: bool
    startTime: int
    endTime: Optional[int]
    timeCost: int


class NodeReport(TypedDict):
    """
    Report for a node.
    
    This represents the execution report for a single node in the workflow.
    """
    id: str
    status: str
    terminated: bool
    startTime: int
    endTime: Optional[int]
    timeCost: int
    snapshots: List[Dict[str, Any]]


class IWorkflow(ABC):
    """
    Interface for workflow.
    
    A workflow represents a process flow with nodes and edges.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the workflow ID.
        
        Returns:
            The unique identifier of the workflow.
        """
        pass
    
    @property
    @abstractmethod
    def inputs(self) -> WorkflowInputs:
        """
        Get the workflow inputs.
        
        Returns:
            The inputs provided to the workflow.
        """
        pass
    
    @property
    @abstractmethod
    def outputs(self) -> WorkflowOutputs:
        """
        Get the workflow outputs.
        
        Returns:
            The outputs produced by the workflow.
        """
        pass
    
    @property
    @abstractmethod
    def status(self) -> WorkflowStatus:
        """
        Get the workflow status.
        
        Returns:
            The current status of the workflow.
        """
        pass
    
    @abstractmethod
    def execute(self) -> None:
        """
        Execute the workflow.
        
        This method starts the execution of the workflow.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Cancel the workflow execution.
        
        This method stops the execution of the workflow.
        """
        pass
