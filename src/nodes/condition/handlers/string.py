"""
String condition handler for condition nodes.
This module provides the handler for string type conditions.
"""
from typing import cast

from ..type import ConditionHandler, ConditionOperation, ConditionValue


def condition_string_handler(condition: ConditionValue) -> bool:
    """
    Handler for string type conditions.
    
    Args:
        condition: The condition to handle.
        
    Returns:
        True if the condition is satisfied, False otherwise.
    """
    operator = condition["operator"]
    left_value = cast(str, condition["leftValue"])
    
    # Switch case share scope, so we need to use if else here
    if operator == ConditionOperation.EQ:
        right_value = cast(str, condition["rightValue"])
        return left_value == right_value
    
    if operator == ConditionOperation.NEQ:
        right_value = cast(str, condition["rightValue"])
        return left_value != right_value
    
    if operator == ConditionOperation.CONTAINS:
        right_value = cast(str, condition["rightValue"])
        return right_value in left_value
    
    if operator == ConditionOperation.NOT_CONTAINS:
        right_value = cast(str, condition["rightValue"])
        return right_value not in left_value
    
    if operator == ConditionOperation.IN:
        right_value = cast(list, condition["rightValue"])
        return left_value in right_value
    
    if operator == ConditionOperation.NIN:
        right_value = cast(list, condition["rightValue"])
        return left_value not in right_value
    
    if operator == ConditionOperation.IS_EMPTY:
        return left_value is None or left_value == ""
    
    if operator == ConditionOperation.IS_NOT_EMPTY:
        return left_value is not None and left_value != ""
    
    return False