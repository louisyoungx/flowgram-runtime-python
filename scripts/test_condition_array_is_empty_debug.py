import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional

# 添加当前目录到路径，以便能够导入 src 模块
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 定义简单工作流架构，用于测试条件节点对数组的 is_empty 和 is_not_empty 操作符
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
                        "array": {
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
                            "left": {"type": "ref", "content": ["start_0", "array"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array"]},
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
                    "result": {"type": "constant", "content": "数组为空"}
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

# 定义复杂工作流架构，包含条件节点和循环节点
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
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "apiKey": {"type": "string"},
                        "apiHost": {"type": "string"},
                        "modelName": {"type": "string"}
                    },
                    "required": ["themes", "apiKey", "apiHost", "modelName"]
                }
            }
        },
        {
            "id": "end_0",
            "type": "end",
            "meta": {"position": {"x": 2258.6, "y": 346}},
            "data": {
                "title": "End",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        },
        {
            "id": "condition_Ts3zx",
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
                        "key": "if_OVHXT"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "themes"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_pTr8_"
                    }
                ]
            }
        },
        {
            "id": "llm_FKRbD",
            "type": "llm",
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "LLM_1",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "没填参数就失败了"}
                },
                "inputs": {
                    "type": "object",
                    "required": ["modelName", "apiKey", "apiHost", "temperature", "prompt"],
                    "properties": {
                        "modelName": {"type": "string"},
                        "apiKey": {"type": "string"},
                        "apiHost": {"type": "string"},
                        "temperature": {"type": "number"},
                        "systemPrompt": {"type": "string"},
                        "prompt": {"type": "string"}
                    }
                },
                "outputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                }
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"}
    ]
}

async def test_empty_array_condition():
    """测试空数组的条件节点处理"""
    print("\n===== 测试空数组条件 =====")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用空数组作为输入
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array": []
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务结果: {result}")
        
        # 检查条件节点是否选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            assert branch == "if_empty", f"期望分支 'if_empty'，实际分支 '{branch}'"
            print("✅ 空数组条件测试通过")
        else:
            print("❌ 错误: 找不到条件节点快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_non_empty_array_condition():
    """测试非空数组的条件节点处理"""
    print("\n===== 测试非空数组条件 =====")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用非空数组作为输入
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array": ["item1", "item2"]
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务结果: {result}")
        
        # 检查条件节点是否选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            assert branch == "if_not_empty", f"期望分支 'if_not_empty'，实际分支 '{branch}'"
            print("✅ 非空数组条件测试通过")
        else:
            print("❌ 错误: 找不到条件节点快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_complex_workflow_empty_array():
    """测试复杂工作流中的空数组条件处理"""
    print("\n===== 测试复杂工作流中的空数组条件 =====")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用空数组作为输入
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://test-api-host",
            "modelName": "test-model"
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务结果: {result}")
        
        # 检查条件节点是否选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            assert branch == "if_OVHXT", f"期望分支 'if_OVHXT'，实际分支 '{branch}'"
            print("✅ 复杂工作流空数组条件测试通过")
        else:
            print("❌ 错误: 找不到条件节点快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_complex_workflow_non_empty_array():
    """测试复杂工作流中的非空数组条件处理"""
    print("\n===== 测试复杂工作流中的非空数组条件 =====")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用非空数组作为输入
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-api-key",
            "apiHost": "https://test-api-host",
            "modelName": "test-model"
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务结果: {result}")
        
        # 检查条件节点是否选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            assert branch == "if_pTr8_", f"期望分支 'if_pTr8_'，实际分支 '{branch}'"
            print("✅ 复杂工作流非空数组条件测试通过")
        else:
            print("❌ 错误: 找不到条件节点快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def run_all_tests():
    """运行所有测试"""
    await test_empty_array_condition()
    await test_non_empty_array_condition()
    await test_complex_workflow_empty_array()
    await test_complex_workflow_non_empty_array()

if __name__ == "__main__":
    asyncio.run(run_all_tests())