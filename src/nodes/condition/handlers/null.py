"""
Null condition handler for condition nodes.
This module provides the handler for null type conditions.
"""
from typing import cast, Any

from ..type import ConditionHandler, ConditionOperation, ConditionValue


def condition_null_handler(condition: ConditionValue) -> bool:
    """
    Handler for null type conditions.
    
    Args:
        condition: The condition to handle.
        
    Returns:
        True if the condition is satisfied, False otherwise.
    """
    operator = condition["operator"]
    left_value = condition["leftValue"]
    
    if operator == ConditionOperation.EQ:
        right_value = condition["rightValue"]
        return left_value is None and right_value is None
    
    if operator == ConditionOperation.IS_EMPTY:
        return left_value is None
    
    if operator == ConditionOperation.IS_NOT_EMPTY:
        return left_value is not None
    
    return False