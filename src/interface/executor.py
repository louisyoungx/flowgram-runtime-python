"""
Executor interfaces for the workflow runtime.
This module contains the interfaces for workflow executors.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from abc import ABC, abstractmethod

from .context import IContext
from .node import INode, FlowGramNode


class ExecutionContext:
    """
    Context for node execution.
    
    This class represents the context for executing a node.
    """
    
    def __init__(self, node: INode, inputs: Dict[str, Any], runtime: IContext, container: Any):
        """
        Initialize execution context.
        
        Args:
            node: The node to execute.
            inputs: The inputs for the node.
            runtime: The runtime context.
            container: The dependency injection container.
        """
        self.node = node
        self.inputs = inputs
        self.runtime = runtime
        self.container = container


class ExecutionResult:
    """
    Result of node execution.
    
    This class represents the result of executing a node.
    """
    
    def __init__(self, outputs: Dict[str, Any], branch: Optional[str] = None):
        """
        Initialize execution result.
        
        Args:
            outputs: The outputs of the node execution.
            branch: The branch to follow (for condition nodes).
        """
        self.outputs = outputs
        self.branch = branch


class IExecutor(ABC):
    """
    Interface for workflow executors.
    
    The executor is responsible for executing nodes in a workflow.
    """
    
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute with the given context and return the result.
        
        Args:
            context: The execution context.
            
        Returns:
            The execution result.
        """
        pass


class INodeExecutor(ABC):
    """
    Interface for node executors.
    
    A node executor is responsible for executing a specific type of node.
    """
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        pass
    
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute a node with the given context and return the result.
        
        Args:
            context: The execution context.
            
        Returns:
            The execution result.
        """
        pass


class INodeExecutorFactory(ABC):
    """
    Interface for node executor factory.
    
    A node executor factory creates node executors for specific node types.
    """
    
    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get the node type that this factory can create executors for.
        
        Returns:
            The node type.
        """
        pass
    
    @abstractmethod
    def create(self) -> INodeExecutor:
        """
        Create a node executor.
        
        Returns:
            The created node executor.
        """
        pass


class EngineServices:
    """
    Services for the workflow engine.
    
    This class provides services for the workflow engine.
    """
    
    def __init__(self, executor: IExecutor):
        """
        Initialize engine services.
        
        Args:
            executor: The executor service.
        """
        self.Executor = executor
