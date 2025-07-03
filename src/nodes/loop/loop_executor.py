"""
Loop Node Executor for the workflow runtime.
This module provides the executor for loop nodes.
"""
from typing import Any, Dict, List, Optional, TypedDict, cast
import asyncio

from ...interface.executor import INodeExecutor, ExecutionContext, ExecutionResult
from ...interface.node import FlowGramNode, WorkflowVariableType
from ...interface.engine import IEngine


class LoopArray(List[Any]):
    """Type alias for loop array."""
    pass


class LoopExecutorInputs(TypedDict):
    """
    Inputs for the loop executor.
    
    Attributes:
        batchFor: The array to loop over.
    """
    batchFor: LoopArray


class LoopExecutor(INodeExecutor):
    """
    Executor for loop nodes.
    
    This executor handles the execution of loop nodes in a workflow.
    It executes child nodes for each item in the loop array.
    """
    
    @property
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        return FlowGramNode.Loop
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute a loop node with the given context and return the result.
        
        Args:
            context: The execution context containing the node, inputs, runtime, and container.
            
        Returns:
            The execution result.
        """
        loop_node_id = context.node.id
        loop_array_result = context.runtime.state.parse_ref(context.node.data["batchFor"])
        self._check_loop_array(loop_array_result)
        
        loop_array = loop_array_result["value"]
        items_type = loop_array_result["items_type"]
        engine = context.container.get(IEngine)
        # Get child nodes from document's _node_blocks
        document = context.runtime.document
        # Access the _node_blocks attribute to get the child nodes
        if hasattr(document, '_node_blocks') and context.node.id in document._node_blocks:
            block_ids = document._node_blocks[context.node.id]
            sub_nodes = [document._nodes[block_id] for block_id in block_ids if block_id in document._nodes]
            # In a loop context, start sub nodes are those that don't have previous nodes within the loop
            start_sub_nodes = [node for node in sub_nodes if not node.prev]
        else:
            # Fallback to the previous method if _node_blocks is not available
            all_nodes = document.nodes
            sub_nodes = [node for node in all_nodes if any(prev.id == context.node.id for prev in node.prev)]
            start_sub_nodes = [node for node in sub_nodes if len([p for p in node.prev if p.id != context.node.id]) == 0]
        
        if not loop_array or not start_sub_nodes:
            return ExecutionResult(outputs={})
        
        # Not use Array method to make error stack more concise, and better performance
        for i in range(len(loop_array)):
            loop_item = loop_array[i]
            sub_context = context.runtime.sub()
            sub_context.variable_store.set_variable({
                "nodeID": f"{loop_node_id}_locals",
                "key": "item",
                "type": items_type,
                "value": loop_item
            })
            
            await asyncio.gather(*[
                engine.execute_node({
                    "context": sub_context,
                    "node": node
                }) for node in start_sub_nodes
            ])
        
        return ExecutionResult(outputs={})
    
    def _check_loop_array(self, loop_array_result: Optional[Any]) -> None:
        """
        Check if the loop array is valid.
        
        Args:
            loop_array_result: The result of parsing the loop array reference.
            
        Raises:
            ValueError: If the loop array is invalid.
        """
        loop_array = loop_array_result["value"] if loop_array_result else None
        if not loop_array or not isinstance(loop_array, list):
            raise ValueError("batchFor is required")
        
        loop_array_type = loop_array_result["type"]
        if loop_array_type != WorkflowVariableType.Array:
            raise ValueError("batchFor must be an array")
        
        loop_array_item_type = loop_array_result["items_type"]
        if loop_array_item_type is None:
            raise ValueError("batchFor items must be array items")
