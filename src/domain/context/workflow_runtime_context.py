"""
Implementation of the workflow runtime context.

The workflow runtime context is the central component of the workflow runtime.
It provides access to various components needed during workflow execution, such as:
- Document: Stores the workflow definition (nodes and edges)
- Variable Store: Manages variables used in the workflow
- State: Manages the execution state of the workflow
- IO Center: Manages inputs and outputs of the workflow
- Snapshot Center: Creates and manages snapshots of the workflow execution
- Status Center: Manages the status of the workflow and nodes
- Reporter: Generates reports of the workflow execution

The context can also create sub-contexts, which inherit certain components from
the parent context, such as the document and IO center, while having their own
variable store and state.
"""
from typing import List, Optional

from ...interface.context import (
    IContext,
    IDocument,
    IState,
    ISnapshotCenter,
    IVariableStore,
    IStatusCenter,
    IReporter,
    IIOCenter,
    ContextData
)
from ...interface.schema import InvokeParams
from ...infrastructure.utils import uuid
from ..variable import WorkflowRuntimeVariableStore
from ..status import WorkflowRuntimeStatusCenter
from ..state import WorkflowRuntimeState
from ..snapshot import WorkflowRuntimeSnapshotCenter
from ..report import WorkflowRuntimeReporter
from ..io_center import WorkflowRuntimeIOCenter
from ..document import WorkflowRuntimeDocument


class WorkflowRuntimeContext(IContext):
    """
    Implementation of the workflow runtime context.
    This class provides the runtime context for workflow execution.
    """

    def __init__(self, data: ContextData):
        """
        Initialize a new instance of the WorkflowRuntimeContext class.
        
        Args:
            data: The context data used to initialize the context.
        """
        self.id: str = uuid()
        self._task_id: str = uuid()  # Default task ID, will be updated when associated with a task
        self._document: IDocument = data.document
        self._variable_store: IVariableStore = data.variable_store
        self._state: IState = data.state
        self._io_center: IIOCenter = data.io_center
        self._snapshot_center: ISnapshotCenter = data.snapshot_center
        self._status_center: IStatusCenter = data.status_center
        self._reporter: IReporter = data.reporter
        self._sub_contexts: List[IContext] = []

    @property
    def document(self) -> IDocument:
        """
        Get the workflow document.
        
        Returns:
            The workflow document.
        """
        return self._document
    
    @property
    def variable_store(self) -> IVariableStore:
        """
        Get the variable store.
        
        Returns:
            The variable store.
        """
        return self._variable_store
    
    @property
    def state(self) -> IState:
        """
        Get the workflow state.
        
        Returns:
            The workflow state.
        """
        return self._state
    
    @property
    def io_center(self) -> IIOCenter:
        """
        Get the IO center.
        
        Returns:
            The IO center.
        """
        return self._io_center
    
    @property
    def snapshot_center(self) -> ISnapshotCenter:
        """
        Get the snapshot center.
        
        Returns:
            The snapshot center.
        """
        return self._snapshot_center
    
    @property
    def status_center(self) -> IStatusCenter:
        """
        Get the status center.
        
        Returns:
            The status center.
        """
        return self._status_center
    
    @property
    def reporter(self) -> IReporter:
        """
        Get the reporter.
        
        Returns:
            The reporter.
        """
        return self._reporter

    def init(self, params: InvokeParams) -> None:
        """
        Initialize the context with the provided parameters.
        
        Args:
            params: The parameters used to initialize the context.
        """
        schema = params["schema"]
        inputs = params["inputs"]
        self._document.init(schema)
        self._variable_store.init()
        self._state.init()
        self._io_center.init(inputs)
        self._snapshot_center.init()
        self._status_center.init()
        self._reporter.init()
        
        # Set inputs as outputs of start node
        start_nodes = self._document.get_nodes_by_type("start")
        if start_nodes and len(start_nodes) > 0:
            start_node = start_nodes[0]
            # Set inputs as outputs of start node in variable store
            for key, value in inputs.items():
                from ...infrastructure.utils import WorkflowRuntimeType
                var_type = WorkflowRuntimeType.get_workflow_type(value)
                if not var_type:
                    var_type = "object"
                
                self._variable_store.set_variable({
                    "nodeID": start_node.id,
                    "key": key,
                    "value": value,
                    "type": var_type
                })

    def dispose(self) -> None:
        """
        Dispose of the context and its resources.
        """
        for sub_context in self._sub_contexts:
            sub_context.dispose()
        self._sub_contexts = []
        self._document.dispose()
        self._variable_store.dispose()
        self._state.dispose()
        self._io_center.dispose()
        self._snapshot_center.dispose()
        self._status_center.dispose()
        self._reporter.dispose()

    def sub(self) -> IContext:
        """
        Create a sub-context that inherits from this context.
        
        Returns:
            A new sub-context.
        """
        variable_store = WorkflowRuntimeVariableStore()
        variable_store.set_parent(self._variable_store)
        state = WorkflowRuntimeState(variable_store)
        context_data = ContextData(
            document=self._document,
            variable_store=variable_store,
            state=state,
            io_center=self._io_center,
            snapshot_center=self._snapshot_center,
            status_center=self._status_center,
            reporter=self._reporter
        )
        sub_context = WorkflowRuntimeContext(context_data)
        self._sub_contexts.append(sub_context)
        sub_context.variable_store.init()
        sub_context.state.init()
        return sub_context

    @staticmethod
    def create() -> IContext:
        """
        Create a new workflow runtime context.
        
        Returns:
            A new workflow runtime context.
        """
        document = WorkflowRuntimeDocument()
        variable_store = WorkflowRuntimeVariableStore()
        state = WorkflowRuntimeState(variable_store)
        io_center = WorkflowRuntimeIOCenter()
        snapshot_center = WorkflowRuntimeSnapshotCenter()
        status_center = WorkflowRuntimeStatusCenter()
        reporter = WorkflowRuntimeReporter(io_center, snapshot_center, status_center)
        context_data = ContextData(
            document=document,
            variable_store=variable_store,
            state=state,
            io_center=io_center,
            snapshot_center=snapshot_center,
            status_center=status_center,
            reporter=reporter
        )
        return WorkflowRuntimeContext(context_data)
