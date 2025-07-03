import os
import sys
import asyncio
import json
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))

from runtime_py_core.src.interface import IEngine, IContainer, WorkflowStatus
from runtime_py_core.src.domain.container import WorkflowRuntimeContainer

# 修正导入路径
sys.path.append(os.path.abspath("runtime-py-core"))
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 定义一个简单的测试工作流，包含条件节点测试数组的 is_empty 和 is_not_empty
SIMPLE_WORKFLOW = {
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
            "meta": {"position": {"x": 600, "y": 100}},
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

async def run_test():
    # 测试用例1：空数组
    print("测试用例1：空数组")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW,
        "inputs": {
            "array_data": []
        }
    })
    
    print(f"任务状态: {task.context.status_center.workflow.status}")
    
    # 等待任务完成
    result = await task.processing
    print(f"任务结果: {result}")
    print(f"最终状态: {task.context.status_center.workflow.status}")
    
    # 检查结果
    assert result == {"result": "Array is empty"}, f"期望 'Array is empty'，但得到 {result}"
    print("测试用例1通过！\n")
    
    # 测试用例2：非空数组
    print("测试用例2：非空数组")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW,
        "inputs": {
            "array_data": ["item1", "item2"]
        }
    })
    
    print(f"任务状态: {task.context.status_center.workflow.status}")
    
    # 等待任务完成
    result = await task.processing
    print(f"任务结果: {result}")
    print(f"最终状态: {task.context.status_center.workflow.status}")
    
    # 检查结果
    assert result == {"result": "Array is not empty"}, f"期望 'Array is not empty'，但得到 {result}"
    print("测试用例2通过！")

if __name__ == "__main__":
    try:
        asyncio.run(run_test())
        print("所有测试通过！")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
