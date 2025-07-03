import os
import sys
import asyncio
import unittest
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))

from src.interface import IEngine, IContainer, WorkflowStatus
from src.domain.container import WorkflowRuntimeContainer

# 简单工作流定义 - 测试空数组条件
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
            "id": "end_1",
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
            "id": "end_2",
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
        {"sourceNodeID": "condition_0", "targetNodeID": "end_1", "sourcePortID": "if_empty"},
        {"sourceNodeID": "condition_0", "targetNodeID": "end_2", "sourcePortID": "if_not_empty"}
    ]
}

# 复杂工作流定义 - 测试数组条件和循环
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

class ConditionArrayTest(unittest.TestCase):
    def setUp(self):
        self.container = WorkflowRuntimeContainer.instance()
        self.engine = self.container.get(IEngine)
    
    async def test_empty_array_condition(self):
        """测试空数组的条件处理"""
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": []  # 空数组
            }
        })
        
        # 等待任务完成
        result = await task.processing
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组为空")
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # 打印调试信息
        print(f"Empty Array Test - Result: {result}")
        print(f"Empty Array Test - Status: {task.context.status_center.workflow.status}")
    
    async def test_non_empty_array_condition(self):
        """测试非空数组的条件处理"""
        task = self.engine.invoke({
            "schema": SIMPLE_WORKFLOW_SCHEMA,
            "inputs": {
                "array_data": ["item1", "item2"]  # 非空数组
            }
        })
        
        # 等待任务完成
        result = await task.processing
        
        # 验证结果
        self.assertEqual(result.get("result"), "数组不为空")
        self.assertEqual(task.context.status_center.workflow.status, WorkflowStatus.Succeeded)
        
        # 打印调试信息
        print(f"Non-Empty Array Test - Result: {result}")
        print(f"Non-Empty Array Test - Status: {task.context.status_center.workflow.status}")
    
    async def test_complex_workflow_empty_array(self):
        """测试复杂工作流中的空数组条件"""
        task = self.engine.invoke({
            "schema": COMPLEX_WORKFLOW_SCHEMA,
            "inputs": {
                "themes": [],  # 空数组
                "apiKey": "test-api-key",
                "apiHost": "https://mock-ai-url/api/v3",
                "modelName": "test-model"
            }
        })
        
        try:
            # 等待任务完成
            result = await task.processing
            
            # 打印调试信息
            print(f"Complex Workflow Empty Array Test - Result: {result}")
            print(f"Complex Workflow Empty Array Test - Status: {task.context.status_center.workflow.status}")
            
            # 验证空数组条件分支被执行
            snapshots = task.context.snapshot_center.export_all()
            condition_snapshot = next((s for s in snapshots if s.node_id == "condition_Ts3zx"), None)
            
            if condition_snapshot:
                print(f"Condition branch: {condition_snapshot.branch}")
                self.assertEqual(condition_snapshot.branch, "if_OVHXT")
            else:
                print("No condition snapshot found")
                self.fail("No condition snapshot found")
        except Exception as e:
            print(f"Error in complex workflow test: {e}")
            raise

def run_tests():
    """运行所有测试"""
    test_cases = [
        ConditionArrayTest("test_empty_array_condition"),
        ConditionArrayTest("test_non_empty_array_condition"),
        ConditionArrayTest("test_complex_workflow_empty_array")
    ]
    
    for test_case in test_cases:
        test_case.setUp()  # 初始化测试环境
        
        # 运行测试方法
        test_method = getattr(test_case, test_case._testMethodName)
        try:
            print(f"\n运行测试: {test_case._testMethodName}")
            asyncio.run(test_method())
            print(f"✅ 测试通过: {test_case._testMethodName}")
        except Exception as e:
            print(f"❌ 测试失败: {test_case._testMethodName}")
            print(f"错误信息: {e}")

if __name__ == "__main__":
    print("开始测试条件节点对数组类型和 is_empty/is_not_empty 操作符的处理...")
    run_tests()
    print("\n测试完成")