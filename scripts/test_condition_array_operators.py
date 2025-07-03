import os
import sys
import asyncio
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))

from runtime_py_core.src.interface import IEngine, IContainer, WorkflowStatus
from runtime_py_core.src.domain.container import WorkflowRuntimeContainer

# 定义一个简单的工作流，包含条件节点，用于测试空数组和非空数组
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

# 定义一个复杂的工作流，包含条件节点和循环节点
COMPLEX_WORKFLOW_SCHEMA = {
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
                    "result": {"type": "constant", "content": "主题列表为空"}
                }
            }
        },
        {
            "id": "loop_0",
            "type": "loop",
            "meta": {"position": {"x": 400, "y": 100}},
            "data": {
                "title": "Loop",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "process_theme",
                    "type": "end",
                    "meta": {"position": {"x": 100, "y": 0}},
                    "data": {
                        "title": "Process Theme",
                        "inputs": {
                            "type": "object",
                            "properties": {
                                "theme": {"type": "string"}
                            }
                        },
                        "inputsValues": {
                            "theme": {"type": "ref", "content": ["loop_0_locals", "item"]}
                        }
                    }
                }
            ],
            "edges": []
        },
        {
            "id": "end_loop",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 100}},
            "data": {
                "title": "End Loop",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "主题列表处理完成"}
                }
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "loop_0", "sourcePortID": "if_not_empty"},
        {"sourceNodeID": "loop_0", "targetNodeID": "end_loop"}
    ]
}

async def test_empty_array_condition():
    """测试空数组条件"""
    print("测试空数组条件...")
    
    # 创建容器和引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用空数组调用工作流
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": []
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 验证结果
    print(f"空数组测试结果: {result}")
    assert result.get("result") == "数组为空", f"期望结果为'数组为空'，但得到了{result}"
    
    # 验证条件分支
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_branch = condition_snapshots[0].branch
        print(f"条件分支: {condition_branch}")
        assert condition_branch == "if_empty", f"期望分支为'if_empty'，但得到了{condition_branch}"
    else:
        print("未找到条件节点快照")
    
    print("空数组条件测试通过 ✅")

async def test_non_empty_array_condition():
    """测试非空数组条件"""
    print("测试非空数组条件...")
    
    # 创建容器和引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用非空数组调用工作流
    task = engine.invoke({
        "schema": SIMPLE_WORKFLOW_SCHEMA,
        "inputs": {
            "array_data": ["item1", "item2", "item3"]
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 验证结果
    print(f"非空数组测试结果: {result}")
    assert result.get("result") == "数组不为空", f"期望结果为'数组不为空'，但得到了{result}"
    
    # 验证条件分支
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_branch = condition_snapshots[0].branch
        print(f"条件分支: {condition_branch}")
        assert condition_branch == "if_not_empty", f"期望分支为'if_not_empty'，但得到了{condition_branch}"
    else:
        print("未找到条件节点快照")
    
    print("非空数组条件测试通过 ✅")

async def test_complex_workflow_empty_array():
    """测试复杂工作流中的空数组条件"""
    print("测试复杂工作流中的空数组条件...")
    
    # 创建容器和引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用空数组调用工作流
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": []
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 验证结果
    print(f"复杂工作流空数组测试结果: {result}")
    assert result.get("result") == "主题列表为空", f"期望结果为'主题列表为空'，但得到了{result}"
    
    # 验证条件分支
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_branch = condition_snapshots[0].branch
        print(f"条件分支: {condition_branch}")
        assert condition_branch == "if_empty", f"期望分支为'if_empty'，但得到了{condition_branch}"
    else:
        print("未找到条件节点快照")
    
    print("复杂工作流空数组条件测试通过 ✅")

async def test_complex_workflow_non_empty_array():
    """测试复杂工作流中的非空数组条件和循环"""
    print("测试复杂工作流中的非空数组条件和循环...")
    
    # 创建容器和引擎
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # 使用非空数组调用工作流
    task = engine.invoke({
        "schema": COMPLEX_WORKFLOW_SCHEMA,
        "inputs": {
            "themes": ["主题1", "主题2", "主题3"]
        }
    })
    
    # 等待工作流执行完成
    result = await task.processing
    
    # 验证结果
    print(f"复杂工作流非空数组测试结果: {result}")
    assert result.get("result") == "主题列表处理完成", f"期望结果为'主题列表处理完成'，但得到了{result}"
    
    # 验证条件分支
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_branch = condition_snapshots[0].branch
        print(f"条件分支: {condition_branch}")
        assert condition_branch == "if_not_empty", f"期望分支为'if_not_empty'，但得到了{condition_branch}"
    else:
        print("未找到条件节点快照")
    
    # 验证循环节点是否执行
    loop_snapshots = [s for s in snapshots if s.node_id.startswith("process_theme")]
    print(f"循环节点快照数量: {len(loop_snapshots)}")
    assert len(loop_snapshots) > 0, "循环节点未执行"
    
    print("复杂工作流非空数组条件和循环测试通过 ✅")

async def run_tests():
    """运行所有测试"""
    try:
        await test_empty_array_condition()
        print("\n")
        await test_non_empty_array_condition()
        print("\n")
        await test_complex_workflow_empty_array()
        print("\n")
        await test_complex_workflow_non_empty_array()
        print("\n全部测试通过 ✅")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_tests())