"""
Implementation of workflow nodes, ports, and edges.
"""
from typing import Any, Dict, List, Optional, Set

from ...interface.node import INode, IPort, IEdge, IPorts


class Port(IPort):
    """Implementation of the port interface."""
    
    def __init__(self, port_id: str, port_type: str, node_id: str, port_key: str):
        """
        Initialize a new instance of the Port class.
        
        Args:
            port_id: The unique identifier of the port.
            port_type: The type of the port (e.g., 'input', 'output').
            node_id: The ID of the node that this port belongs to.
            port_key: The key of the port.
        """
        self._id = port_id
        self._type = port_type
        self._node_id = node_id
        self._key = port_key
        self._edges: List[Edge] = []
    
    @property
    def id(self) -> str:
        """Get the port ID."""
        return self._id
    
    @property
    def type(self) -> str:
        """Get the port type."""
        return self._type
    
    @property
    def node_id(self) -> str:
        """Get the ID of the node that this port belongs to."""
        return self._node_id
    
    @property
    def key(self) -> str:
        """Get the port key."""
        return self._key
    
    @property
    def edges(self) -> List['Edge']:
        """Get the edges connected to this port."""
        return self._edges
    
    def add_edge(self, edge: 'Edge') -> None:
        """
        Add an edge to this port.
        
        Args:
            edge: The edge to add.
        """
        self._edges.append(edge)


class Edge(IEdge):
    """Implementation of the edge interface."""
    
    def __init__(self, edge_id: str, source_port_id: str, target_port_id: str):
        """
        Initialize a new instance of the Edge class.
        
        Args:
            edge_id: The unique identifier of the edge.
            source_port_id: The ID of the source port.
            target_port_id: The ID of the target port.
        """
        self._id = edge_id
        self._source_port_id = source_port_id
        self._target_port_id = target_port_id
        self._source_port: Optional[Port] = None
        self._target_port: Optional[Port] = None
    
    @property
    def id(self) -> str:
        """Get the edge ID."""
        return self._id
    
    @property
    def source_port_id(self) -> str:
        """Get the source port ID."""
        return self._source_port_id
    
    @property
    def target_port_id(self) -> str:
        """Get the target port ID."""
        return self._target_port_id
    
    @property
    def source_port(self) -> Optional[Port]:
        """Get the source port."""
        return self._source_port
    
    @source_port.setter
    def source_port(self, port: Port) -> None:
        """
        Set the source port.
        
        Args:
            port: The source port.
        """
        self._source_port = port
    
    @property
    def target_port(self) -> Optional[Port]:
        """Get the target port."""
        return self._target_port
    
    @target_port.setter
    def target_port(self, port: Port) -> None:
        """
        Set the target port.
        
        Args:
            port: The target port.
        """
        self._target_port = port


class Ports(IPorts):
    """Implementation of the ports collection interface."""
    
    def __init__(self):
        """Initialize a new instance of the Ports class."""
        self._inputs: Dict[str, Port] = {}
        self._outputs: Dict[str, Port] = {}
    
    @property
    def inputs(self) -> Dict[str, Port]:
        """Get the input ports."""
        return self._inputs
    
    @property
    def outputs(self) -> Dict[str, Port]:
        """Get the output ports."""
        return self._outputs
    
    def add_input(self, port: Port) -> None:
        """
        Add an input port.
        
        Args:
            port: The input port to add.
        """
        self._inputs[port.key] = port
    
    def add_output(self, port: Port) -> None:
        """
        Add an output port.
        
        Args:
            port: The output port to add.
        """
        self._outputs[port.key] = port


class Node(INode):
    """Implementation of the node interface."""
    
    def __init__(self, node_id: str, node_type: str, node_data: Dict[str, Any]):
        """
        Initialize a new instance of the Node class.
        
        Args:
            node_id: The unique identifier of the node.
            node_type: The type of the node.
            node_data: The data associated with the node.
        """
        self._id = node_id
        self._type = node_type
        self._data = node_data
        self._prev: List[Node] = []
        self._next: List[Node] = []
        self._ports = Ports()
    
    @property
    def id(self) -> str:
        """Get the node ID."""
        return self._id
    
    @property
    def type(self) -> str:
        """Get the node type."""
        return self._type
    
    @property
    def data(self) -> Dict[str, Any]:
        """Get the node data."""
        return self._data
    
    @property
    def prev(self) -> List['Node']:
        """Get the previous nodes."""
        return self._prev
    
    @property
    def next(self) -> List['Node']:
        """Get the next nodes."""
        return self._next
    
    @property
    def ports(self) -> Ports:
        """Get the ports of the node."""
        return self._ports
    
    def add_prev(self, node: 'Node') -> None:
        """
        Add a previous node.
        
        Args:
            node: The previous node to add.
        """
        if node not in self._prev:
            self._prev.append(node)
    
    def add_next(self, node: 'Node') -> None:
        """
        Add a next node.
        
        Args:
            node: The next node to add.
        """
        if node not in self._next:
            self._next.append(node)