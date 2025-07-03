"""
Test script to debug condition node handling of array types with is_empty/is_not_empty operators.
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, List

# Add the runtime-py-core directory to the Python path
sys.path.append(os.path.abspath("runtime-py-core"))

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath("."))
from runtime_py_core.src.interface import IEngine, IContainer, WorkflowStatus
from runtime_py_core.src.domain.container import WorkflowRuntimeContainer

# Define test schemas
empty_array_schema = {
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
                        "array_value": {
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
                            "left": {"type": "ref", "content": ["start_0", "array_value"]},
                            "operator": "is_empty"
                        },
                        "key": "if_empty"
                    },
                    {
                        "value": {
                            "left": {"type": "ref", "content": ["start_0", "array_value"]},
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
                    "result": {"type": "constant", "content": "Array is empty"}
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
                    "result": {"type": "constant", "content": "Array is not empty"}
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

async def test_condition_with_empty_array():
    """Test condition node with empty array."""
    print("Testing condition node with empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with empty array
    task = engine.invoke({
        "schema": empty_array_schema,
        "inputs": {
            "array_value": []
        }
    })
    
    print(f"Task ID: {task.id}")
    print(f"Initial status: {task.context.status_center.workflow.status}")
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Final status: {task.context.status_center.workflow.status}")
    print(f"Result: {result}")
    
    # Get branch from condition node snapshot
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_snapshot = condition_snapshots[0]
        branch = condition_snapshot.branch if hasattr(condition_snapshot, "branch") else None
        print(f"Condition branch: {branch}")
    else:
        print("No condition snapshot found")
    
    return result

async def test_condition_with_non_empty_array():
    """Test condition node with non-empty array."""
    print("\nTesting condition node with non-empty array...")
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with non-empty array
    task = engine.invoke({
        "schema": empty_array_schema,
        "inputs": {
            "array_value": ["item1", "item2"]
        }
    })
    
    print(f"Task ID: {task.id}")
    print(f"Initial status: {task.context.status_center.workflow.status}")
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Final status: {task.context.status_center.workflow.status}")
    print(f"Result: {result}")
    
    # Get branch from condition node snapshot
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_0"]
    
    if condition_snapshots:
        condition_snapshot = condition_snapshots[0]
        branch = condition_snapshot.branch if hasattr(condition_snapshot, "branch") else None
        print(f"Condition branch: {branch}")
    else:
        print("No condition snapshot found")
    
    return result

async def test_complex_workflow():
    """Test the complex workflow from the curl request."""
    print("\nTesting complex workflow...")
    
    # Load the complex schema from the curl request
    complex_schema_str = """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":180,"y":346}},"data":{"title":"Start","outputs":{"type":"object","properties":{"themes":{"key":5,"name":"themes","isPropertyRequired":true,"type":"array","extra":{"index":0},"items":{"type":"string"}},"apiKey":{"key":7,"name":"apiKey","isPropertyRequired":true,"type":"string","extra":{"index":1}},"apiHost":{"key":8,"name":"apiHost","isPropertyRequired":true,"type":"string","extra":{"index":2}},"modelName":{"key":12,"name":"modelName","isPropertyRequired":true,"type":"string","extra":{"index":3}}},"required":["themes","apiKey","apiHost","modelName"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":2258.6,"y":346}},"data":{"title":"End","inputs":{"type":"object","properties":{"result":{"type":"string"}}}}},{"id":"condition_Ts3zx","type":"condition","meta":{"position":{"x":640,"y":282.5}},"data":{"title":"Condition","conditions":[{"value":{"left":{"type":"ref","content":["start_0","themes"]},"operator":"is_empty"},"key":"if_OVHXT"},{"value":{"left":{"type":"ref","content":["start_0","themes"]},"operator":"is_not_empty"},"key":"if_pTr8_"}]}},{"id":"llm_FKRbD","type":"llm","meta":{"position":{"x":1449.3,"y":0}},"data":{"title":"LLM_1","inputsValues":{"modelName":{"type":"ref","content":["start_0","modelName"]},"apiKey":{"type":"ref","content":["start_0","apiKey"]},"apiHost":{"type":"ref","content":["start_0","apiHost"]},"temperature":{"type":"constant","content":0.5},"systemPrompt":{"type":"constant","content":"You are an AI assistant."},"prompt":{"type":"constant","content":"没填参数就失败了"}},"inputs":{"type":"object","required":["modelName","apiKey","apiHost","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}},{"id":"loop_2OD2p","type":"loop","meta":{"position":{"x":1020,"y":483}},"data":{"title":"Loop_1","batchFor":{"type":"ref","content":["start_0","themes"]}},"blocks":[{"id":"832659","type":"llm","meta":{"position":{"x":189.65,"y":0}},"data":{"title":"LLM_1","inputsValues":{"modelName":{"type":"ref","content":["start_0","modelName"]},"apiKey":{"type":"ref","content":["start_0","apiKey"]},"apiHost":{"type":"ref","content":["start_0","apiHost"]},"temperature":{"type":"constant","content":0.6},"systemPrompt":{"type":"constant","content":"用户会传入一个 prompt，你需要将这个prompt扩写为一个完整的标题，例如输入"露营"，返回"在瑞士阿尔卑斯山的露营之旅""},"prompt":{"type":"ref","content":["loop_2OD2p_locals","item"]}},"inputs":{"type":"object","required":["modelName","apiKey","apiHost","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}},{"id":"llm_KYkc0","type":"llm","meta":{"position":{"x":668.95,"y":0}},"data":{"title":"LLM_4","inputsValues":{"modelName":{"type":"ref","content":["start_0","modelName"]},"apiKey":{"type":"ref","content":["start_0","apiKey"]},"apiHost":{"type":"ref","content":["start_0","apiHost"]},"temperature":{"type":"constant","content":0.6},"systemPrompt":{"type":"constant","content":"用户传入的是一个标题，你需要根据这个标题生成一个小于50字的简短的介绍"},"prompt":{"type":"ref","content":["832659","result"]}},"inputs":{"type":"object","required":["modelName","apiKey","apiHost","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"832659","targetNodeID":"llm_KYkc0"}]},{"id":"135409","type":"comment","meta":{"position":{"x":370.5603139013452,"y":590.6292974588938}},"data":{"size":{"width":454.75261584454404,"height":282.5863976083707},"note":"{\n  \"modelName\": \"ep-20250206192339-nnr9m\",\n  \"apiKey\": \"c5720be8-e02d-4584-8cd7-27bcbcc14dab\",\n  \"apiHost\": \"https://ark.cn-beijing.volces.com/api/v3\",\n  \"themes\": [\n    \"露营\",\n    \"登山\",\n    \"滑雪\",\n    \"徒步\"\n  ]\n}"}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"condition_Ts3zx"},{"sourceNodeID":"llm_FKRbD","targetNodeID":"end_0"},{"sourceNodeID":"loop_2OD2p","targetNodeID":"end_0"},{"sourceNodeID":"condition_Ts3zx","targetNodeID":"llm_FKRbD","sourcePortID":"if_OVHXT"},{"sourceNodeID":"condition_Ts3zx","targetNodeID":"loop_2OD2p","sourcePortID":"if_pTr8_"}]}"""
    complex_schema = json.loads(complex_schema_str)
    
    container = WorkflowRuntimeContainer.instance()
    engine = container.get(IEngine)
    
    # Test with empty themes array
    print("Testing with empty themes array...")
    task = engine.invoke({
        "schema": complex_schema,
        "inputs": {
            "modelName": "ep-20250206192339-nnr9m",
            "apiKey": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
            "apiHost": "https://ark.cn-beijing.volces.com/api/v3",
            "themes": []
        }
    })
    
    print(f"Task ID: {task.id}")
    print(f"Initial status: {task.context.status_center.workflow.status}")
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Final status: {task.context.status_center.workflow.status}")
    print(f"Result: {result}")
    
    # Get branch from condition node snapshot
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
    
    if condition_snapshots:
        condition_snapshot = condition_snapshots[0]
        branch = condition_snapshot.branch if hasattr(condition_snapshot, "branch") else None
        print(f"Condition branch: {branch}")
    else:
        print("No condition snapshot found")
    
    # Test with non-empty themes array
    print("\nTesting with non-empty themes array...")
    task = engine.invoke({
        "schema": complex_schema,
        "inputs": {
            "modelName": "ep-20250206192339-nnr9m",
            "apiKey": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
            "apiHost": "https://ark.cn-beijing.volces.com/api/v3",
            "themes": ["露营", "登山", "滑雪", "徒步"]
        }
    })
    
    print(f"Task ID: {task.id}")
    print(f"Initial status: {task.context.status_center.workflow.status}")
    
    # Wait for task to complete
    result = await task.processing
    
    print(f"Final status: {task.context.status_center.workflow.status}")
    print(f"Result: {result}")
    
    # Get branch from condition node snapshot
    snapshots = task.context.snapshot_center.export_all()
    condition_snapshots = [s for s in snapshots if s.node_id == "condition_Ts3zx"]
    
    if condition_snapshots:
        condition_snapshot = condition_snapshots[0]
        branch = condition_snapshot.branch if hasattr(condition_snapshot, "branch") else None
        print(f"Condition branch: {branch}")
    else:
        print("No condition snapshot found")
    
    return result

async def main():
    """Main function to run all tests."""
    # Test condition node with empty array
    await test_condition_with_empty_array()
    
    # Test condition node with non-empty array
    await test_condition_with_non_empty_array()
    
    # Test complex workflow
    await test_complex_workflow()

if __name__ == "__main__":
    asyncio.run(main())
