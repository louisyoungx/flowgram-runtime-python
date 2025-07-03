"""
Boolean condition handler for condition nodes.
This module provides the handler for boolean type conditions.
"""
from typing import cast

from ..type import ConditionHandler, ConditionOperation, ConditionValue


def condition_boolean_handler(condition: ConditionValue) -> bool:
    """
    Handler for boolean type conditions.
    
    Args:
        condition: The condition to handle.
        
    Returns:
        True if the condition is satisfied, False otherwise.
    """
    operator = condition["operator"]
    left_value = cast(bool, condition["leftValue"])
    
    if operator == ConditionOperation.EQ:
        right_value = cast(bool, condition["rightValue"])
        return left_value == right_value
    
    if operator == ConditionOperation.NEQ:
        right_value = cast(bool, condition["rightValue"])
        return left_value != right_value
    
    if operator == ConditionOperation.IS_TRUE:
        return left_value is True
    
    if operator == ConditionOperation.IS_FALSE:
        return left_value is False
    
    if operator == ConditionOperation.IN:
        right_value = cast(list, condition["rightValue"])
        return left_value in right_value
    
    if operator == ConditionOperation.NIN:
        right_value = cast(list, condition["rightValue"])
        return left_value not in right_value
    
    if operator == ConditionOperation.IS_EMPTY:
        return left_value is None
    
    if operator == ConditionOperation.IS_NOT_EMPTY:
        return left_value is not None
    
    return False