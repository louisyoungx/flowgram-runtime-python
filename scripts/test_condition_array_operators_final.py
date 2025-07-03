"""
测试条件节点对数组类型和is_empty/is_not_empty操作符的处理
"""
import sys
import os
import asyncio
import json
from typing import Dict, Any, List, Optional

# 添加项目根目录到Python路径
sys.path.append('runtime-py-core')

from src.interface import IEngine, IContainer, WorkflowStatus, WorkflowVariableType
from src.domain.container import WorkflowRuntimeContainer
from src.nodes.condition.type import ConditionOperation

# 测试空数组的is_empty条件
async def test_empty_array():
    """测试空数组的is_empty条件"""
    print("\n测试空数组的is_empty条件...")
    
    # 创建工作流模式
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
                            "array_data": {
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
                                "left": {"type": "ref", "content": ["start_0", "array_data"]},
                                "operator": "is_empty"
                            },
                            "key": "if_empty"
                        },
                        {
                            "value": {
                                "left": {"type": "ref", "content": ["start_0", "array_data"]},
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
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    }
                }
            },
            {
                "id": "end_not_empty",
                "type": "end",
                "meta": {"position": {"x": 400, "y": 100}},
                "data": {
                    "title": "End Not Empty",
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is not empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
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
    
    # 创建输入数据 - 空数组
    inputs = {
        "array_data": []
    }
    
    # 获取工作流引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 调用工作流引擎
    task = engine.invoke({
        "schema": schema,
        "inputs": inputs
    })
    
    # 获取上下文和处理过程
    context = task.context
    print(f"初始工作流状态: {context.status_center.workflow.status}")
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 检查最终状态和结果
    print(f"最终工作流状态: {context.status_center.workflow.status}")
    print(f"工作流结果: {result}")
    
    # 获取条件节点
    condition_node = context.document.get_node("condition_0")
    print(f"条件节点: {condition_node}")
    
    # 检查快照
    snapshots = context.snapshot_center.export_all()
    print("\n快照信息:")
    for snapshot_data in snapshots:
        print(f"节点ID: {snapshot_data.get('nodeID')}")
        print(f"输入: {snapshot_data.get('inputs')}")
        print(f"输出: {snapshot_data.get('outputs')}")
        print(f"数据: {snapshot_data.get('data')}")
        print(f"分支: {snapshot_data.get('branch', '')}")
        print("-" * 50)
    
    # 验证结果
    assert context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "Array is empty"}
    
    return result

# 测试非空数组的is_not_empty条件
async def test_non_empty_array():
    """测试非空数组的is_not_empty条件"""
    print("\n测试非空数组的is_not_empty条件...")
    
    # 创建工作流模式
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
                            "array_data": {
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
                                "left": {"type": "ref", "content": ["start_0", "array_data"]},
                                "operator": "is_empty"
                            },
                            "key": "if_empty"
                        },
                        {
                            "value": {
                                "left": {"type": "ref", "content": ["start_0", "array_data"]},
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
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    }
                }
            },
            {
                "id": "end_not_empty",
                "type": "end",
                "meta": {"position": {"x": 400, "y": 100}},
                "data": {
                    "title": "End Not Empty",
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Array is not empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
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
    
    # 创建输入数据 - 非空数组
    inputs = {
        "array_data": ["item1", "item2", "item3"]
    }
    
    # 获取工作流引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 调用工作流引擎
    task = engine.invoke({
        "schema": schema,
        "inputs": inputs
    })
    
    # 获取上下文和处理过程
    context = task.context
    print(f"初始工作流状态: {context.status_center.workflow.status}")
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 检查最终状态和结果
    print(f"最终工作流状态: {context.status_center.workflow.status}")
    print(f"工作流结果: {result}")
    
    # 获取条件节点
    condition_node = context.document.get_node("condition_0")
    print(f"条件节点: {condition_node}")
    
    # 检查快照
    snapshots = context.snapshot_center.export_all()
    print("\n快照信息:")
    for snapshot_data in snapshots:
        print(f"节点ID: {snapshot_data.get('nodeID')}")
        print(f"输入: {snapshot_data.get('inputs')}")
        print(f"输出: {snapshot_data.get('outputs')}")
        print(f"数据: {snapshot_data.get('data')}")
        print(f"分支: {snapshot_data.get('branch', '')}")
        print("-" * 50)
    
    # 验证结果
    assert context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "Array is not empty"}
    
    return result

# 测试复杂工作流中的条件节点
async def test_complex_workflow():
    """测试复杂工作流中的条件节点"""
    print("\n测试复杂工作流中的条件节点...")
    
    # 创建工作流模式 - 模拟用户提供的复杂工作流
    schema = {
        "nodes": [
            {
                "id": "start_0",
                "type": "start",
                "meta": {"position": {"x": 180, "y": 346}},
                "data": {
                    "title": "Start",
                    "outputs": {
                        "type": "object",
                        "properties": {
                            "themes": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "apiKey": {"type": "string"},
                            "apiHost": {"type": "string"},
                            "modelName": {"type": "string"}
                        }
                    }
                }
            },
            {
                "id": "condition_0",
                "type": "condition",
                "meta": {"position": {"x": 640, "y": 282.5}},
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
                "meta": {"position": {"x": 1000, "y": 0}},
                "data": {
                    "title": "End Empty",
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Themes array is empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
                    }
                }
            },
            {
                "id": "end_not_empty",
                "type": "end",
                "meta": {"position": {"x": 1000, "y": 200}},
                "data": {
                    "title": "End Not Empty",
                    "inputsValues": {
                        "result": {"type": "constant", "content": "Themes array is not empty"}
                    },
                    "inputs": {
                        "type": "object",
                        "properties": {
                            "result": {"type": "string"}
                        }
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
    
    # 测试非空数组
    inputs = {
        "themes": ["露营", "登山", "滑雪", "徒步"],
        "apiKey": "test-api-key",
        "apiHost": "https://api.example.com",
        "modelName": "test-model"
    }
    
    # 获取工作流引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 调用工作流引擎
    task = engine.invoke({
        "schema": schema,
        "inputs": inputs
    })
    
    # 获取上下文和处理过程
    context = task.context
    print(f"初始工作流状态: {context.status_center.workflow.status}")
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 检查最终状态和结果
    print(f"最终工作流状态: {context.status_center.workflow.status}")
    print(f"工作流结果: {result}")
    
    # 验证结果
    assert context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "Themes array is not empty"}
    
    # 测试空数组
    inputs = {
        "themes": [],
        "apiKey": "test-api-key",
        "apiHost": "https://api.example.com",
        "modelName": "test-model"
    }
    
    # 调用工作流引擎
    task = engine.invoke({
        "schema": schema,
        "inputs": inputs
    })
    
    # 获取上下文和处理过程
    context = task.context
    print(f"\n初始工作流状态: {context.status_center.workflow.status}")
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 检查最终状态和结果
    print(f"最终工作流状态: {context.status_center.workflow.status}")
    print(f"工作流结果: {result}")
    
    # 验证结果
    assert context.status_center.workflow.status == WorkflowStatus.Succeeded
    assert result == {"result": "Themes array is empty"}
    
    return "复杂工作流测试完成"

async def main():
    """主函数"""
    try:
        # 测试空数组
        empty_result = await test_empty_array()
        print(f"\n空数组测试结果: {empty_result}")
        
        # 测试非空数组
        non_empty_result = await test_non_empty_array()
        print(f"\n非空数组测试结果: {non_empty_result}")
        
        # 测试复杂工作流
        complex_result = await test_complex_workflow()
        print(f"\n复杂工作流测试结果: {complex_result}")
        
        print("\n所有测试通过!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 创建新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 运行测试
    loop.run_until_complete(main())
    loop.close()