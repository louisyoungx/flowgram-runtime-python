"""
Nodes module for workflow runtime.
"""
from typing import List, Type

from ..interface import INodeExecutorFactory
from .start import StartExecutor
from .end import EndExecutor
from .llm import LLMExecutor
from .condition import ConditionExecutor
from .loop import LoopExecutor

# List of all node executor factories
WorkflowRuntimeNodeExecutors: List[Type[INodeExecutorFactory]] = [
    StartExecutor,
    EndExecutor,
    LLMExecutor,
    ConditionExecutor,
    LoopExecutor,
]

__all__ = [
    'WorkflowRuntimeNodeExecutors',
    'StartExecutor',
    'EndExecutor',
    'LLMExecutor',
    'ConditionExecutor',
    'LoopExecutor',
]