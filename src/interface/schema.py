"""
Schema interfaces for the workflow runtime.
This module contains the interfaces for workflow schemas.
"""
from typing import Any, Dict, List, Optional, Union, TypedDict
from enum import Enum


class PortSchema(TypedDict):
    """
    Schema for a port.
    
    A port represents an input or output point of a node.
    """
    id: str
    type: str
    nodeId: str
    key: str


class EdgeSchema(TypedDict):
    """
    Schema for an edge.
    
    An edge represents a connection between two ports.
    """
    id: str
    sourcePortId: str
    targetPortId: str


class NodeSchema(TypedDict):
    """
    Schema for a node.
    
    A node represents a processing unit in a workflow.
    """
    id: str
    type: str
    data: Dict[str, Any]
    ports: Dict[str, List[PortSchema]]


class WorkflowSchema(TypedDict):
    """
    Schema for a workflow.
    
    A workflow represents a process flow with nodes and edges.
    """
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]


class TaskRunInput(TypedDict):
    """
    Input for task run API.
    
    This class represents the input for the task run API.
    """
    schema: str
    inputs: Dict[str, Any]


class TaskRunOutput(TypedDict):
    """
    Output for task run API.
    
    This class represents the output for the task run API.
    """
    taskID: str


class TaskReportInput(TypedDict):
    """
    Input for task report API.
    
    This class represents the input for the task report API.
    """
    taskID: str


class TaskResultInput(TypedDict):
    """
    Input for task result API.
    
    This class represents the input for the task result API.
    """
    taskID: str


class TaskCancelInput(TypedDict):
    """
    Input for task cancel API.
    
    This class represents the input for the task cancel API.
    """
    taskID: str


class InvokeParams:
    """
    Parameters for invoking a workflow.
    
    This class represents the parameters for invoking a workflow.
    """
    
    def __init__(self, schema: Union[str, Dict[str, Any]], inputs: Dict[str, Any]):
        """
        Initialize invoke parameters.
        
        Args:
            schema: The workflow schema, either as a JSON string or a dictionary.
            inputs: The workflow inputs.
        """
        self.schema = schema
        self.inputs = inputs


class WorkflowOutputs(TypedDict):
    """
    Outputs of a workflow.
    
    This class represents the outputs of a workflow.
    """
    outputs: Dict[str, Any]


class WorkflowStatus(str, Enum):
    """
    Enum for workflow status.
    
    This enum represents the status of a workflow.
    """
    Processing = "processing"
    Success = "success"
    Failed = "failed"
    Cancelled = "cancelled"


class FlowGramAPIName(str, Enum):
    """
    Enum for FlowGram API names.
    
    This enum represents the names of FlowGram APIs.
    """
    TaskRun = "taskRun"
    TaskReport = "taskReport"
    TaskResult = "taskResult"
    TaskCancel = "taskCancel"
    ServerInfo = "serverInfo"
    Validation = "validation"
