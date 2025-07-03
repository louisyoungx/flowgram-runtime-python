import os
import sys
import asyncio
import unittest
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流定义：测试空数组和非空数组的条件节点
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
                        "array": {"type": "array", "items": {"type": "string"}}
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
            "meta": {"position": {"x": 600, "y": -100}},
            "data": {
                "title": "End Empty",
                "inputsValues": {
                    "result": {"type": "constant", "content": "数组为空"}
                },
                "inputs": {
                    "type": "object",
                    "properties": {"result": {"type": "string"}}
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
                    "result": {"type": "constant", "content": "数组不为空"}
                },
                "inputs": {
                    "type": "object",
                    "properties": {"result": {"type": "string"}}
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

# 复杂工作流定义：包含条件节点、循环节点和多个分支
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
            "id": "end_0",
            "type": "end",
            "meta": {"position": {"x": 2258.6, "y": 346}},
            "data": {
                "title": "End",
                "inputs": {
                    "type": "object",
                    "properties": {"result": {"type": "string"}}
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
                    "properties": {"result": {"type": "string"}}
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

async def test_empty_array():
    """测试空数组条件"""
    print("\n测试空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建一个包含空数组的输入
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array": []
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务完成，结果: {result}")
        
        # 检查是否选择了正确的分支
        if result.get("result") == "数组为空":
            print("✅ 成功: 空数组条件正确触发")
        else:
            print(f"❌ 失败: 空数组条件未正确触发，得到: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_non_empty_array():
    """测试非空数组条件"""
    print("\n测试非空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建一个包含非空数组的输入
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array": ["item1", "item2"]
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务完成，结果: {result}")
        
        # 检查是否选择了正确的分支
        if result.get("result") == "数组不为空":
            print("✅ 成功: 非空数组条件正确触发")
        else:
            print(f"❌ 失败: 非空数组条件未正确触发，得到: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_complex_workflow_empty_array():
    """测试复杂工作流中的空数组条件"""
    print("\n测试复杂工作流中的空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建一个包含空主题数组的输入
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": [],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务完成，结果: {result}")
        
        # 检查任务状态和分支选择
        status = task.status
        print(f"任务状态: {status}")
        
        # 检查快照，确认条件节点选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            if branch == "if_OVHXT":
                print("✅ 成功: 空数组条件在复杂工作流中正确触发")
            else:
                print(f"❌ 失败: 空数组条件在复杂工作流中未正确触发，分支: {branch}")
        else:
            print("❌ 失败: 未找到条件节点的快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def test_complex_workflow_non_empty_array():
    """测试复杂工作流中的非空数组条件"""
    print("\n测试复杂工作流中的非空数组条件...")
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 创建一个包含非空主题数组的输入
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-api-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    try:
        # 等待任务完成
        result = await task.processing
        print(f"任务完成，结果: {result}")
        
        # 检查任务状态和分支选择
        status = task.status
        print(f"任务状态: {status}")
        
        # 检查快照，确认条件节点选择了正确的分支
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点选择的分支: {branch}")
            if branch == "if_pTr8_":
                print("✅ 成功: 非空数组条件在复杂工作流中正确触发")
            else:
                print(f"❌ 失败: 非空数组条件在复杂工作流中未正确触发，分支: {branch}")
        else:
            print("❌ 失败: 未找到条件节点的快照")
    except Exception as e:
        print(f"❌ 错误: {e}")

async def run_tests():
    """运行所有测试"""
    print("开始运行条件节点数组类型测试...")
    
    await test_empty_array()
    await test_non_empty_array()
    await test_complex_workflow_empty_array()
    await test_complex_workflow_non_empty_array()
    
    print("\n测试完成")

if __name__ == "__main__":
    asyncio.run(run_tests())