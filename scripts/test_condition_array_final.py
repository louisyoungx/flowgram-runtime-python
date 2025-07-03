import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

# 确保正确导入
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流模式 - 测试空数组条件
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

# 复杂工作流模式 - 模拟实际场景
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
        }
    ],
    "edges": [
        {"sourceNodeID": "start_0", "targetNodeID": "condition_Ts3zx"},
        {"sourceNodeID": "llm_FKRbD", "targetNodeID": "end_0"},
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "llm_FKRbD", "sourcePortID": "if_OVHXT"}
    ]
}

class ConditionArrayTest(unittest.TestCase):
    """测试条件节点对数组类型的处理"""

    def setUp(self):
        """设置测试环境"""
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)

    async def test_empty_array_condition(self):
        """测试空数组条件"""
        print("测试空数组条件...")
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_SCHEMA,
            "inputs": {
                "array": []  # 空数组
            },
        })
        
        # 等待任务完成
        result = await task.processing
        print(f"空数组测试结果: {result}")
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组为空")

    async def test_non_empty_array_condition(self):
        """测试非空数组条件"""
        print("测试非空数组条件...")
        task = self.engine.invoke({
            "schema": EMPTY_ARRAY_SCHEMA,
            "inputs": {
                "array": ["item1", "item2"]  # 非空数组
            },
        })
        
        # 等待任务完成
        result = await task.processing
        print(f"非空数组测试结果: {result}")
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组不为空")

    async def test_complex_workflow_empty_array(self):
        """测试复杂工作流中的空数组条件"""
        print("测试复杂工作流中的空数组条件...")
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],  # 空数组
                "apiKey": "test-key",
                "apiHost": "https://mock-api.com",
                "modelName": "test-model"
            },
        })
        
        # 等待任务完成
        try:
            result = await task.processing
            print(f"复杂工作流空数组测试结果: {result}")
            # 这里不验证具体结果，只要不报错就行
        except Exception as e:
            self.fail(f"复杂工作流测试失败: {e}")

    async def test_complex_workflow_non_empty_array(self):
        """测试复杂工作流中的非空数组条件"""
        print("测试复杂工作流中的非空数组条件...")
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": ["theme1", "theme2"],  # 非空数组
                "apiKey": "test-key",
                "apiHost": "https://mock-api.com",
                "modelName": "test-model"
            },
        })
        
        # 等待任务完成
        try:
            result = await task.processing
            print(f"复杂工作流非空数组测试结果: {result}")
            # 这里不验证具体结果，只要不报错就行
        except Exception as e:
            self.fail(f"复杂工作流测试失败: {e}")

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试用例
    test_cases = [
        ConditionArrayTest('test_empty_array_condition'),
        ConditionArrayTest('test_non_empty_array_condition'),
        ConditionArrayTest('test_complex_workflow_empty_array'),
        ConditionArrayTest('test_complex_workflow_non_empty_array')
    ]
    
    # 将测试用例添加到测试套件
    suite.addTests(test_cases)
    
    # 运行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    # 使用unittest框架运行测试
    run_tests()
