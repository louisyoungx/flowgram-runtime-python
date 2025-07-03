"""
Implementation of the workflow runtime variable store.

The variable store manages variables used in the workflow. It provides methods to
get, set, check existence, and delete variables. The variable store also supports
a parent-child relationship, where a child variable store can inherit variables
from its parent. This is useful for creating sub-contexts that need access to
variables from their parent context, while also having their own isolated variable
scope.
"""
from typing import Any, Dict, List, Mapping, Optional, TypedDict, Union, cast

from ...interface.context import IVariableStore, IVariableParseResult
from ...interface.node import WorkflowVariableType
from ...infrastructure.utils import uuid, WorkflowRuntimeType


class IVariable(TypedDict, total=False):
    """Interface for a variable in the workflow runtime."""
    nodeID: str
    key: str
    value: Any
    type: WorkflowVariableType
    itemsType: Optional[WorkflowVariableType]


class WorkflowRuntimeVariable:
    """
    Implementation of the workflow runtime variable.
    This class represents a variable in the workflow runtime.
    """

    @staticmethod
    def create(params: IVariable) -> IVariable:
        """
        Create a new variable.
        
        Args:
            params: The variable parameters.
            
        Returns:
            The created variable.
        """
        return {
            "nodeID": params["nodeID"],
            "key": params["key"],
            "value": params["value"],
            "type": params["type"],
            "itemsType": params.get("itemsType")
        }


class WorkflowRuntimeVariableStore(IVariableStore):
    """
    Implementation of the variable store.
    This class provides storage and access to variables used in the workflow.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeVariableStore class.
        """
        self.id: str = uuid()
        self._parent: Optional[WorkflowRuntimeVariableStore] = None
        self.store: Dict[str, Dict[str, IVariable]] = {}

    def init(self) -> None:
        """
        Initialize the variable store.
        """
        self.store = {}

    def dispose(self) -> None:
        """
        Dispose the variable store and release resources.
        """
        self.store.clear()
        self._parent = None

    def set_parent(self, parent: IVariableStore) -> None:
        """
        Set the parent variable store.
        
        Args:
            parent: The parent variable store.
        """
        self._parent = cast(WorkflowRuntimeVariableStore, parent)

    def global_get(self, node_id: str) -> Optional[Dict[str, IVariable]]:
        """
        Get variables for a specific node from this store or its parent.
        
        Args:
            node_id: The node ID.
            
        Returns:
            The node's variable store, or None if not found.
        """
        store = self.store.get(node_id)
        if not store and self._parent:
            return self._parent.global_get(node_id)
        return store

    def set_variable(self, params: Dict[str, Any]) -> None:
        """
        Set a variable with type information.
        
        Args:
            params: The parameters containing nodeID, key, value, type, and optionally itemsType.
        """
        node_id = params["nodeID"]
        key = params["key"]
        value = params["value"]
        var_type = params["type"]
        items_type = params.get("itemsType")
        
        if node_id not in self.store:
            # Create node store
            self.store[node_id] = {}
        
        node_store = self.store[node_id]
        # Create variable store
        variable = WorkflowRuntimeVariable.create({
            "nodeID": node_id,
            "key": key,
            "value": value,
            "type": var_type,
            "itemsType": items_type
        })
        node_store[key] = variable

    def set_value(self, params: Dict[str, Any]) -> None:
        """
        Set a value in a variable, optionally at a specific path.
        
        Args:
            params: The parameters containing nodeID, variableKey, value, and optionally variablePath.
        """
        node_id = params["nodeID"]
        variable_key = params["variableKey"]
        variable_path = params.get("variablePath")
        value = params["value"]
        
        if node_id not in self.store:
            # Create node store
            self.store[node_id] = {}
        
        node_store = self.store[node_id]
        if variable_key not in node_store:
            # Create variable store
            variable = WorkflowRuntimeVariable.create({
                "nodeID": node_id,
                "key": variable_key,
                "value": {},
                "type": WorkflowVariableType.Object
            })
            node_store[variable_key] = variable
        
        variable = node_store[variable_key]
        if not variable_path:
            variable["value"] = value
            return
        
        # Set value at path
        current = variable["value"]
        for i, path_part in enumerate(variable_path):
            if i == len(variable_path) - 1:
                current[path_part] = value
            else:
                if path_part not in current or not isinstance(current[path_part], dict):
                    current[path_part] = {}
                current = current[path_part]

    def get_value(self, params: Dict[str, Any]) -> Optional[IVariableParseResult]:
        """
        Get a value from a variable, optionally at a specific path.
        
        Args:
            params: The parameters containing nodeID, variableKey, and optionally variablePath.
            
        Returns:
            The variable parse result, or None if not found.
        """
        node_id = params["nodeID"]
        variable_key = params["variableKey"]
        variable_path = params.get("variablePath")
        
        node_store = self.global_get(node_id)
        if not node_store or variable_key not in node_store:
            return None
        
        variable = node_store[variable_key]
        if not variable_path or len(variable_path) == 0:
            return {
                "value": variable["value"],
                "type": variable["type"],
                "itemsType": variable.get("itemsType")
            }
        
        # Get value at path
        current = variable["value"]
        for path_part in variable_path:
            if not isinstance(current, dict) or path_part not in current:
                return None
            current = current[path_part]
        
        var_type = WorkflowRuntimeType.get_workflow_type(current)
        if not var_type:
            return None
        
        if var_type == WorkflowVariableType.Array and isinstance(current, list) and len(current) > 0:
            items_type = WorkflowRuntimeType.get_workflow_type(current[0])
            if not items_type:
                return None
            return {
                "value": current,
                "type": var_type,
                "itemsType": items_type
            }
        
        return {
            "value": current,
            "type": var_type
        }

    # Legacy methods for backward compatibility
    def get(self, key: str) -> Any:
        """
        Get a variable by key (legacy method).
        
        Args:
            key: The variable key.
            
        Returns:
            The variable value.
        """
        # Assume variables are stored in a default node
        default_node = "default"
        node_store = self.global_get(default_node)
        if node_store and key in node_store:
            return node_store[key]["value"]
        
        if self._parent:
            return self._parent.get(key)
        
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a variable by key (legacy method).
        
        Args:
            key: The variable key.
            value: The variable value.
        """
        # Assume variables are stored in a default node
        default_node = "default"
        var_type = WorkflowRuntimeType.get_workflow_type(value)
        if not var_type:
            var_type = WorkflowVariableType.Object
        
        self.set_variable({
            "nodeID": default_node,
            "key": key,
            "value": value,
            "type": var_type
        })

    def has(self, key: str) -> bool:
        """
        Check if a variable exists (legacy method).
        
        Args:
            key: The variable key.
            
        Returns:
            True if the variable exists, False otherwise.
        """
        # Assume variables are stored in a default node
        default_node = "default"
        node_store = self.global_get(default_node)
        if node_store and key in node_store:
            return True
        
        if self._parent:
            return self._parent.has(key)
        
        return False

    def delete(self, key: str) -> None:
        """
        Delete a variable by key (legacy method).
        
        Args:
            key: The variable key.
        """
        # Assume variables are stored in a default node
        default_node = "default"
        if default_node in self.store and key in self.store[default_node]:
            del self.store[default_node][key]
            
    def has_variable(self, key: str, node_id: str = "default") -> bool:
        """
        Check if a variable exists in a specific node.
        
        Args:
            key: The variable key.
            node_id: The node ID. Defaults to "default".
            
        Returns:
            True if the variable exists, False otherwise.
        """
        # Check if the node exists in this store
        node_store = self.global_get(node_id)
        if node_store and key in node_store:
            return True
        
        # Check in parent store if not found
        if self._parent:
            return self._parent.has_variable(key, node_id)
        
        return False
        
    def get_variable(self, key: str, node_id: str = "default") -> Any:
        """
        Get a variable by key from a specific node.
        
        Args:
            key: The variable key.
            node_id: The node ID. Defaults to "default".
            
        Returns:
            The variable value.
        """
        # Get from this store
        node_store = self.global_get(node_id)
        if node_store and key in node_store:
            return node_store[key]["value"]
        
        # Get from parent store if not found
        if self._parent:
            return self._parent.get_variable(key, node_id)
        
        return None
