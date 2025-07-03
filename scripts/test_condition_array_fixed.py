"""
Test script for condition node with array type and is_empty/is_not_empty operators.
"""
import json
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath("./"))

from runtime_py_core.src.interface import WorkflowStatus
from runtime_py_core.src.application import WorkflowApplication

def print_section(title):
    print(f"\n{'='*10} {title} {'='*10}")

async def main():
    # 定义一个简单的工作流，包含条件节点和数组类型
    schema = {
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
                            }
                        },
                        "required": ["themes"]
                    }
                }
            },
            {
                "id": "end_0",
                "type": "end",
                "meta": {"position": {"x": 800, "y": 346}},
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
                "meta": {"position": {"x": 500, "y": 346}},
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
                "meta": {"position": {"x": 650, "y": 200}},
                "data": {
                    "title": "LLM Empty",
                    "inputsValues": {
                        "modelName": {"type": "constant", "content": "test-model"},
                        "apiKey": {"type": "constant", "content": "test-key"},
                        "apiHost": {"type": "constant", "content": "https://mock-ai-url/api/v3"},
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
                "id": "llm_not_empty",
                "type": "llm",
                "meta": {"position": {"x": 650, "y": 500}},
                "data": {
                    "title": "LLM Not Empty",
                    "inputsValues": {
                        "modelName": {"type": "constant", "content": "test-model"},
                        "apiKey": {"type": "constant", "content": "test-key"},
                        "apiHost": {"type": "constant", "content": "https://mock-ai-url/api/v3"},
                        "temperature": {"type": "constant", "content": 0.5},
                        "systemPrompt": {"type": "constant", "content": "You are an AI assistant."},
                        "prompt": {"type": "constant", "content": "数组不为空"}
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
            {"sourceNodeID": "start_0", "targetNodeID": "condition_0"},
            {"sourceNodeID": "condition_0", "targetNodeID": "llm_empty", "sourcePortID": "if_empty"},
            {"sourceNodeID": "condition_0", "targetNodeID": "llm_not_empty", "sourcePortID": "if_not_empty"},
            {"sourceNodeID": "llm_empty", "targetNodeID": "end_0"},
            {"sourceNodeID": "llm_not_empty", "targetNodeID": "end_0"}
        ]
    }

    from runtime_py_core.src.domain.container import WorkflowRuntimeContainer
    from runtime_py_core.src.interface import IEngine

    # 获取引擎实例
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)

    # 测试空数组
    print_section("Testing with empty array")
    task_empty = engine.invoke({
        "schema": schema,
        "inputs": {"themes": []}
    })
    
    # 等待任务完成
    result_empty = await task_empty.processing
    
    print(f"Task ID: {task_empty.id}")
    print(f"Workflow status: {task_empty.context.status_center.workflow.status}")
    print(f"Inputs: {task_empty.context.io_center.inputs}")
    print(f"Outputs: {task_empty.context.io_center.outputs}")
    print(f"Branch taken: {task_empty.context.snapshot_center.export_all()[1].get('branch', 'No branch')}")
    
    # 测试非空数组
    print_section("Testing with non-empty array")
    task_not_empty = engine.invoke({
        "schema": schema,
        "inputs": {"themes": ["主题1", "主题2"]}
    })
    
    # 等待任务完成
    result_not_empty = await task_not_empty.processing
    
    print(f"Task ID: {task_not_empty.id}")
    print(f"Workflow status: {task_not_empty.context.status_center.workflow.status}")
    print(f"Inputs: {task_not_empty.context.io_center.inputs}")
    print(f"Outputs: {task_not_empty.context.io_center.outputs}")
    print(f"Branch taken: {task_not_empty.context.snapshot_center.export_all()[1].get('branch', 'No branch')}")
    
    # 测试复杂工作流
    print_section("Testing complex workflow")
    
    # 定义复杂工作流的schema
    complex_schema = {
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
    
    # 测试空数组的复杂工作流
    task_complex_empty = engine.invoke({
        "schema": complex_schema,
        "inputs": {
            "themes": [],
            "apiKey": "test-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    # 等待任务完成
    result_complex_empty = await task_complex_empty.processing
    
    print(f"Task ID: {task_complex_empty.id}")
    print(f"Workflow status: {task_complex_empty.context.status_center.workflow.status}")
    print(f"Inputs: {task_complex_empty.context.io_center.inputs}")
    print(f"Outputs: {task_complex_empty.context.io_center.outputs}")
    print(f"Branch taken: {task_complex_empty.context.snapshot_center.export_all()[1].get('branch', 'No branch')}")
    
    # 测试非空数组的复杂工作流
    complex_schema["edges"].append(
        {"sourceNodeID": "condition_Ts3zx", "targetNodeID": "end_0", "sourcePortID": "if_pTr8_"}
    )
    
    task_complex_not_empty = engine.invoke({
        "schema": complex_schema,
        "inputs": {
            "themes": ["露营", "登山", "滑雪", "徒步"],
            "apiKey": "test-key",
            "apiHost": "https://mock-ai-url/api/v3",
            "modelName": "test-model"
        }
    })
    
    # 等待任务完成
    result_complex_not_empty = await task_complex_not_empty.processing
    
    print(f"Task ID: {task_complex_not_empty.id}")
    print(f"Workflow status: {task_complex_not_empty.context.status_center.workflow.status}")
    print(f"Inputs: {task_complex_not_empty.context.io_center.inputs}")
    print(f"Outputs: {task_complex_not_empty.context.io_center.outputs}")
    print(f"Branch taken: {task_complex_not_empty.context.snapshot_center.export_all()[1].get('branch', 'No branch')}")

if __name__ == "__main__":
    asyncio.run(main())