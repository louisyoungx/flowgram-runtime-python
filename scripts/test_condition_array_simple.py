import sys
import os
import asyncio
from typing import Dict, Any, List

# 添加项目根目录到 Python 路径
sys.path.append('runtime-py-core')

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单的工作流模式，包含条件节点测试空数组和非空数组
EMPTY_ARRAY_SCHEMA = {
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
            "meta": {"position": {"x": 300, "y": 0}},
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
            "meta": {"position": {"x": 600, "y": -100}},
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
            "meta": {"position": {"x": 600, "y": 100}},
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

async def test_empty_array():
    """测试空数组条件处理"""
    print("测试空数组条件处理...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建并运行工作流，使用空数组作为输入
    task = engine.invoke({
        "schema": EMPTY_ARRAY_SCHEMA,
        "inputs": {
            "array_data": []
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    print(f"工作流执行结果: {result}")
    print(f"最终状态: {task.context.status_center.workflow.status}")
    
    # 验证结果
    assert result == {"result": "Array is empty"}, "空数组应该激活 is_empty 条件"
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded, "工作流应该成功执行"
    
    return result

async def test_non_empty_array():
    """测试非空数组条件处理"""
    print("\n测试非空数组条件处理...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建并运行工作流，使用非空数组作为输入
    task = engine.invoke({
        "schema": EMPTY_ARRAY_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2"]
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    print(f"工作流执行结果: {result}")
    print(f"最终状态: {task.context.status_center.workflow.status}")
    
    # 验证结果
    assert result == {"result": "Array is not empty"}, "非空数组应该激活 is_not_empty 条件"
    assert task.context.status_center.workflow.status == WorkflowStatus.Succeeded, "工作流应该成功执行"
    
    return result

async def main():
    """主函数"""
    # 测试空数组
    empty_result = await test_empty_array()
    
    # 测试非空数组
    non_empty_result = await test_non_empty_array()
    
    print("\n测试总结:")
    print(f"空数组测试结果: {empty_result}")
    print(f"非空数组测试结果: {non_empty_result}")
    
    print("\n所有测试通过!")

if __name__ == "__main__":
    asyncio.run(main())