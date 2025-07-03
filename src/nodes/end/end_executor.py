"""
End Node Executor for the workflow runtime.
This module provides the executor for end nodes.
"""
from typing import Any, Dict

from ...interface.executor import INodeExecutor, ExecutionContext, ExecutionResult
from ...interface.node import FlowGramNode


class EndExecutor(INodeExecutor):
    """
    Executor for end nodes.
    
    This executor handles the execution of end nodes in a workflow.
    It sets the inputs as the outputs in the IO center and returns the inputs as outputs.
    """
    
    @property
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        return FlowGramNode.End
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute an end node with the given context and return the result.
        
        Args:
            context: The execution context containing the node, inputs, runtime, and container.
            
        Returns:
            The execution result containing the inputs as outputs.
        """
        # For end nodes, we set the inputs as the outputs in the IO center
        # This makes the inputs available as the workflow outputs
        context.runtime.io_center.set_outputs(context.inputs)
        
        # Return the inputs as the outputs of this node execution
        return ExecutionResult(
            outputs=context.inputs
        )
