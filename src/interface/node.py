"""
Node interfaces for the workflow runtime.
This module contains the interfaces for workflow nodes.
"""
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from enum import Enum


class FlowGramNode(str, Enum):
    """Enum for node types."""
    Start = "start"
    End = "end"
    LLM = "llm"
    Condition = "condition"
    Loop = "loop"


class WorkflowStatus(str, Enum):
    """Enum for workflow status."""
    Idle = "idle"
    Processing = "processing"
    Succeeded = "succeeded"
    Failed = "failed"
    Cancelled = "cancelled"


class WorkflowVariableType(str, Enum):
    """Enum for workflow variable types."""
    String = "string"
    Number = "number"
    Integer = "integer"
    Boolean = "boolean"
    Object = "object"
    Array = "array"
    Null = "null"


class IPort(ABC):
    """
    Interface for node ports.
    
    A port represents an input or output point of a node.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the port ID.
        
        Returns:
            The unique identifier of the port.
        """
        pass
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the port type.
        
        Returns:
            The type of the port (e.g., 'input', 'output').
        """
        pass
    
    @property
    @abstractmethod
    def node_id(self) -> str:
        """
        Get the ID of the node that this port belongs to.
        
        Returns:
            The node ID.
        """
        pass
    
    @property
    @abstractmethod
    def key(self) -> str:
        """
        Get the port key.
        
        Returns:
            The key of the port.
        """
        pass


class IEdge(ABC):
    """
    Interface for edges connecting ports.
    
    An edge represents a connection between two ports.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the edge ID.
        
        Returns:
            The unique identifier of the edge.
        """
        pass
    
    @property
    @abstractmethod
    def source_port_id(self) -> str:
        """
        Get the source port ID.
        
        Returns:
            The ID of the source port.
        """
        pass
    
    @property
    @abstractmethod
    def target_port_id(self) -> str:
        """
        Get the target port ID.
        
        Returns:
            The ID of the target port.
        """
        pass


class IPorts(ABC):
    """
    Interface for node ports collection.
    
    This interface provides access to the input and output ports of a node.
    """
    
    @property
    @abstractmethod
    def inputs(self) -> Dict[str, IPort]:
        """
        Get the input ports.
        
        Returns:
            A dictionary of input ports, keyed by port key.
        """
        pass
    
    @property
    @abstractmethod
    def outputs(self) -> Dict[str, IPort]:
        """
        Get the output ports.
        
        Returns:
            A dictionary of output ports, keyed by port key.
        """
        pass


class INode(ABC):
    """
    Interface for workflow nodes.
    
    A node represents a processing unit in a workflow.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the node ID.
        
        Returns:
            The unique identifier of the node.
        """
        pass
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the node type.
        
        Returns:
            The type of the node (e.g., 'start', 'end', 'llm', 'condition', 'loop').
        """
        pass
    
    @property
    @abstractmethod
    def data(self) -> Dict[str, Any]:
        """
        Get the node data.
        
        Returns:
            The data associated with the node.
        """
        pass
    
    @property
    @abstractmethod
    def prev(self) -> List['INode']:
        """
        Get the previous nodes.
        
        Returns:
            A list of nodes that come before this node in the workflow.
        """
        pass
    
    @property
    @abstractmethod
    def next(self) -> List['INode']:
        """
        Get the next nodes.
        
        Returns:
            A list of nodes that come after this node in the workflow.
        """
        pass
    
    @property
    @abstractmethod
    def ports(self) -> IPorts:
        """
        Get the ports of the node.
        
        Returns:
            The ports collection of the node.
        """
        pass
