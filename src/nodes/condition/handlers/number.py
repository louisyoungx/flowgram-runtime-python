"""
Number condition handler for condition nodes.
This module provides the handler for number type conditions.
"""
from typing import cast, Union

from ..type import ConditionHandler, ConditionOperation, ConditionValue


def condition_number_handler(condition: ConditionValue) -> bool:
    """
    Handler for number type conditions.
    
    Args:
        condition: The condition to handle.
        
    Returns:
        True if the condition is satisfied, False otherwise.
    """
    operator = condition["operator"]
    left_value = cast(Union[int, float], condition["leftValue"])
    
    if operator == ConditionOperation.EQ:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value == right_value
    
    if operator == ConditionOperation.NEQ:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value != right_value
    
    if operator == ConditionOperation.GT:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value > right_value
    
    if operator == ConditionOperation.GTE:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value >= right_value
    
    if operator == ConditionOperation.LT:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value < right_value
    
    if operator == ConditionOperation.LTE:
        right_value = cast(Union[int, float], condition["rightValue"])
        return left_value <= right_value
    
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