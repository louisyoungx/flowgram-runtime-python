"""
Array condition handler for condition nodes.
This module provides the handler for array type conditions.
"""
from typing import cast, List, Any

from ..type import ConditionHandler, ConditionOperation, ConditionValue


def condition_array_handler(condition: ConditionValue) -> bool:
    """
    Handler for array type conditions.
    
    Args:
        condition: The condition to handle.
        
    Returns:
        True if the condition is satisfied, False otherwise.
    """
    operator = condition["operator"]
    left_value = cast(List[Any], condition["leftValue"])
    
    if operator == ConditionOperation.IS_EMPTY:
        return left_value is None or len(left_value) == 0
    
    if operator == ConditionOperation.IS_NOT_EMPTY:
        return left_value is not None and len(left_value) > 0
    
    return False