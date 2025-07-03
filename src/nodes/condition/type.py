"""
Type definitions for condition nodes.
This module contains the type definitions for condition nodes.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict, Union, Callable

from ...interface.node import WorkflowVariableType


class ConditionOperation(str, Enum):
    """
    Enum for condition operations.
    """
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"
    IS_TRUE = "is_true"
    IS_FALSE = "is_false"


class ConditionItem(TypedDict):
    """
    Condition item definition.
    """
    key: str
    value: Dict[str, Any]


Conditions = List[ConditionItem]


ConditionRule = Dict[ConditionOperation, Optional[WorkflowVariableType]]


ConditionRules = Dict[WorkflowVariableType, ConditionRule]


class ConditionValue(TypedDict):
    """
    Condition value definition.
    """
    key: str
    leftValue: Any
    rightValue: Any
    leftType: WorkflowVariableType
    rightType: WorkflowVariableType
    operator: ConditionOperation


ConditionHandler = Callable[[ConditionValue], bool]


ConditionHandlers = Dict[WorkflowVariableType, ConditionHandler]