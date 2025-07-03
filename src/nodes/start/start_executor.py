"""
Start Node Executor for the workflow runtime.
This module provides the executor for start nodes.
"""
from typing import Any, Dict

from ...interface.executor import INodeExecutor, ExecutionContext, ExecutionResult
from ...interface.node import FlowGramNode


class StartExecutor(INodeExecutor):
    """
    Executor for start nodes.
    
    This executor handles the execution of start nodes in a workflow.
    It simply returns the inputs from the IO center as outputs.
    """
    
    @property
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        return FlowGramNode.Start
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute a start node with the given context and return the result.
        
        Args:
            context: The execution context containing the node, inputs, runtime, and container.
            
        Returns:
            The execution result containing the outputs from the IO center.
        """
        return ExecutionResult(
            outputs=context.runtime.io_center.inputs
        )
