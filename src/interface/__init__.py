"""
Interface definitions for the workflow runtime.
This module exports all interfaces for the workflow runtime.
"""

# Engine interfaces
from .engine import IEngine

# Task interfaces
from .task import ITask, TaskParams

# Context interfaces
from .context import (
    IContext, IVariableStore, IDocument, IState, IIOCenter,
    IStatusCenter, IWorkflowStatus, INodeStatus, ISnapshotCenter,
    ISnapshot, IReporter, IReport, ContextData, IContainer
)

# Node interfaces
from .node import (
    INode, IPort, IEdge, IPorts,
    FlowGramNode, WorkflowVariableType
)

# Executor interfaces
from .executor import (
    IExecutor, INodeExecutor, INodeExecutorFactory,
    ExecutionContext, ExecutionResult, EngineServices
)

# Schema interfaces
from .schema import (
    WorkflowSchema, NodeSchema, PortSchema, EdgeSchema,
    InvokeParams, WorkflowOutputs, TaskRunInput, TaskRunOutput,
    TaskReportInput, TaskResultInput, TaskCancelInput,
    WorkflowStatus, FlowGramAPIName
)

# Validation interfaces
from .validation import IValidation, ValidationResult

# Workflow interfaces
from .workflow import (
    WorkflowInputs, WorkflowOutputs, WorkflowStatusType,
    WorkflowStatus as WorkflowStatusDict, NodeReport, IWorkflow
)

# Container interfaces
from .container import IContainer

# Report interfaces
from .report import INodeReport, IReport, IReporter

# Snapshot interfaces
from .snapshot import ISnapshot, ISnapshotCenter

# Status interfaces
from .status import StatusType, IStatus, IWorkflowStatus, INodeStatus, IStatusCenter

# Variable interfaces
from .variable import (
    VariableType, VariableValueType, IVariable,
    IVariableValue, IVariableStore
)

__all__ = [
    # Engine interfaces
    "IEngine",
    
    # Task interfaces
    "ITask", "TaskParams",
    
    # Context interfaces
    "IContext", "IVariableStore", "IDocument", "IState",
    "IIOCenter", "IStatusCenter", "IWorkflowStatus", "INodeStatus",
    "ISnapshotCenter", "ISnapshot", "IReporter", "IReport",
    "ContextData", "IContainer",
    
    # Node interfaces
    "INode", "IPort", "IEdge", "IPorts",
    "FlowGramNode", "WorkflowVariableType",
    
    # Executor interfaces
    "IExecutor", "INodeExecutor", "INodeExecutorFactory",
    "ExecutionContext", "ExecutionResult", "EngineServices",
    
    # Schema interfaces
    "WorkflowSchema", "NodeSchema", "PortSchema", "EdgeSchema",
    "InvokeParams", "WorkflowOutputs", "TaskRunInput", "TaskRunOutput",
    "TaskReportInput", "TaskResultInput", "TaskCancelInput",
    "WorkflowStatus", "FlowGramAPIName",
    
    # Validation interfaces
    "IValidation", "ValidationResult",
    
    # Workflow interfaces
    "WorkflowInputs", "WorkflowOutputs", "WorkflowStatusType",
    "WorkflowStatusDict", "NodeReport", "IWorkflow",
    
    # Container interfaces
    "IContainer",
    
    # Report interfaces
    "INodeReport", "IReport", "IReporter",
    
    # Snapshot interfaces
    "ISnapshot", "ISnapshotCenter",
    
    # Status interfaces
    "StatusType", "IStatus", "IWorkflowStatus", "INodeStatus", "IStatusCenter",
    
    # Variable interfaces
    "VariableType", "VariableValueType", "IVariable",
    "IVariableValue", "IVariableStore"
]
