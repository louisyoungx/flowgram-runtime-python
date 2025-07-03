"""
Implementation of the workflow runtime snapshot center.

This module contains the implementation of the snapshot center, which is responsible
for managing snapshots of the workflow execution. It provides methods to create,
export, and manage snapshots.
"""
from typing import Any, Dict, List

from ...interface.context import ISnapshotCenter, ISnapshot
from ...infrastructure.utils import uuid


class WorkflowRuntimeSnapshot(ISnapshot):
    """
    Implementation of the workflow snapshot.
    This class represents a snapshot of a node execution.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a new instance of the WorkflowRuntimeSnapshot class.
        
        Args:
            data: The snapshot data.
        """
        self.id = uuid()
        self.data = data

    def add_data(self, data: Dict[str, Any]) -> None:
        """
        Add data to the snapshot.
        
        Args:
            data: The data to add.
        """
        self.data.update(data)

    def validate(self) -> bool:
        """
        Validate the snapshot.
        
        Returns:
            True if the snapshot is valid, False otherwise.
        """
        required = ['nodeID', 'inputs', 'outputs', 'data']
        return all(key in self.data for key in required)

    def export(self) -> Dict[str, Any]:
        """
        Export the snapshot.
        
        Returns:
            The exported snapshot.
        """
        snapshot = {
            'id': self.id,
            **self.data
        }
        return snapshot

    @staticmethod
    def create(params: Dict[str, Any]) -> ISnapshot:
        """
        Create a new snapshot.
        
        Args:
            params: The snapshot parameters.
            
        Returns:
            The created snapshot.
        """
        # Convert node_id to nodeID for consistency with JS version
        if 'node_id' in params:
            params['nodeID'] = params.pop('node_id')
        return WorkflowRuntimeSnapshot(params)


class WorkflowRuntimeSnapshotCenter(ISnapshotCenter):
    """
    Implementation of the snapshot center.
    This class manages snapshots of the workflow execution.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeSnapshotCenter class.
        """
        self.id = uuid()
        self._snapshots: List[ISnapshot] = []

    def init(self) -> None:
        """
        Initialize the snapshot center.
        """
        self._snapshots = []

    def dispose(self) -> None:
        """
        Dispose the snapshot center and release resources.
        """
        # Because the data is not persisted, do not clear the execution result
        pass

    def create(self, snapshot_data: Dict[str, Any]) -> ISnapshot:
        """
        Create a snapshot with the given data.
        
        Args:
            snapshot_data: The snapshot data.
            
        Returns:
            The created snapshot.
        """
        snapshot = WorkflowRuntimeSnapshot.create(snapshot_data)
        self._snapshots.append(snapshot)
        return snapshot

    def export_all(self) -> List[Dict[str, Any]]:
        """
        Export all snapshots.
        
        Returns:
            A list of all snapshots.
        """
        return [snapshot.export() for snapshot in self._snapshots]

    def export(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Export snapshots grouped by node ID.
        
        Returns:
            A dictionary mapping node IDs to lists of snapshot data.
        """
        result: Dict[str, List[Dict[str, Any]]] = {}
        for snapshot in self.export_all():
            node_id = snapshot.get('nodeID', '')
            if node_id:
                if node_id not in result:
                    result[node_id] = []
                result[node_id].append(snapshot)
        return result
