"""
Variable interfaces for the runtime.
This module contains the interfaces for variable related types.
"""
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from enum import Enum


class VariableType(str, Enum):
    """
    Enum for variable types.
    
    This enum represents the possible types of variables in a workflow.
    """
    String = "string"
    Number = "number"
    Integer = "integer"
    Boolean = "boolean"
    Object = "object"
    Array = "array"
    Null = "null"


class VariableValueType(str, Enum):
    """
    Enum for variable value types.
    
    This enum represents the possible types of variable values in a workflow.
    """
    Constant = "constant"
    Reference = "ref"
    Expression = "expression"


class IVariable(ABC):
    """
    Interface for variable.
    
    A variable represents a value that can be used in a workflow.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the variable ID.
        
        Returns:
            The unique identifier of the variable.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the variable name.
        
        Returns:
            The name of the variable.
        """
        pass
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the variable type.
        
        Returns:
            The type of the variable (e.g., 'string', 'number', 'boolean', 'object', 'array').
        """
        pass
    
    @property
    @abstractmethod
    def value(self) -> Any:
        """
        Get the variable value.
        
        Returns:
            The value of the variable.
        """
        pass
    
    @abstractmethod
    def set_value(self, value: Any) -> None:
        """
        Set the variable value.
        
        Args:
            value: The new value of the variable.
        """
        pass


class IVariableValue(ABC):
    """
    Interface for variable value.
    
    A variable value represents a value that can be used in a workflow.
    """
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the variable value type.
        
        Returns:
            The type of the variable value (e.g., 'constant', 'ref', 'expression').
        """
        pass
    
    @property
    @abstractmethod
    def content(self) -> Any:
        """
        Get the variable value content.
        
        Returns:
            The content of the variable value.
        """
        pass


class IVariableStore(ABC):
    """
    Interface for variable store.
    
    The variable store manages variables in a workflow.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the variable store.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the variable store and release resources.
        """
        pass
    
    @abstractmethod
    def get(self, key: str) -> Any:
        """
        Get a variable value by key.
        
        Args:
            key: The variable key.
            
        Returns:
            The variable value.
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set a variable value by key.
        
        Args:
            key: The variable key.
            value: The variable value.
        """
        pass
    
    @abstractmethod
    def has(self, key: str) -> bool:
        """
        Check if a variable exists by key.
        
        Args:
            key: The variable key.
            
        Returns:
            True if the variable exists, False otherwise.
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete a variable by key.
        
        Args:
            key: The variable key.
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """
        Clear all variables.
        """
        pass
    
    @abstractmethod
    def export(self) -> Dict[str, Any]:
        """
        Export all variables.
        
        Returns:
            A dictionary of all variables.
        """
        pass
