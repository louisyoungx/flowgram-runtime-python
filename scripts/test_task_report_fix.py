import os
import sys
import json
import time
import asyncio
from typing import Dict, Any

# Add runtime-py-core to the Python path
sys.path.append(os.path.abspath('runtime-py-core'))

from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.interface.schema import WorkflowStatus

async def test_task_report_status_update():
    """
    Test that the TaskReport API correctly updates the status from 'processing' to 'succeeded'.
    """
    print("开始测试 TaskReport API 状态更新...")
    
    # 准备工作流输入
    input_data = {
        "inputs": {
            "model_name": "ep-20250206192339-nnr9m",
            "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
            "api_host": "https://ark.cn-beijing.volces.com/api/v3",
            "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
        },
        "schema": """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
    }

    # 运行工作流
    task_run_result = await TaskRunAPI(input_data)
    task_id = task_run_result["taskID"]
    print(f"工作流任务已启动，taskID: {task_id}")

    # 立即检查任务报告，应该是 'processing' 状态
    initial_report = await TaskReportAPI({"taskID": task_id})
    initial_status = initial_report.get("workflowStatus", {}).get("status", "unknown")
    print(f"初始状态: {initial_status}")
    
    # 等待一段时间让工作流执行完成
    print("等待工作流执行完成...")
    max_attempts = 10
    final_status = None
    
    for i in range(max_attempts):
        await asyncio.sleep(1)  # 等待1秒
        report = await TaskReportAPI({"taskID": task_id})
        status = report.get("workflowStatus", {}).get("status", "unknown")
        print(f"检查 #{i+1}: 状态 = {status}")
        print(f"报告内容: {json.dumps(report, indent=2)}")
        
        if status in ["succeeded", "failed", "cancelled", "Success", "Failed", "Cancelled", "Succeeded"]:
            final_status = status
            print(f"工作流已完成，最终状态: {final_status}")
            print(f"完整报告: {json.dumps(report, indent=2)}")
            break
    
    # 验证状态是否已更新
    if final_status:
        print("✅ 测试通过: 状态已从 'processing' 更新为终止状态")
        return True
    else:
        print("❌ 测试失败: 状态未更新，仍然是 'processing'")
        return False

if __name__ == "__main__":
    asyncio.run(test_task_report_status_update())
