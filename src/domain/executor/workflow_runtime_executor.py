"""
Workflow runtime executor.
"""
from typing import Dict, Type, List, Any

from ...interface import (
    FlowGramNode,
    IExecutor,
    INodeExecutor,
    INodeExecutorFactory,
    ExecutionContext,
    ExecutionResult
)


class WorkflowRuntimeExecutor(IExecutor):
    """
    Workflow runtime executor.
    Implements the IExecutor interface to execute nodes in a workflow.
    """
    
    def __init__(self, node_executors: List[Type[INodeExecutorFactory]]):
        """
        Initialize the executor with node executors.
        
        Args:
            node_executors: A list of node executor factories.
        """
        self._node_executors: Dict[FlowGramNode, INodeExecutor] = {}
        
        # Register node executors
        for executor_factory in node_executors:
            self.register(executor_factory())
    
    def register(self, executor: INodeExecutor) -> None:
        """
        Register a node executor.
        
        Args:
            executor: The node executor to register.
        """
        self._node_executors[executor.type] = executor
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute a node in a workflow.
        
        Args:
            context: The execution context.
            
        Returns:
            The execution result.
            
        Raises:
            Exception: If no executor is found for the node type.
        """
        node_type = context.node.type
        node_executor = self._node_executors.get(node_type)
        
        if not node_executor:
            raise Exception(f"No executor found for node type {node_type}")
        
        output = await node_executor.execute(context)
        return output