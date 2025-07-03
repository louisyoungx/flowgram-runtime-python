"""
Context interfaces for the workflow runtime.
This module contains the interfaces for workflow runtime context.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Callable, TypedDict
from abc import ABC, abstractmethod

from .schema import InvokeParams
from .node import WorkflowVariableType


class IVariableParseResult(TypedDict, total=False):
    """
    Interface for variable parse result.
    
    This represents the result of parsing a variable, including its value and type information.
    """
    value: Any
    type: WorkflowVariableType
    itemsType: Optional[WorkflowVariableType]


class IDocument(ABC):
    """
    Interface for workflow document.
    
    The document represents the workflow definition, including nodes and edges.
    """
    
    @property
    @abstractmethod
    def start(self) -> 'INode':
        """
        Get the start node of the workflow.
        
        Returns:
            The start node of the workflow.
        """
        pass
    
    @abstractmethod
    def init(self, schema: Dict[str, Any]) -> None:
        """
        Initialize the document with the given schema.
        
        Args:
            schema: The workflow schema.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the document and release resources.
        """
        pass


class IVariableStore(ABC):
    """
    Interface for variable store.
    
    The variable store manages variables used in the workflow.
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
        Get a variable by key.
        
        Args:
            key: The variable key.
            
        Returns:
            The variable value.
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set a variable by key.
        
        Args:
            key: The variable key.
            value: The variable value.
        """
        pass
    
    @abstractmethod
    def has(self, key: str) -> bool:
        """
        Check if a variable exists.
        
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
    def set_parent(self, parent: 'IVariableStore') -> None:
        """
        Set the parent variable store.
        
        Args:
            parent: The parent variable store.
        """
        pass


class IState(ABC):
    """
    Interface for workflow state.
    
    The state manages the execution state of the workflow.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the state.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the state and release resources.
        """
        pass
    
    @abstractmethod
    def get_node_inputs(self, node: 'INode') -> Dict[str, Any]:
        """
        Get the inputs for a node.
        
        Args:
            node: The node.
            
        Returns:
            The node inputs.
        """
        pass
    
    @abstractmethod
    def set_node_outputs(self, node: 'INode', outputs: Dict[str, Any]) -> None:
        """
        Set the outputs for a node.
        
        Args:
            node: The node.
            outputs: The node outputs.
        """
        pass
    
    @abstractmethod
    def add_executed_node(self, node: 'INode') -> None:
        """
        Add a node to the executed nodes list.
        
        Args:
            node: The node.
        """
        pass
    
    @abstractmethod
    def is_executed_node(self, node: 'INode') -> bool:
        """
        Check if a node has been executed.
        
        Args:
            node: The node.
            
        Returns:
            True if the node has been executed, False otherwise.
        """
        pass
    
    @abstractmethod
    def parse_ref(self, ref: str) -> Any:
        """
        Parse a reference.
        
        Args:
            ref: The reference string.
            
        Returns:
            The parsed reference value.
        """
        pass
    
    @abstractmethod
    def parse_value(self, value: Any) -> Any:
        """
        Parse a value.
        
        Args:
            value: The value to parse.
            
        Returns:
            The parsed value.
        """
        pass


class IIOCenter(ABC):
    """
    Interface for IO center.
    
    The IO center manages inputs and outputs of the workflow.
    """
    
    @property
    @abstractmethod
    def outputs(self) -> Dict[str, Any]:
        """
        Get the workflow outputs.
        
        Returns:
            The workflow outputs.
        """
        pass
    
    @abstractmethod
    def init(self, inputs: Dict[str, Any]) -> None:
        """
        Initialize the IO center with the given inputs.
        
        Args:
            inputs: The workflow inputs.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the IO center and release resources.
        """
        pass


class IStatusCenter(ABC):
    """
    Interface for status center.
    
    The status center manages the status of the workflow and nodes.
    """
    
    @property
    @abstractmethod
    def workflow(self) -> 'IWorkflowStatus':
        """
        Get the workflow status.
        
        Returns:
            The workflow status.
        """
        pass
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the status center.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the status center and release resources.
        """
        pass
    
    @abstractmethod
    def node_status(self, node_id: str) -> 'INodeStatus':
        """
        Get the status of a node.
        
        Args:
            node_id: The node ID.
            
        Returns:
            The node status.
        """
        pass
    
    @abstractmethod
    def get_status_node_ids(self, status: str) -> List[str]:
        """
        Get the IDs of nodes with the given status.
        
        Args:
            status: The status.
            
        Returns:
            The list of node IDs.
        """
        pass


class IWorkflowStatus(ABC):
    """
    Interface for workflow status.
    
    The workflow status manages the status of the workflow.
    """
    
    @property
    @abstractmethod
    def terminated(self) -> bool:
        """
        Check if the workflow is terminated.
        
        Returns:
            True if the workflow is terminated, False otherwise.
        """
        pass
    
    @abstractmethod
    def process(self) -> None:
        """
        Set the workflow status to processing.
        """
        pass
    
    @abstractmethod
    def success(self) -> None:
        """
        Set the workflow status to success.
        """
        pass
    
    @abstractmethod
    def fail(self) -> None:
        """
        Set the workflow status to failed.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Set the workflow status to cancelled.
        """
        pass


class INodeStatus(ABC):
    """
    Interface for node status.
    
    The node status manages the status of a node.
    """
    
    @abstractmethod
    def process(self) -> None:
        """
        Set the node status to processing.
        """
        pass
    
    @abstractmethod
    def success(self) -> None:
        """
        Set the node status to success.
        """
        pass
    
    @abstractmethod
    def fail(self) -> None:
        """
        Set the node status to failed.
        """
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        """
        Set the node status to cancelled.
        """
        pass


class ISnapshotCenter(ABC):
    """
    Interface for snapshot center.
    
    The snapshot center manages snapshots of the workflow execution.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the snapshot center.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the snapshot center and release resources.
        """
        pass
    
    @abstractmethod
    def create(self, params: Dict[str, Any]) -> 'ISnapshot':
        """
        Create a snapshot with the given parameters.
        
        Args:
            params: The snapshot parameters.
            
        Returns:
            The created snapshot.
        """
        pass


class ISnapshot(ABC):
    """
    Interface for snapshot.
    
    A snapshot represents the state of a node execution.
    """
    
    @abstractmethod
    def add_data(self, data: Dict[str, Any]) -> None:
        """
        Add data to the snapshot.
        
        Args:
            data: The data to add.
        """
        pass


class IReporter(ABC):
    """
    Interface for reporter.
    
    The reporter generates reports of the workflow execution.
    """
    
    @abstractmethod
    def init(self) -> None:
        """
        Initialize the reporter.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the reporter and release resources.
        """
        pass
    
    @abstractmethod
    def export(self) -> 'IReport':
        """
        Export the report.
        
        Returns:
            The exported report.
        """
        pass


class IReport(ABC):
    """
    Interface for report.
    
    A report contains information about the workflow execution.
    """
    pass


T = TypeVar('T')

class IContext(ABC):
    """
    Interface for workflow runtime context.
    
    The context provides access to various components of the workflow runtime.
    """
    
    @property
    @abstractmethod
    def document(self) -> IDocument:
        """
        Get the workflow document.
        
        Returns:
            The workflow document.
        """
        pass
    
    @property
    @abstractmethod
    def variable_store(self) -> IVariableStore:
        """
        Get the variable store.
        
        Returns:
            The variable store.
        """
        pass
    
    @property
    @abstractmethod
    def state(self) -> IState:
        """
        Get the workflow state.
        
        Returns:
            The workflow state.
        """
        pass
    
    @property
    @abstractmethod
    def io_center(self) -> IIOCenter:
        """
        Get the IO center.
        
        Returns:
            The IO center.
        """
        pass
    
    @property
    @abstractmethod
    def status_center(self) -> IStatusCenter:
        """
        Get the status center.
        
        Returns:
            The status center.
        """
        pass
    
    @property
    @abstractmethod
    def snapshot_center(self) -> ISnapshotCenter:
        """
        Get the snapshot center.
        
        Returns:
            The snapshot center.
        """
        pass
    
    @property
    @abstractmethod
    def reporter(self) -> IReporter:
        """
        Get the reporter.
        
        Returns:
            The reporter.
        """
        pass
    
    @abstractmethod
    def init(self, params: InvokeParams) -> None:
        """
        Initialize the context with the given parameters.
        
        Args:
            params: The invoke parameters.
        """
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """
        Dispose the context and release resources.
        """
        pass
    
    @abstractmethod
    def sub(self) -> 'IContext':
        """
        Create a sub-context.
        
        Returns:
            The created sub-context.
        """
        pass


class ContextData:
    """
    Data for creating a context.
    
    This class represents the data needed to create a workflow runtime context.
    """
    
    def __init__(
        self,
        document: IDocument,
        variable_store: IVariableStore,
        state: IState,
        io_center: IIOCenter,
        snapshot_center: ISnapshotCenter,
        status_center: IStatusCenter,
        reporter: IReporter
    ):
        """
        Initialize context data.
        
        Args:
            document: The workflow document.
            variable_store: The variable store.
            state: The workflow state.
            io_center: The IO center.
            snapshot_center: The snapshot center.
            status_center: The status center.
            reporter: The reporter.
        """
        self.document = document
        self.variable_store = variable_store
        self.state = state
        self.io_center = io_center
        self.snapshot_center = snapshot_center
        self.status_center = status_center
        self.reporter = reporter


class IContainer(Generic[T], ABC):
    """
    Interface for dependency injection container.
    
    The container manages dependencies and provides instances of them.
    """
    
    @abstractmethod
    def get(self, key: Any) -> T:
        """
        Get an instance of a dependency.
        
        Args:
            key: The dependency key.
            
        Returns:
            The dependency instance.
        """
        pass


# Forward reference for INode
from .node import INode
