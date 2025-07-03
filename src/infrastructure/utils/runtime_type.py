"""
Utility functions for determining and comparing workflow variable types.
"""
from typing import Any, Optional
from ...interface.node import WorkflowVariableType


class WorkflowRuntimeType:
    """
    Provides utility functions for working with workflow variable types.
    """
    
    @staticmethod
    def get_workflow_type(value: Any = None) -> Optional[WorkflowVariableType]:
        """
        Determines the workflow variable type of a given value.
        
        Args:
            value: The value to determine the type of.
            
        Returns:
            The workflow variable type, or None if the type cannot be determined.
        """
        # 处理 null 和 undefined 的情况
        if value is None:
            return WorkflowVariableType.Null
        
        # 处理基本类型
        if isinstance(value, str):
            return WorkflowVariableType.String
        
        if isinstance(value, bool):
            return WorkflowVariableType.Boolean
        
        if isinstance(value, int):
            return WorkflowVariableType.Integer
        
        if isinstance(value, float):
            return WorkflowVariableType.Number
        
        # 处理数组
        if isinstance(value, list):
            return WorkflowVariableType.Array
        
        # 处理普通对象
        if isinstance(value, dict):
            return WorkflowVariableType.Object
        
        return None
    
    @staticmethod
    def is_match_workflow_type(value: Any, type_: WorkflowVariableType) -> bool:
        """
        Checks if a value matches a specific workflow variable type.
        
        Args:
            value: The value to check.
            type_: The workflow variable type to match against.
            
        Returns:
            True if the value matches the specified type, False otherwise.
        """
        workflow_type = WorkflowRuntimeType.get_workflow_type(value)
        if workflow_type is None:
            return False
        
        return WorkflowRuntimeType.is_type_equal(workflow_type, type_)
    
    @staticmethod
    def is_type_equal(left_type: WorkflowVariableType, right_type: WorkflowVariableType) -> bool:
        """
        Checks if two workflow variable types are considered equal.
        
        Args:
            left_type: The first type to compare.
            right_type: The second type to compare.
            
        Returns:
            True if the types are considered equal, False otherwise.
        """
        # 处理 Number 和 Integer 等价的情况
        if (
            (left_type == WorkflowVariableType.Number and right_type == WorkflowVariableType.Integer) or
            (left_type == WorkflowVariableType.Integer and right_type == WorkflowVariableType.Number)
        ):
            return True
        
        return left_type == right_type
