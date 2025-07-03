import os
import sys
import unittest
import asyncio
import json
from typing import Dict, Any, List

# 确保能够正确导入runtime-py-core中的模块
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流定义：测试空数组条件
EMPTY_ARRAY_WORKFLOW = {
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
                    "result": {"type": "constant", "content": "数组为空"}
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
                    "result": {"type": "constant", "content": "数组不为空"}
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

# 复杂工作流定义：测试条件节点和循环节点的结合
COMPLEX_WORKFLOW = {
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
            "id": "llm_empty",
            "type": "llm",
            "meta": {"position": {"x": 1449.3, "y": 0}},
            "data": {
                "title": "LLM Empty",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "数组为空，返回空数组处理结果"}
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
            "id": "loop_0",
            "type": "loop",
            "meta": {"position": {"x": 1020, "y": 483}},
            "data": {
                "title": "Loop",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "llm_1",
                    "type": "llm",
                    "meta": {"position": {"x": 189.65, "y": 0}},
                    "data": {
                        "title": "LLM Title",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "生成标题"},
                            "prompt": {"type": "ref", "content": ["loop_0_locals", "item"]}
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
                    "id": "llm_2",
                    "type": "llm",
                    "meta": {"position": {"x": 668.95, "y": 0}},
                    "data": {
                        "title": "LLM Description",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "生成描述"},
                            "prompt": {"type": "ref", "content": ["llm_1", "result"]}
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
                {"sourceNodeID": "llm_1", "targetNodeID": "llm_2"}
            ]
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "llm_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "loop_0", "sourcePortID": "if_not_empty"},
        {"sourceNodeID": "llm_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "loop_0", "targetNodeID": "end_0"}
    ]
}

class ConditionArrayTest(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_empty_array_condition(self):
        """测试空数组条件"""
        print("测试空数组条件...")
        
        # 使用空数组作为输入
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_WORKFLOW,
            "inputs": {
                "array_data": []
            }
        })
        
        # 等待任务完成
        result = await task.processing
        
        # 验证结果
        print(f"空数组测试结果: {result}")
        self.assertEqual(result.get("result"), "数组为空")
        
        # 验证工作流状态
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)

    async def test_non_empty_array_condition(self):
        """测试非空数组条件"""
        print("测试非空数组条件...")
        
        # 使用非空数组作为输入
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_WORKFLOW,
            "inputs": {
                "array_data": ["item1", "item2"]
            }
        })
        
        # 等待任务完成
        result = await task.processing
        
        # 验证结果
        print(f"非空数组测试结果: {result}")
        self.assertEqual(result.get("result"), "数组不为空")
        
        # 验证工作流状态
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)

    async def test_complex_workflow_empty_array(self):
        """测试复杂工作流中的空数组条件"""
        print("测试复杂工作流中的空数组条件...")
        
        # 使用空数组作为输入
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW,
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
            
            # 验证分支选择
            snapshots = task.context.snapshot_center.export_all()
            branches = [s.data.get("branch", "") for s in snapshots if s.node_id == "condition_0"]
            
            print(f"复杂工作流空数组分支: {branches}")
            self.assertTrue(any(b == "if_empty" for b in branches))
            
        except Exception as e:
            print(f"测试过程中出现异常: {e}")
            # 即使LLM执行失败，我们仍然可以验证条件节点的分支选择是否正确
            snapshots = task.context.snapshot_center.export_all()
            branches = [s.data.get("branch", "") for s in snapshots if s.node_id == "condition_0"]
            
            print(f"复杂工作流空数组分支: {branches}")
            self.assertTrue(any(b == "if_empty" for b in branches))

    async def test_complex_workflow_non_empty_array(self):
        """测试复杂工作流中的非空数组条件"""
        print("测试复杂工作流中的非空数组条件...")
        
        # 使用非空数组作为输入
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW,
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
            
            # 验证分支选择
            snapshots = task.context.snapshot_center.export_all()
            branches = [s.data.get("branch", "") for s in snapshots if s.node_id == "condition_0"]
            
            print(f"复杂工作流非空数组分支: {branches}")
            self.assertTrue(any(b == "if_not_empty" for b in branches))
            
        except Exception as e:
            print(f"测试过程中出现异常: {e}")
            # 即使LLM执行失败，我们仍然可以验证条件节点的分支选择是否正确
            snapshots = task.context.snapshot_center.export_all()
            branches = [s.data.get("branch", "") for s in snapshots if s.node_id == "condition_0"]
            
            print(f"复杂工作流非空数组分支: {branches}")
            self.assertTrue(any(b == "if_not_empty" for b in branches))

def run_tests():
    """运行所有测试"""
    # 创建事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 创建测试实例
    test = ConditionArrayTest()
    test.setUp()
    
    # 运行测试
    tests = [
        test.test_empty_array_condition(),
        test.test_non_empty_array_condition(),
        test.test_complex_workflow_empty_array(),
        test.test_complex_workflow_non_empty_array()
    ]
    
    # 等待所有测试完成
    loop.run_until_complete(asyncio.gather(*tests))
    loop.close()

if __name__ == "__main__":
    run_tests()