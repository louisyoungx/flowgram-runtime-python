"""
Implementation of the workflow runtime document.

The workflow document represents the workflow definition, including nodes and edges.
It is responsible for parsing the workflow schema and providing access to the nodes
and edges of the workflow. The document is initialized with a schema that defines
the structure of the workflow, including the nodes, their configurations, and the
connections between them.
"""
from typing import Any, Dict, Optional, List, Set

from ...interface.context import IDocument
from ...interface.node import INode, FlowGramNode
from .node import Node, Port, Edge


class WorkflowRuntimeDocument(IDocument):
    """
    Implementation of the workflow document.
    This class provides the document for workflow execution.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeDocument class.
        """
        self._start_node: Optional[INode] = None
        self._schema: Optional[Dict[str, Any]] = None

    @property
    def start(self) -> INode:
        """
        Get the start node of the workflow.
        
        Returns:
            The start node of the workflow.
        """
        if not self._start_node:
            raise ValueError("Document is not initialized")
        return self._start_node

    def init(self, schema: Dict[str, Any]) -> None:
        """
        Initialize the document with the given schema.
        
        Args:
            schema: The workflow schema.
        """
        self._schema = schema
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, Edge] = {}
        self._node_blocks: Dict[str, List[str]] = {}
        
        # Flatten the schema to include nested blocks
        flattened_schema = self._flatten_schema(schema)
        
        # Parse nodes and create ports
        for node_data in flattened_schema.get("nodes", []):
            node_id = node_data.get("id", "")
            node_type = node_data.get("type", "")
            node_data_obj = node_data.get("data", {})
            node = Node(node_id, node_type, node_data_obj)
            self._nodes[node_id] = node
            
            # Set start node if this is a start node
            if node_type == FlowGramNode.Start:
                self._start_node = node
            
            # Create input ports
            if "inputs" in node_data_obj:
                inputs_schema = node_data_obj.get("inputs", {})
                if "properties" in inputs_schema:
                    for key in inputs_schema.get("properties", {}):
                        port_id = f"{node_id}_in_{key}"
                        port = Port(port_id, "input", node_id, key)
                        node.ports.add_input(port)
            
            # Create output ports
            if "outputs" in node_data_obj:
                outputs_schema = node_data_obj.get("outputs", {})
                if "properties" in outputs_schema:
                    for key in outputs_schema.get("properties", {}):
                        port_id = f"{node_id}_out_{key}"
                        port = Port(port_id, "output", node_id, key)
                        node.ports.add_output(port)
        
        # Parse edges and connect ports
        for edge_data in flattened_schema.get("edges", []):
            source_node_id = edge_data.get("sourceNodeID", "")
            target_node_id = edge_data.get("targetNodeID", "")
            source_port_id = edge_data.get("sourcePortID", "defaultOutput")
            target_port_id = edge_data.get("targetPortID", "defaultInput")
            
            if source_node_id in self._nodes and target_node_id in self._nodes:
                source_node = self._nodes[source_node_id]
                target_node = self._nodes[target_node_id]
                
                # Connect nodes
                source_node.add_next(target_node)
                target_node.add_prev(source_node)
                
                # Connect ports if port IDs are provided
                if source_port_id and target_port_id:
                    # In JavaScript version, ports are created if they don't exist
                    # Here we'll try to find existing ports or create new ones
                    source_port = None
                    target_port = None
                    
                    # Try to find existing ports by ID
                    for port in source_node.ports.outputs.values():
                        if port.id == source_port_id:
                            source_port = port
                            break
                    
                    for port in target_node.ports.inputs.values():
                        if port.id == target_port_id:
                            target_port = port
                            break
                    
                    # If ports don't exist, create them
                    if not source_port:
                        source_port = Port(source_port_id, "output", source_node_id, source_port_id)
                        source_node.ports.add_output(source_port)
                    
                    if not target_port:
                        target_port = Port(target_port_id, "input", target_node_id, target_port_id)
                        target_node.ports.add_input(target_port)
                    
                    if source_port and target_port:
                        edge_id = f"{source_node_id}_{source_port_id}_to_{target_node_id}_{target_port_id}"
                        edge = Edge(edge_id, source_port.id, target_port.id)
                        edge.source_port = source_port
                        edge.target_port = target_port
                        source_port.add_edge(edge)
                        target_port.add_edge(edge)
                        self._edges[edge_id] = edge

    def get_nodes_by_type(self, node_type: str) -> List[INode]:
        """
        Get all nodes of a specific type.
        
        Args:
            node_type: The type of nodes to get.
            
        Returns:
            A list of nodes of the specified type.
        """
        if not hasattr(self, '_nodes'):
            return []
        
        return [node for node in self._nodes.values() if node.type == node_type]
    
    @property
    def nodes(self) -> List[INode]:
        """
        Get all nodes in the document.
        
        Returns:
            A list of all nodes in the document.
        """
        if not hasattr(self, '_nodes'):
            return []
        
        return list(self._nodes.values())
    
    def _flatten_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten the schema to include nested blocks.
        
        Args:
            schema: The workflow schema.
            
        Returns:
            The flattened schema.
        """
        flattened_schema = {
            "nodes": [],
            "edges": []
        }
        
        # Add root nodes and edges
        flattened_schema["nodes"].extend(schema.get("nodes", []))
        flattened_schema["edges"].extend(schema.get("edges", []))
        
        # Process nested blocks
        self._process_blocks(flattened_schema, schema.get("nodes", []))
        
        return flattened_schema
    
    def _process_blocks(self, flattened_schema: Dict[str, Any], nodes: List[Dict[str, Any]]) -> None:
        """
        Process blocks in nodes and add them to the flattened schema.
        
        Args:
            flattened_schema: The flattened schema to update.
            nodes: The nodes to process.
        """
        for node in nodes:
            node_id = node.get("id", "")
            blocks = node.get("blocks", [])
            edges = node.get("edges", [])
            
            if blocks:
                # Add blocks to flattened schema
                flattened_schema["nodes"].extend(blocks)
                # Record block IDs for the node
                block_ids = [block.get("id", "") for block in blocks]
                self._node_blocks[node_id] = block_ids
                # Process nested blocks recursively
                self._process_blocks(flattened_schema, blocks)
                # Remove blocks from node to avoid duplication
                node.pop("blocks", None)
            
            if edges:
                # Add edges to flattened schema
                flattened_schema["edges"].extend(edges)
                # Remove edges from node to avoid duplication
                node.pop("edges", None)
    
    def get_node(self, node_id: str) -> Optional[INode]:
        """
        Get a node by its ID.
        
        Args:
            node_id: The ID of the node to get.
            
        Returns:
            The node with the specified ID, or None if not found.
        """
        if not hasattr(self, '_nodes'):
            return None
        
        return self._nodes.get(node_id)
    
    def dispose(self) -> None:
        """
        Dispose the document and release resources.
        """
        self._start_node = None
        self._schema = None
        self._node_blocks = {}
