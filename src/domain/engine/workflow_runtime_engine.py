"""
Workflow runtime engine implementation.
"""
import asyncio
import logging
from typing import Dict, List, Optional, Set, Any, TYPE_CHECKING

from ...interface import (
    EngineServices,
    IEngine,
    IExecutor,
    INode,
    WorkflowOutputs,
    IContext,
    InvokeParams,
    ITask,
    FlowGramNode,
    ExecutionResult
)

from ..task import WorkflowRuntimeTask
from ..context import WorkflowRuntimeContext

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from ..container import WorkflowRuntimeContainer


class WorkflowRuntimeEngine(IEngine):
    """
    Implementation of the workflow runtime engine.
    
    This class is responsible for executing workflow nodes and managing the workflow execution process.
    
    Note:
        Methods prefixed with underscore (_) are considered private methods in Python,
        equivalent to private methods in JavaScript.
    """
    
    def cancel(self) -> None:
        """
        Cancel the current workflow execution.
        
        This method stops all running workflows managed by this engine.
        It cancels all processing nodes and marks the workflow as cancelled.
        """
        from ..container import WorkflowRuntimeContainer
        
        # Get all active tasks from the WorkflowApplication
        container = WorkflowRuntimeContainer.instance()
        application = container.get("WorkflowApplication")
        
        # Cancel all active tasks
        for task_id, task in application.tasks.items():
            if task.status == "processing":
                task.cancel()
                logging.info(f"Cancelled task {task_id}")
    
    def __init__(self, service: EngineServices):
        """
        Initialize a new instance of the WorkflowRuntimeEngine class.
        
        Args:
            service: The engine services containing the executor.
        """
        self.executor: IExecutor = service["Executor"]
    
    def invoke(self, params: InvokeParams) -> ITask:
        """
        Invoke the workflow with the specified parameters.
        
        Args:
            params: The parameters to invoke the workflow with.
            
        Returns:
            A task representing the workflow execution.
        """
        context = WorkflowRuntimeContext.create()
        context.init(params)
        context.status_center.workflow.process()  # Set workflow status to processing
        processing = self.process(context)
        
        # Use a callback to dispose the context when processing is done
        async def process_with_dispose():
            try:
                result = await processing
                return result
            finally:
                context.dispose()
        
        return WorkflowRuntimeTask.create({
            "processing": process_with_dispose(),
            "context": context,
        })
    
    async def execute_node(self, params: Dict[str, Any]) -> None:
        """
        Execute a node in the workflow.
        
        Args:
            params: The parameters for node execution.
                node: The node to execute.
                context: The workflow context.
        """
        node: INode = params["node"]
        context: IContext = params["context"]
        
        try:
            if not self._can_execute_node(params={"node": node, "context": context}):
                return
        except Exception as e:
            logging.error(f"Error in _can_execute_node: {str(e)}")
            return
        
        # Set node status to processing and record start time
        import time
        node_status = context.status_center.node_status(node.id)
        node_status.process()
        node_status._start_time = int(time.time() * 1000)  # Set start time in milliseconds
        
        try:
            # Get node inputs and create snapshot
            inputs = context.state.get_node_inputs(node)
            
            # Generate a unique ID for the snapshot
            import uuid
            snapshot_id = str(uuid.uuid4())
            
            # Create snapshot with more complete data
            snapshot = context.snapshot_center.create({
                "id": snapshot_id,
                "node_id": node.id,
                "data": node.data,
                "inputs": inputs,
            })
            
            # Log snapshot creation
            logging.info(f"Created snapshot for node {node.id}: {snapshot_id}")
            
            # Import container here to avoid circular imports
            from ..container import WorkflowRuntimeContainer
            
            # Create a proper ExecutionContext object instead of a dictionary
            from ...interface.executor import ExecutionContext
            execution_context = ExecutionContext(
                node=node,
                inputs=inputs,
                runtime=context,
                container=WorkflowRuntimeContainer.instance()
            )
            result = await self.executor.execute(execution_context)
            
            if context.status_center.workflow.terminated:
                return
            
            outputs = result.outputs
            branch = result.branch
            
            # Add output data to snapshot
            logging.info(f"Adding branch to snapshot for node {node.id}: {branch}")
            snapshot.add_data({"outputs": outputs, "branch": branch})
            
            # Update state with node outputs and mark node as executed
            context.state.set_node_outputs(node, outputs)
            context.state.add_executed_node(node)
            
            # Set node status to success and record end time
            import time
            node_status = context.status_center.node_status(node.id)
            node_status.success()
            node_status._end_time = int(time.time() * 1000)  # Set end time in milliseconds
            
            # Log node execution success
            logging.info(f"Node {node.id} executed successfully, time cost: {node_status.timeCost}ms")
            
            try:
                next_nodes = self._get_next_nodes({"node": node, "branch": branch, "context": context})
                await self._execute_next({"node": node, "next_nodes": next_nodes, "context": context})
            except Exception as e:
                logging.error(f"Error in _get_next_nodes or _execute_next: {str(e)}")
                return
        
        except Exception as e:
            # Set node status to failed and record end time
            import time
            node_status = context.status_center.node_status(node.id)
            node_status.fail()
            node_status._end_time = int(time.time() * 1000)  # Set end time in milliseconds
            
            # Log node execution failure with detailed error
            logging.error(f"Error executing node {node.id}: {str(e)}")
            logging.error(f"Node {node.id} failed, time cost: {node_status.timeCost}ms")
            
            # Add error data to snapshot if available
            if 'snapshot' in locals():
                snapshot.add_data({"error": str(e)})
                logging.info(f"Added error data to snapshot for node {node.id}")
            
            return
    
    async def process(self, context: IContext) -> WorkflowOutputs:
        """
        Process the workflow execution.
        
        Args:
            context: The workflow context.
            
        Returns:
            The workflow outputs.
            
        Raises:
            Exception: If an error occurs during workflow execution.
        """
        start_node = context.document.start
        
        # Set workflow status to processing and record start time
        import time
        context.status_center.workflow.process()
        context.status_center.workflow._start_time = int(time.time() * 1000)
        
        try:
            logging.info(f"Starting workflow execution with start node: {start_node.id}")
            params = {"node": start_node, "context": context}
            
            # Execute the start node and wait for it to complete
            await self.execute_node(params)
            
            # Check if workflow is already terminated (e.g., by cancel)
            if context.status_center.workflow.terminated:
                return context.io_center.outputs
            
            outputs = context.io_center.outputs
            logging.info(f"Workflow execution completed with outputs: {outputs}")
            
            # Set workflow status to success and record end time if not already terminated
            if not context.status_center.workflow.terminated:
                # Use the success method instead of directly setting the status property
                context.status_center.workflow.success()
            
            # Log workflow execution time
            time_cost = context.status_center.workflow.timeCost
            logging.info(f"Workflow execution time: {time_cost}ms")
            
            return outputs
        
        except Exception as e:
            logging.error(f"Error during workflow execution: {str(e)}")
            
            # Set workflow status to failed and record end time
            # Use the fail method instead of directly setting the status property
            context.status_center.workflow.fail()
            
            # Log workflow execution time
            time_cost = context.status_center.workflow.timeCost
            logging.error(f"Workflow execution failed, time cost: {time_cost}ms")
            
            raise e
    
    def _can_execute_node(self, params: Dict[str, Any]) -> bool:
        """
        Check if a node can be executed.
        
        A node can be executed if all its previous nodes have been executed.
        
        Args:
            params: The parameters containing the node and context.
                node: The node to check.
                context: The workflow context.
            
        Returns:
            True if the node can be executed, False otherwise.
        """
        node: INode = params["node"]
        context: IContext = params["context"]
        
        prev_nodes = node.prev
        if len(prev_nodes) == 0:
            return True
        
        return all(context.state.is_executed_node(prev_node) for prev_node in prev_nodes)
    
    def _get_next_nodes(self, params: Dict[str, Any]) -> List[INode]:
        """
        Get the next nodes to execute based on the current node and branch.
        
        If a branch is specified, only the nodes connected to that branch will be returned.
        Nodes that are skipped due to branch selection will be marked as executed.
        
        Args:
            params: The parameters containing the node, branch, and context.
                node: The current node.
                branch: The optional branch ID to follow.
                context: The workflow context.
            
        Returns:
            The list of next nodes to execute.
            
        Raises:
            Exception: If the specified branch is not found.
        """
        node: INode = params["node"]
        branch: Optional[str] = params.get("branch")
        context: IContext = params["context"]
        
        all_next_nodes = node.next
        if not branch:
            return all_next_nodes
        
        # For condition nodes, the branch is the condition key (e.g., "if_1")
        # We need to find the port that corresponds to this branch
        if node.type == FlowGramNode.Condition:
            # For condition nodes, we need to find edges that have the branch as their sourcePortID
            next_node_ids: Set[str] = set()
            
            # Iterate through all output ports and their edges
            for port in node.ports.outputs.values():
                for edge in port.edges:
                    # Check if this edge has the branch as its sourcePortID or if the port ID matches the branch
                    if edge.source_port.id == branch or port.key == branch:
                        next_node_ids.add(edge.target_port.node_id)
                        break
            
            # If no matching edges were found, try to find a port with a matching key
            if not next_node_ids:
                # Try to find a port with a key that matches the branch
                for port in node.ports.outputs.values():
                    if port.key == branch:
                        next_node_ids.update(edge.to.id for edge in port.edges)
                        break
        else:
            # For non-condition nodes, find the port with the matching ID
            target_port = next((port for port in node.ports.outputs.values() if port.id == branch), None)
            if not target_port:
                raise Exception(f"branch {branch} not found")
            
            next_node_ids: Set[str] = set(edge.to.id for edge in target_port.edges)
        next_nodes = [next_node for next_node in all_next_nodes if next_node.id in next_node_ids]
        skip_nodes = [next_node for next_node in all_next_nodes if next_node.id not in next_node_ids]
        
        for skip_node in skip_nodes:
            context.state.add_executed_node(skip_node)
        
        return next_nodes
    
    async def _execute_next(self, params: Dict[str, Any]) -> None:
        """
        Execute the next nodes in the workflow.
        
        If the current node is an End node, no further execution will occur.
        If there are no next nodes, the execution will also stop.
        Otherwise, all next nodes will be executed in parallel.
        
        Args:
            params: The parameters containing the context, current node, and next nodes.
                context: The workflow context.
                node: The current node.
                next_nodes: The list of next nodes to execute.
        """
        context: IContext = params["context"]
        node: INode = params["node"]
        next_nodes: List[INode] = params["next_nodes"]
        
        if node.type == FlowGramNode.End:
            return
        
        if len(next_nodes) == 0:
            # Inside loop node may have no next nodes
            return
        
        # Execute all next nodes in parallel
        await asyncio.gather(*[
            self.execute_node({
                "node": next_node,
                "context": context
            }) for next_node in next_nodes
        ])
