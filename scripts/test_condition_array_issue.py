import os
import sys
import json
import asyncio
import unittest
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流模式：测试空数组和非空数组的条件判断
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
                        "empty_array": {"type": "array", "items": {"type": "string"}},
                        "non_empty_array": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        },
        {
            "id": "condition_0",
            "type": "condition",
            "meta": {"position": {"x": 300, "y": 0}},
            "data": {
                "title": "Empty Array Condition",
                "conditions": [
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "empty_array"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "empty_array"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_not_empty"
                    }
                ]
            }
        },
        {
            "id": "condition_1",
            "type": "condition",
            "meta": {"position": {"x": 300, "y": 200}},
            "data": {
                "title": "Non-Empty Array Condition",
                "conditions": [
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "non_empty_array"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "non_empty_array"]},
                            "operator": "is_not_empty"
                        },
                        "key": "if_not_empty"
                    }
                ]
            }
        },
        {
            "id": "end_0",
            "type": "end",
            "meta": {"position": {"x": 600, "y": 0}},
            "data": {
                "title": "End",
                "inputs": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string"}
                    }
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "测试完成"}
                }
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "start_0", "targetNodeID": "condition_1"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_0", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_1", "targetNodeID": "end_0", "sourcePortID": "if_not_empty"}
    ]
}

# 复杂工作流模式：模拟用户提供的场景
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
                },
                "inputsValues": {
                    "result": {"type": "constant", "content": "测试完成"}
                }
            }
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "end_0", "sourcePortID": "if_pTr8_"}
    ]
}

class ConditionArrayTest(unittest.TestCase):
    def setUp(self):
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)
        
    async def test_empty_array_condition(self):
        """测试空数组的条件判断"""
        print("\n测试空数组的条件判断...")
        
        # 使用简单工作流，传入空数组和非空数组
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "empty_array": [],
                "non_empty_array": ["item1", "item2"]
            }
        })
        
        context = task.context
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # 等待任务完成
        result = await task.processing
        print(f"任务结果: {result}")
        
        # 验证工作流状态
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # 检查条件节点的分支
        snapshots = context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"空数组条件分支: {branch}")
            self.assertEqual(branch, "if_empty", "空数组应该走 is_empty 分支")
        else:
            self.fail("未找到条件节点的快照")
            
        # 检查非空数组条件节点的分支
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_1"]
        
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"非空数组条件分支: {branch}")
            self.assertEqual(branch, "if_not_empty", "非空数组应该走 is_not_empty 分支")
        else:
            self.fail("未找到条件节点的快照")
    
    async def test_complex_workflow_empty_array(self):
        """测试复杂工作流中的空数组条件"""
        print("\n测试复杂工作流中的空数组条件...")
        
        # 使用复杂工作流，传入空数组
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],
                "apiKey": "test-api-key",
                "apiHost": "https://test-api-host",
                "modelName": "test-model"
            }
        })
        
        context = task.context
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # 等待任务完成
        try:
            result = await task.processing
            print(f"任务结果: {result}")
            
            # 验证工作流状态
            self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Succeeded)
            
            # 检查条件节点的分支
            snapshots = context.snapshot_center.export_all()
            condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
            
            if condition_snapshots:
                branch = condition_snapshots[0].branch
                print(f"条件分支: {branch}")
                self.assertEqual(branch, "if_OVHXT", "空数组应该走 is_empty 分支")
            else:
                self.fail("未找到条件节点的快照")
        except Exception as e:
            print(f"执行出错: {e}")
            self.fail(f"执行出错: {e}")
    
    async def test_complex_workflow_non_empty_array(self):
        """测试复杂工作流中的非空数组条件"""
        print("\n测试复杂工作流中的非空数组条件...")
        
        # 使用复杂工作流，传入非空数组
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],
                "apiKey": "test-api-key",
                "apiHost": "https://test-api-host",
                "modelName": "test-model"
            }
        })
        
        context = task.context
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # 等待任务完成
        try:
            result = await task.processing
            print(f"任务结果: {result}")
            
            # 验证工作流状态
            self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Succeeded)
            
            # 检查条件节点的分支
            snapshots = context.snapshot_center.export_all()
            condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
            
            if condition_snapshots:
                branch = condition_snapshots[0].branch
                print(f"条件分支: {branch}")
                self.assertEqual(branch, "if_pTr8_", "非空数组应该走 is_not_empty 分支")
            else:
                self.fail("未找到条件节点的快照")
        except Exception as e:
            print(f"执行出错: {e}")
            self.fail(f"执行出错: {e}")

async def run_tests():
    """运行所有测试"""
    test = ConditionArrayTest()
    test.setUp()
    
    print("===== 开始测试条件节点对数组类型的处理 =====")
    
    await test.test_empty_array_condition()
    await test.test_complex_workflow_empty_array()
    await test.test_complex_workflow_non_empty_array()
    
    print("===== 测试完成 =====")

if __name__ == "__main__":
    asyncio.run(run_tests())