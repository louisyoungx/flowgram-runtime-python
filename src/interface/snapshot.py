"""
Snapshot interfaces for the runtime.
This module contains the interfaces for snapshot related types.
"""
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class ISnapshot(ABC):
    """
    Interface for snapshot.
    
    A snapshot represents the state of a node execution at a specific point in time.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the snapshot ID.
        
        Returns:
            The unique identifier of the snapshot.
        """
        pass
    
    @property
    @abstractmethod
    def node_id(self) -> str:
        """
        Get the node ID.
        
        Returns:
            The ID of the node that this snapshot belongs to.
        """
        pass
    
    @property
    @abstractmethod
    def inputs(self) -> Dict[str, Any]:
        """
        Get the inputs of the node at the time of the snapshot.
        
        Returns:
            The inputs of the node.
        """
        pass
    
    @property
    @abstractmethod
    def outputs(self) -> Optional[Dict[str, Any]]:
        """
        Get the outputs of the node at the time of the snapshot.
        
        Returns:
            The outputs of the node, or None if the node has not produced any outputs yet.
        """
        pass
    
    @property
    @abstractmethod
    def data(self) -> Dict[str, Any]:
        """
        Get the additional data of the snapshot.
        
        Returns:
            The additional data of the snapshot.
        """
        pass
    
    @property
    @abstractmethod
    def branch(self) -> Optional[str]:
        """
        Get the branch of the snapshot.
        
        Returns:
            The branch of the snapshot, or None if the snapshot is not associated with a branch.
        """
        pass
    
    @abstractmethod
    def add_data(self, data: Dict[str, Any]) -> None:
        """
        Add data to the snapshot.
        
        Args:
            data: The data to add.
        """
        pass


class ISnapshotCenter(ABC):
    """
    Interface for snapshot center.
    
    The snapshot center manages snapshots of the workflow execution.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the snapshot center.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the snapshot center and release resources.
        """
        pass
    
    @abstractmethod
    def create(self, params: Dict[str, Any]) -> ISnapshot:
        """
        Create a snapshot with the given parameters.
        
        Args:
            params: The snapshot parameters.
            
        Returns:
            The created snapshot.
        """
        pass
    
    @abstractmethod
    def export_all(self) -> List[ISnapshot]:
        """
        Export all snapshots.
        
        Returns:
            A list of all snapshots.
        """
        pass
    
    @abstractmethod
    def get_by_node_id(self, node_id: str) -> List[ISnapshot]:
        """
        Get snapshots by node ID.
        
        Args:
            node_id: The ID of the node.
            
        Returns:
            A list of snapshots for the specified node.
        """
        pass
