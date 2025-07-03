import os
import sys
import unittest
import asyncio
import json
from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流，测试空数组和非空数组的条件
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

# 复杂工作流，测试条件节点和循环节点的组合
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
                "title": "LLM_Empty",
                "inputsValues": {
                    "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                    "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                    "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                    "temperature": {"type": "constant", "content": 0.5},
                    "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                    "prompt": {"type": "constant", "content": "数组为空"}
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
                "title": "Loop_NotEmpty",
                "batchFor": {"type": "ref", "content": ["start_0", "themes"]}
            },
            "blocks": [
                {
                    "id": "llm_1",
                    "type": "llm",
                    "meta": {"position": {"x": 189.65, "y": 0}},
                    "data": {
                        "title": "LLM_1",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题"},
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
                        "title": "LLM_2",
                        "inputsValues": {
                            "modelName": {"type": "ref", "content": ["start_0", "modelName"]},
                            "apiKey": {"type": "ref", "content": ["start_0", "apiKey"]},
                            "apiHost": {"type": "ref", "content": ["start_0", "apiHost"]},
                            "temperature": {"type": "constant", "content": 0.6},
                            "systemPrompt": {"type": "constant", "content": "用户传入的是一个标题，你需要根据这个标题生成一个小于50字的简短的介绍"},
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
        {"sourceNodeID": "llm_empty", "targetNodeID": "end_0"},
        {"sourceNodeID": "loop_0", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_0", "targetNodeID": "llm_empty", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "loop_0", "sourcePortID": "if_not_empty"}
    ]
}

class ConditionArrayTest(unittest.TestCase):
    def setUp(self):
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_empty_array_condition(self):
        """测试空数组条件"""
        print("\n测试空数组条件...")
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": []
            }
        })
        
        result = await task.processing
        print(f"空数组测试结果: {result}")
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组为空")
        
        # 验证分支是否正确
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点分支: {branch}")
            self.assertEqual(branch, "if_empty")

    async def test_non_empty_array_condition(self):
        """测试非空数组条件"""
        print("\n测试非空数组条件...")
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": ["item1", "item2"]
            }
        })
        
        result = await task.processing
        print(f"非空数组测试结果: {result}")
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组不为空")
        
        # 验证分支是否正确
        snapshots = task.context.snapshot_center.export_all()
        condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
        if condition_snapshots:
            branch = condition_snapshots[0].branch
            print(f"条件节点分支: {branch}")
            self.assertEqual(branch, "if_not_empty")

    async def test_complex_workflow_empty_array(self):
        """测试复杂工作流中的空数组条件"""
        print("\n测试复杂工作流中的空数组条件...")
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],
                "apiKey": "mock-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "mock-model"
            }
        })
        
        try:
            result = await task.processing
            print(f"复杂工作流空数组测试结果: {result}")
            
            # 验证分支是否正确
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
            if condition_snapshots:
                branch = condition_snapshots[0].branch
                print(f"条件节点分支: {branch}")
                self.assertEqual(branch, "if_empty")
        except Exception as e:
            print(f"测试出错: {e}")
            self.fail(f"测试失败: {e}")

    async def test_complex_workflow_non_empty_array(self):
        """测试复杂工作流中的非空数组条件"""
        print("\n测试复杂工作流中的非空数组条件...")
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["露营", "登山", "滑雪", "徒步"],
                "apiKey": "mock-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "mock-model"
            }
        })
        
        try:
            result = await task.processing
            print(f"复杂工作流非空数组测试结果: {result}")
            
            # 验证分支是否正确
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
            if condition_snapshots:
                branch = condition_snapshots[0].branch
                print(f"条件节点分支: {branch}")
                self.assertEqual(branch, "if_not_empty")
        except Exception as e:
            print(f"测试出错: {e}")
            self.fail(f"测试失败: {e}")

def run_tests():
    """运行所有测试"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    test_cases = [
        ConditionArrayTest('test_empty_array_condition'),
        ConditionArrayTest('test_non_empty_array_condition'),
        ConditionArrayTest('test_complex_workflow_empty_array'),
        ConditionArrayTest('test_complex_workflow_non_empty_array')
    ]
    
    for test in test_cases:
        test.setUp()
        try:
            loop.run_until_complete(getattr(test, test._testMethodName)())
            print(f"{test._testMethodName} 通过")
        except Exception as e:
            print(f"{test._testMethodName} 失败: {e}")
    
    loop.close()

if __name__ == "__main__":
    run_tests()