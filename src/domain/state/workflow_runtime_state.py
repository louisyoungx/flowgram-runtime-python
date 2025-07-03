"""
Implementation of the workflow runtime state.

The workflow state manages the execution state of the workflow. It tracks which
nodes have been executed, stores the outputs of each node, and provides methods
to get the inputs for a node based on its connections. It also provides methods
to parse references and values, which are used to resolve variables and node
outputs in the workflow.

The state works closely with the variable store to resolve references to variables
and with the document to resolve references to node outputs.
"""
from typing import Any, Dict, List, Optional

from ...interface.context import IState, IVariableStore
from ...interface.node import INode, WorkflowVariableType


class WorkflowRuntimeState(IState):
    """
    Implementation of the workflow state.
    This class manages the execution state of the workflow.
    """

    def __init__(self, variable_store: IVariableStore):
        """
        Initialize a new instance of the WorkflowRuntimeState class.
        
        Args:
            variable_store: The variable store to use.
        """
        self._variable_store = variable_store
        self._executed_nodes: List[INode] = []
        self._node_outputs: Dict[str, Dict[str, Any]] = {}

    def init(self) -> None:
        """
        Initialize the state.
        """
        self._executed_nodes = []
        self._node_outputs = {}

    def dispose(self) -> None:
        """
        Dispose the state and release resources.
        """
        self._executed_nodes = []
        self._node_outputs = {}

    def get_node_inputs(self, node: INode) -> Dict[str, Any]:
        """
        Get the inputs for a node.
        
        Args:
            node: The node.
            
        Returns:
            The node inputs.
        """
        inputs = {}
        
        # Get inputs from node data
        if "inputsValues" in node.data:
            input_values = node.data.get("inputsValues", {})
            
            for key, value_config in input_values.items():
                value_type = value_config.get("type")
                value_content = value_config.get("content")
                
                if value_type == "constant":
                    # Constant value
                    inputs[key] = value_content
                elif value_type == "ref" and isinstance(value_content, list):
                    # Reference to another node's output or variable
                    if len(value_content) >= 2:
                        node_id = value_content[0]
                        output_key = value_content[1]
                        
                        # Get from node outputs
                        if node_id in self._node_outputs and output_key in self._node_outputs[node_id]:
                            inputs[key] = self._node_outputs[node_id][output_key]
                        # Get from variable store with specific node_id (for loop locals or other node-specific variables)
                        elif self._variable_store.has_variable(output_key, node_id=node_id):
                            inputs[key] = self._variable_store.get_variable(output_key, node_id=node_id)
                        # Get from workflow inputs (start node)
                        elif node_id == "start_0" and self._variable_store.has_variable(output_key):
                            inputs[key] = self._variable_store.get_variable(output_key)
                        # Handle nested references (e.g., ["start_0", "llm_settings", "temperature"])
                        elif len(value_content) > 2:
                            # Try to get the parent object
                            parent_key = output_key
                            if self._variable_store.has_variable(parent_key, node_id=node_id):
                                parent_value = self._variable_store.get_variable(parent_key, node_id=node_id)
                                
                                # Navigate through nested keys
                                current_value = parent_value
                                for i in range(2, len(value_content)):
                                    nested_key = value_content[i]
                                    if isinstance(current_value, dict) and nested_key in current_value:
                                        current_value = current_value[nested_key]
                                    else:
                                        current_value = None
                                        break
                                
                                if current_value is not None:
                                    inputs[key] = current_value
        
        return inputs

    def set_node_outputs(self, node: INode, outputs: Dict[str, Any]) -> None:
        """
        Set the outputs for a node.
        
        Args:
            node: The node.
            outputs: The node outputs.
        """
        self._node_outputs[node.id] = outputs

    def add_executed_node(self, node: INode) -> None:
        """
        Add a node to the executed nodes list.
        
        Args:
            node: The node.
        """
        self._executed_nodes.append(node)

    def is_executed_node(self, node: INode) -> bool:
        """
        Check if a node has been executed.
        
        Args:
            node: The node.
            
        Returns:
            True if the node has been executed, False otherwise.
        """
        return node in self._executed_nodes

    def parse_ref(self, ref: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a reference.
        
        Args:
            ref: The reference object with type 'ref'.
            
        Returns:
            The parsed reference value and type, or None if the reference is invalid.
        """
        if not ref or ref.get("type") != "ref":
            raise ValueError(f"Invalid ref value: {ref}")
        
        content = ref.get("content", [])
        if not content or len(content) < 2:
            return None
        
        node_id = content[0]
        variable_key = content[1]
        variable_path = content[2:] if len(content) > 2 else []
        
        # Get the value from variable store
        if self._variable_store.has_variable(variable_key, node_id=node_id):
            value = self._variable_store.get_variable(variable_key, node_id=node_id)
            
            # Navigate through path if provided
            for path_item in variable_path:
                if isinstance(value, dict) and path_item in value:
                    value = value[path_item]
                else:
                    return None
            
            # Get the type of the value
            from ...infrastructure.utils.runtime_type import WorkflowRuntimeType
            value_type = WorkflowRuntimeType.get_workflow_type(value)
            
            if value_type:
                result = {
                    "value": value,
                    "type": value_type
                }
                
                # Add items_type for arrays
                if value_type == WorkflowVariableType.Array and isinstance(value, list):
                    # For empty arrays, set items_type to String by default
                    if len(value) == 0:
                        result["items_type"] = WorkflowVariableType.String
                    else:
                        first_item = value[0]
                        items_type = WorkflowRuntimeType.get_workflow_type(first_item)
                        if items_type:
                            result["items_type"] = items_type
                
                return result
        
        return None

    def parse_value(self, flow_value: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a flow value (constant or reference).
        
        Args:
            flow_value: The flow value object.
            
        Returns:
            The parsed value and type, or None if the value is invalid.
        """
        if not flow_value or not flow_value.get("type"):
            raise ValueError(f"Invalid flow value type: {flow_value}")
        
        # Handle constant values
        if flow_value["type"] == "constant":
            value = flow_value.get("content")
            
            # Import here to avoid circular imports
            from ...infrastructure.utils.runtime_type import WorkflowRuntimeType
            value_type = WorkflowRuntimeType.get_workflow_type(value)
            
            if value is None or not value_type:
                return None
                
            result = {
                "value": value,
                "type": value_type
            }
            
            # Add items_type for arrays
            if value_type == WorkflowVariableType.Array and isinstance(value, list):
                # For empty arrays, set items_type to String by default
                if len(value) == 0:
                    result["items_type"] = WorkflowVariableType.String
                else:
                    first_item = value[0]
                    items_type = WorkflowRuntimeType.get_workflow_type(first_item)
                    if items_type:
                        result["items_type"] = items_type
            
            return result
        
        # Handle reference values
        elif flow_value["type"] == "ref":
            return self.parse_ref(flow_value)
        
        # Unknown type
        else:
            raise ValueError(f"Unknown flow value type: {flow_value['type']}")
