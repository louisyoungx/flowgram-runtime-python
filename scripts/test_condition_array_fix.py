import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional

# 添加项目路径
sys.path.append('runtime-py-core')

from src.interface import WorkflowStatus, WorkflowVariableType
from src.domain.container import WorkflowRuntimeContainer
from src.domain.state.workflow_runtime_state import WorkflowRuntimeState
from src.nodes.condition.condition_executor import ConditionExecutor
from src.nodes.condition.type import ConditionOperation

async def test_condition_array():
    """测试条件节点对数组类型的处理"""
    print("===== 测试条件节点对数组类型和 is_empty/is_not_empty 操作符的处理 =====\n")
    
    # 创建一个简单的工作流，包含条件节点
    schema = {
        "nodes": [
            {
                "id": "start_0",
                "type": "start",
                "meta": {"position": {"x": 0, "y": 0}},
                "data": {
                    "title": "Start",
                    "outputs": {
                        "type": "object",
                        "properties": {
                            "themes": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            },
            {
                "id": "condition_0",
                "type": "condition",
                "meta": {"position": {"x": 200, "y": 0}},
                "data": {
                    "title": "Condition",
                    "conditions": [
                        {
                            "value": {
                                "left": {"type": "ref", "content": ["start_0", "themes"]},
                                "operator": "is_empty"
                            },
                            "key": "if_empty"
                        },
                        {
                            "value": {
                                "left": {"type": "ref", "content": ["start_0", "themes"]},
                                "operator": "is_not_empty"
                            },
                            "key": "if_not_empty"
                        }
                    ]
                }
            },
            {
                "id": "end_empty",
                "type": "end",
                "meta": {"position": {"x": 400, "y": -100}},
                "data": {
                    "title": "End Empty",
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    },
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is empty"}
                    }
                }
            },
            {
                "id": "end_not_empty",
                "type": "end",
                "meta": {"position": {"x": 400, "y": 100}},
                "data": {
                    "title": "End Not Empty",
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    },
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is not empty"}
                    }
                }
            }
        ],
        "edges": [
            {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
            {"sourceNodeID": "condition_0", "targetNodeID": "end_empty", "sourcePortID": "if_empty"},
            {"sourceNodeID": "condition_0", "targetNodeID": "end_not_empty", "sourcePortID": "if_not_empty"}
        ]
    }
    
    # 测试空数组
    print("----- 测试空数组 -----")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get("Engine")
    
    # 使用空数组作为输入
    task_empty = engine.invoke({
        "schema": schema,
        "inputs": {
            "themes": []
        }
    })
    
    # 输出任务ID和初始状态
    print(f"任务ID: {task_empty.id}")
    print(f"初始状态: {task_empty.context.status_center.workflow.status}")
    
    # 获取条件节点执行器
    condition_node = task_empty.context.document.get_node("condition_0")
    condition_executor = ConditionExecutor(condition_node)
    
    # 直接调试条件节点的执行
    conditions = condition_node.data.get("conditions", [])
    print(f"Processing {len(conditions)} conditions: {json.dumps(conditions)}")
    
    # 手动解析条件
    parsed_conditions = []
    for condition in conditions:
        value = condition.get("value", {})
        left = value.get("left", {})
        operator = value.get("operator", "")
        right = value.get("right", {})
        
        # 调用parse_ref处理左操作数
        state = task_empty.context.runtime.state
        left_value = state.parse_ref(left)
        left_type = left_value.get("value_type") if isinstance(left_value, dict) else None
        left_value = left_value.get("value") if isinstance(left_value, dict) else left_value
        
        # 调用parse_value处理右操作数
        right_value = state.parse_value(right)
        right_type = right_value.get("value_type") if isinstance(right_value, dict) else None
        right_value = right_value.get("value") if isinstance(right_value, dict) else right_value
        
        parsed_condition = {
            "key": condition.get("key", ""),
            "leftValue": left_value,
            "leftType": left_type,
            "rightValue": right_value,
            "rightType": right_type,
            "operator": operator
        }
        parsed_conditions.append(parsed_condition)
    
    print(f"Parsed conditions: {parsed_conditions}")
    
    # 验证条件
    valid_conditions = []
    for condition in parsed_conditions:
        left_type = condition.get("leftType")
        operator = condition.get("operator")
        right_type = condition.get("rightType")
        
        # 检查条件是否有效
        from src.nodes.condition.rules import condition_rules
        rule = condition_rules.get(left_type, {}).get(operator)
        if rule and (rule == right_type or right_type is None):
            valid_conditions.append(condition)
    
    print(f"Valid conditions: {valid_conditions}")
    
    # 处理条件
    activated_condition = None
    for condition in valid_conditions:
        left_value = condition.get("leftValue")
        left_type = condition.get("leftType")
        operator = condition.get("operator")
        right_value = condition.get("rightValue")
        
        # 根据类型和操作符处理条件
        if left_type == WorkflowVariableType.Array:
            if operator == "is_empty":
                if left_value is None or len(left_value) == 0:
                    activated_condition = condition
                    break
            elif operator == "is_not_empty":
                if left_value is not None and len(left_value) > 0:
                    activated_condition = condition
                    break
    
    print(f"Activated condition: {activated_condition}")
    if activated_condition:
        print(f"ConditionExecutor returning branch: {activated_condition.get('key')}")
    
    # 等待任务完成
    result_empty = await task_empty.processing
    
    # 输出最终状态和结果
    print(f"最终状态: {task_empty.context.status_center.workflow.status}")
    print(f"结果: {result_empty}")
    
    # 测试非空数组
    print("\n----- 测试非空数组 -----")
    task_not_empty = engine.invoke({
        "schema": schema,
        "inputs": {
            "themes": ["主题1", "主题2"]
        }
    })
    
    # 输出任务ID和初始状态
    print(f"任务ID: {task_not_empty.id}")
    print(f"初始状态: {task_not_empty.context.status_center.workflow.status}")
    
    # 等待任务完成
    result_not_empty = await task_not_empty.processing
    
    # 输出最终状态和结果
    print(f"最终状态: {task_not_empty.context.status_center.workflow.status}")
    print(f"结果: {result_not_empty}")
    
    # 检查 workflow_runtime_state.py 中的 parse_ref 方法
    print("\n----- 检查 parse_ref 方法 -----")
    state = task_not_empty.context.runtime.state
    
    # 测试对数组类型的引用
    ref_empty = {"type": "ref", "content": ["start_0", "themes"]}
    ref_result_empty = state.parse_ref(ref_empty)
    print(f"parse_ref 对空数组的结果: {ref_result_empty}")
    
    ref_not_empty = {"type": "ref", "content": ["start_0", "themes"]}
    ref_result_not_empty = state.parse_ref(ref_not_empty)
    print(f"parse_ref 对非空数组的结果: {ref_result_not_empty}")
    
    # 检查 condition_executor.py 中的条件处理逻辑
    print("\n----- 检查 condition_executor.py 中的条件处理逻辑 -----")
    condition_node_not_empty = task_not_empty.context.document.get_node("condition_0")
    condition_executor_not_empty = ConditionExecutor(condition_node_not_empty)
    
    # 直接执行条件节点
    branch_not_empty = await condition_executor_not_empty.execute(task_not_empty.context)
    print(f"条件节点对非空数组返回的分支: {branch_not_empty}")

async def main():
    """主函数"""
    await test_condition_array()

if __name__ == "__main__":
    asyncio.run(main())