"""
测试条件节点对数组类型和is_empty/is_not_empty操作符的处理
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 定义测试用的简单工作流模式
SIMPLE_WORKFLOW_SCHEMA = {
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
                    "result": {"type": "constant", "content": "数组为空"}
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
                    "result": {"type": "constant", "content": "数组不为空"}
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

# 定义测试用的复杂工作流模式（包含条件节点和循环节点）
COMPLEX_WORKFLOW_SCHEMA = {
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
                            "key": 5,
                            "name": "themes",
                            "isPropertyRequired": True,
                            "type": "array",
                            "extra": {"index": 0},
                            "items": {"type": "string"}
                        },
                        "apiKey": {
                            "key": 7,
                            "name": "apiKey",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 1}
                        },
                        "apiHost": {
                            "key": 8,
                            "name": "apiHost",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 2}
                        },
                        "modelName": {
                            "key": 12,
                            "name": "modelName",
                            "isPropertyRequired": True,
                            "type": "string",
                            "extra": {"index": 3}
                        }
                    },
                    "required": ["themes", "apiKey", "apiHost", "modelName"]
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
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "End Empty",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "主题数组为空"}
                }
            }
        },
        {
            "id": "end_not_empty",
            "type": "end",
            "meta": {"position": {"x": 1449.3, "y": 500}},
            "data": {
                "title": "End Not Empty",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "主题数组不为空"}
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
    """测试空数组条件"""
    print("测试空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建任务
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": []
        }
    })
    
    # 等待任务完成
    try:
        result = await task.processing
        print(f"空数组测试结果: {result}")
        
        # 检查结果是否符合预期
        assert result.get("result") == "数组为空", f"预期结果为 '数组为空'，实际结果为 {result}"
        
        # 检查工作流状态
        status = task.context.status_center.workflow.status
        print(f"工作流状态: {status}")
        assert status in ["succeeded", "success", WorkflowStatus.Success, WorkflowStatus.Succeeded], f"工作流状态应为成功，实际为 {status}"
        
        # 检查条件节点的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        if condition_snapshot:
            branch = condition_snapshot.branch
            print(f"条件节点分支: {branch}")
            assert branch == "if_empty", f"条件节点应选择 'if_empty' 分支，实际为 {branch}"
        else:
            print("未找到条件节点快照")
        
        return True
    except Exception as e:
        print(f"空数组测试失败: {e}")
        return False

async def test_non_empty_array():
    """测试非空数组条件"""
    print("测试非空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建任务
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2"]
        }
    })
    
    # 等待任务完成
    try:
        result = await task.processing
        print(f"非空数组测试结果: {result}")
        
        # 检查结果是否符合预期
        assert result.get("result") == "数组不为空", f"预期结果为 '数组不为空'，实际结果为 {result}"
        
        # 检查工作流状态
        status = task.context.status_center.workflow.status
        print(f"工作流状态: {status}")
        assert status in ["succeeded", "success", WorkflowStatus.Success, WorkflowStatus.Succeeded], f"工作流状态应为成功，实际为 {status}"
        
        # 检查条件节点的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        if condition_snapshot:
            branch = condition_snapshot.branch
            print(f"条件节点分支: {branch}")
            assert branch == "if_not_empty", f"条件节点应选择 'if_not_empty' 分支，实际为 {branch}"
        else:
            print("未找到条件节点快照")
        
        return True
    except Exception as e:
        print(f"非空数组测试失败: {e}")
        return False

async def test_complex_workflow_empty_array():
    """测试复杂工作流中的空数组条件"""
    print("测试复杂工作流中的空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建任务
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://test-api-host.com",
            "modelName": "test-model"
        }
    })
    
    # 等待任务完成
    try:
        result = await task.processing
        print(f"复杂工作流空数组测试结果: {result}")
        
        # 检查结果是否符合预期
        assert result.get("result") == "主题数组为空", f"预期结果为 '主题数组为空'，实际结果为 {result}"
        
        # 检查工作流状态
        status = task.context.status_center.workflow.status
        print(f"工作流状态: {status}")
        assert status in ["succeeded", "success", WorkflowStatus.Success, WorkflowStatus.Succeeded], f"工作流状态应为成功，实际为 {status}"
        
        # 检查条件节点的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        if condition_snapshot:
            branch = condition_snapshot.branch
            print(f"条件节点分支: {branch}")
            assert branch == "if_empty", f"条件节点应选择 'if_empty' 分支，实际为 {branch}"
        else:
            print("未找到条件节点快照")
        
        return True
    except Exception as e:
        print(f"复杂工作流空数组测试失败: {e}")
        return False

async def test_complex_workflow_non_empty_array():
    """测试复杂工作流中的非空数组条件"""
    print("测试复杂工作流中的非空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建任务
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-api-key",
            "apiHost": "https://test-api-host.com",
            "modelName": "test-model"
        }
    })
    
    # 等待任务完成
    try:
        result = await task.processing
        print(f"复杂工作流非空数组测试结果: {result}")
        
        # 检查结果是否符合预期
        assert result.get("result") == "主题数组不为空", f"预期结果为 '主题数组不为空'，实际结果为 {result}"
        
        # 检查工作流状态
        status = task.context.status_center.workflow.status
        print(f"工作流状态: {status}")
        assert status in ["succeeded", "success", WorkflowStatus.Success, WorkflowStatus.Succeeded], f"工作流状态应为成功，实际为 {status}"
        
        # 检查条件节点的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshot = None
        for snapshot in snapshots:
            if snapshot.node_id == "condition_0":
                condition_snapshot = snapshot
                break
        
        if condition_snapshot:
            branch = condition_snapshot.branch
            print(f"条件节点分支: {branch}")
            assert branch == "if_not_empty", f"条件节点应选择 'if_not_empty' 分支，实际为 {branch}"
        else:
            print("未找到条件节点快照")
        
        return True
    except Exception as e:
        print(f"复杂工作流非空数组测试失败: {e}")
        return False

async def run_tests():
    """运行所有测试"""
    results = []
    results.append(await test_empty_array())
    results.append(await test_non_empty_array())
    results.append(await test_complex_workflow_empty_array())
    results.append(await test_complex_workflow_non_empty_array())
    
    # 打印测试结果摘要
    print("\n测试结果摘要:")
    print(f"空数组条件测试: {'通过' if results[0] else '失败'}")
    print(f"非空数组条件测试: {'通过' if results[1] else '失败'}")
    print(f"复杂工作流空数组条件测试: {'通过' if results[2] else '失败'}")
    print(f"复杂工作流非空数组条件测试: {'通过' if results[3] else '失败'}")
    
    # 检查 WorkflowStatus 枚举值
    print("\nWorkflowStatus 枚举值:")
    for status in WorkflowStatus:
        print(f"{status.name} = {status.value}")
    
    return all(results)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(run_tests())
    print(f"\n总体测试结果: {'通过' if success else '失败'}")
    sys.exit(0 if success else 1)