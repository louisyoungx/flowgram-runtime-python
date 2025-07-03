"""
Report interfaces for the runtime.
This module contains the interfaces for report related types.
"""
from typing import Any, Dict, List, Optional, TypedDict
from abc import ABC, abstractmethod


class INodeReport(TypedDict):
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


class IReport(TypedDict):
    """
    Report for a workflow.
    
    This represents the execution report for a workflow.
    """
    id: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    workflowStatus: Dict[str, Any]
    reports: Dict[str, INodeReport]


class IReporter(ABC):
    """
    Interface for reporter.
    
    The reporter generates reports of the workflow execution.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the reporter.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the reporter and release resources.
        """
        pass
    
    @abstractmethod
    def export(self) -> IReport:
        """
        Export the report.
        
        Returns:
            The exported report.
        """
        pass
    
    @abstractmethod
    def add_node_report(self, node_id: str, status: Dict[str, Any], snapshots: List[Dict[str, Any]]) -> None:
        """
        Add a node report.
        
        Args:
            node_id: The ID of the node.
            status: The status of the node.
            snapshots: The snapshots of the node execution.
        """
        pass
