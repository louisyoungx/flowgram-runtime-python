"""
Condition handlers for condition nodes.
This module exports all condition handlers.
"""
from ....interface.node import WorkflowVariableType
from ..type import ConditionHandlers
from .string import condition_string_handler
from .number import condition_number_handler
from .boolean import condition_boolean_handler
from .object import condition_object_handler
from .array import condition_array_handler
from .null import condition_null_handler


condition_handlers: ConditionHandlers = {
    WorkflowVariableType.String: condition_string_handler,
    WorkflowVariableType.Number: condition_number_handler,
    WorkflowVariableType.Integer: condition_number_handler,
    WorkflowVariableType.Boolean: condition_boolean_handler,
    WorkflowVariableType.Object: condition_object_handler,
    WorkflowVariableType.Array: condition_array_handler,
    WorkflowVariableType.Null: condition_null_handler,
}
