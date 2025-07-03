"""
Utility functions for handling snapshots in tests.
"""
from typing import List, Dict, Any, TypeVar, Generic

from ....interface.context import ISnapshot

T = TypeVar('T')

class VOData(Dict[str, Any]):
    """Value Object Data type."""
    pass


def snapshots_to_vo_data(snapshots: List[Dict[str, Any]]) -> List[VOData]:
    """
    Convert a list of snapshots to a list of value object data.
    
    Args:
        snapshots: The list of snapshots to convert. Can be either ISnapshot objects or dictionaries.
        
    Returns:
        A list of value object data.
    """
    result = []
    for snapshot in snapshots:
        if isinstance(snapshot, dict):
            # Handle dictionary input
            node_id = snapshot.get('nodeID', '')
            inputs = snapshot.get('inputs', {})
            outputs = snapshot.get('outputs', {})
            data = snapshot.get('data', {})
            branch = snapshot.get('branch', None)
        else:
            # Handle ISnapshot object input
            node_id = snapshot.node_id if hasattr(snapshot, 'node_id') else ''
            inputs = snapshot.inputs if hasattr(snapshot, 'inputs') else {}
            outputs = snapshot.outputs if hasattr(snapshot, 'outputs') else {}
            data = snapshot.data if hasattr(snapshot, 'data') else {}
            branch = snapshot.branch if hasattr(snapshot, 'branch') else None
        
        new_snapshot = VOData({
            "nodeID": node_id,
            "inputs": inputs,
            "outputs": outputs,
            "data": data,
        })
        
        # Always include branch field, even if it's None or empty
        new_snapshot["branch"] = branch
        
        result.append(new_snapshot)
    
    return result
