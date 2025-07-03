"""
Condition Node Executor for the workflow runtime.
This module provides the executor for condition nodes.
"""
from typing import Any, Dict, List, Optional, cast

from ...interface.executor import INodeExecutor, ExecutionContext, ExecutionResult
from ...interface.node import FlowGramNode, WorkflowVariableType

from .type import ConditionItem, ConditionValue, Conditions
from .rules import condition_rules
from .handlers import condition_handlers


class ConditionExecutor(INodeExecutor):
    """
    Executor for condition nodes.
    
    This executor handles the execution of condition nodes in a workflow.
    It evaluates conditions and determines which branch to follow.
    """
    
    @property
    def type(self) -> str:
        """
        Get the node type that this executor can handle.
        
        Returns:
            The node type.
        """
        return FlowGramNode.Condition
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """
        Execute a condition node with the given context and return the result.
        
        Args:
            context: The execution context containing the node, inputs, runtime, and container.
            
        Returns:
            The execution result containing the outputs and branch to follow.
        """
        conditions: Optional[Conditions] = context.node.data.get("conditions")
        if not conditions:
            print("No conditions found in node data")
            return ExecutionResult(outputs={})
        
        print(f"Processing {len(conditions)} conditions: {conditions}")
        parsed_conditions = [
            self._parse_condition(item, context)
            for item in conditions
        ]
        print(f"Parsed conditions: {parsed_conditions}")
        
        valid_conditions = [
            item for item in parsed_conditions
            if self._check_condition(item)
        ]
        print(f"Valid conditions: {valid_conditions}")
        
        activated_condition = next(
            (item for item in valid_conditions if self._handle_condition(item)),
            None
        )
        print(f"Activated condition: {activated_condition}")
        
        if not activated_condition:
            print("No activated condition found")
            return ExecutionResult(outputs={})
        
        branch = activated_condition["key"]
        print(f"ConditionExecutor returning branch: {branch}")
        
        return ExecutionResult(
            outputs={},
            branch=branch
        )
    
    def _parse_condition(self, item: ConditionItem, context: ExecutionContext) -> ConditionValue:
        """
        Parse a condition item.
        
        Args:
            item: The condition item to parse.
            context: The execution context.
            
        Returns:
            The parsed condition value.
        """
        key = item["key"]
        value = item["value"]
        left = value["left"]
        operator = value["operator"]
        right = value.get("right")  # Use get() to safely handle missing 'right' for is_empty/is_not_empty
        
        parsed_left = context.runtime.state.parse_ref(left)
        left_value = parsed_left.get("value") if parsed_left else None
        left_type = parsed_left.get("type") if parsed_left else WorkflowVariableType.Null
        
        parsed_right = context.runtime.state.parse_value(right) if right else None
        right_value = parsed_right.get("value") if parsed_right else None
        right_type = parsed_right.get("type") if parsed_right else WorkflowVariableType.Null
        
        return {
            "key": key,
            "leftValue": left_value,
            "leftType": left_type,
            "rightValue": right_value,
            "rightType": right_type,
            "operator": operator
        }
    
    def _check_condition(self, condition: ConditionValue) -> bool:
        """
        Check if a condition is valid.
        
        Args:
            condition: The condition to check.
            
        Returns:
            True if the condition is valid, False otherwise.
        """
        rule = condition_rules.get(condition["leftType"])
        if rule is None:
            raise ValueError(f"condition left type {condition['leftType']} is not supported")
        
        rule_type = rule.get(condition["operator"])
        if rule_type is None:
            raise ValueError(f"condition operator {condition['operator']} is not supported")
        
        if rule_type != condition["rightType"]:
            # Instead of raising an error, we return False
            # raise ValueError(f"condition right type expected {rule_type}, got {condition['rightType']}")
            return False
        
        return True
    
    def _handle_condition(self, condition: ConditionValue) -> bool:
        """
        Handle a condition.
        
        Args:
            condition: The condition to handle.
            
        Returns:
            True if the condition is satisfied, False otherwise.
        """
        handler = condition_handlers.get(condition["leftType"])
        if not handler:
            raise ValueError(f"condition left type {condition['leftType']} is not supported")
        
        is_active = handler(condition)
        return is_active
