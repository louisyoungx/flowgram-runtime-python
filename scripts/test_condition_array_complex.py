import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))

from runtime_py_core.src.interface import IEngine, IContainer, WorkflowStatus
from runtime_py_core.src.domain.container import WorkflowRuntimeContainer

# 复杂工作流定义，包含条件节点和循环节点
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
        },
        {
            "id": "loop_2OD2p",
            "type": "loop",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "Loop_1",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "832659",
                    "type": "llm",
                    "meta": {"position": {"x": 189.65, "y": 0}},
                    "data": {
                        "title": "LLM_1",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题，例如输入"露营"，返回"在瑞士阿尔卑斯山的露营之旅""},
                            "prompt": {"type": "ref", "content": ["loop_2OD2p_locals", "item"]}
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
                    "id": "llm_KYkc0",
                    "type": "llm",
                    "meta": {"position": {"x": 668.95, "y": 0}},
                    "data": {
                        "title": "LLM_4",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "用户传入的是一个标题，你需要根据这个标题生成一个小于50字的简短的介绍"},
                            "prompt": {"type": "ref", "content": ["832659", "result"]}
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
            "edges": [{"sourceNodeID": "832659", "targetNodeID": "llm_KYkc0"}]
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "loop_2OD2p", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "loop_2OD2p", "sourcePortID": "if_pTr8_"}
    ]
}

class ConditionArrayComplexTest(unittest.TestCase):
    def setUp(self):
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_empty_array_condition(self):
        """测试空数组条件分支"""
        # 使用空数组作为输入
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            },
        })
        
        context = task.context
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # 等待工作流执行完成
        result = await task.processing
        
        # 验证工作流状态
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # 验证条件节点选择了空数组分支
        condition_snapshot = None
        for snapshot in context.snapshot_center.export_all():
            if snapshot.node_id == "condition_Ts3zx":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot, "条件节点快照不存在")
        self.assertEqual(condition_snapshot.branch, "if_OVHXT", "条件节点没有选择空数组分支")
        
        # 验证执行了空数组分支的LLM节点
        self.assertIn("llm_FKRbD", context.status_center.node_statuses)
        self.assertEqual(context.status_center.node_status("llm_FKRbD").status, WorkflowStatus.Succeeded)
        
        # 验证没有执行循环节点
        self.assertNotIn("loop_2OD2p", context.status_center.node_statuses)

    async def test_non_empty_array_condition(self):
        """测试非空数组条件分支"""
        # 使用非空数组作为输入
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            },
        })
        
        context = task.context
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Processing)
        
        # 等待工作流执行完成
        result = await task.processing
        
        # 验证工作流状态
        self.assertEqual(context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # 验证条件节点选择了非空数组分支
        condition_snapshot = None
        for snapshot in context.snapshot_center.export_all():
            if snapshot.node_id == "condition_Ts3zx":
                condition_snapshot = snapshot
                break
        
        self.assertIsNotNone(condition_snapshot, "条件节点快照不存在")
        self.assertEqual(condition_snapshot.branch, "if_pTr8_", "条件节点没有选择非空数组分支")
        
        # 验证执行了循环节点
        self.assertIn("loop_2OD2p", context.status_center.node_statuses)
        self.assertEqual(context.status_center.node_status("loop_2OD2p").status, WorkflowStatus.Succeeded)
        
        # 验证没有执行空数组分支的LLM节点
        self.assertNotIn("llm_FKRbD", context.status_center.node_statuses)

def run_tests():
    # 创建一个事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 运行测试
    test_cases = [
        ConditionArrayComplexTest('test_empty_array_condition'),
        ConditionArrayComplexTest('test_non_empty_array_condition')
    ]
    
    for test_case in test_cases:
        # 设置测试环境
        test_case.setUp()
        
        # 运行测试方法
        test_method = getattr(test_case, test_case._testMethodName)
        try:
            loop.run_until_complete(test_method())
            print(f"✅ {test_case._testMethodName} 通过")
        except Exception as e:
            print(f"❌ {test_case._testMethodName} 失败: {e}")
    
    # 关闭事件循环
    loop.close()

if __name__ == "__main__":
    run_tests()