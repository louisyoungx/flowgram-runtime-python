"""
最终验证测试脚本，用于确认TaskReport API修复是否在实际环境中正常工作
"""
import os
import sys
import json
import time
import asyncio
import requests
from typing import Dict, Any, Optional

# 添加runtime-py-core到Python路径
sys.path.append(os.path.abspath('runtime-py-core'))

# 直接使用API函数进行测试
from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI

# 测试数据 - 与curl命令中使用的相同
TEST_INPUT = {
    "inputs": {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    },
    "schema": """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
}

async def test_direct_api_calls():
    """直接调用API函数进行测试"""
    print("=== 测试1: 直接调用API函数 ===")
    
    # 运行工作流
    print("运行工作流...")
    task_run_result = await TaskRunAPI(TEST_INPUT)
    task_id = task_run_result["taskID"]
    print(f"工作流任务已启动，taskID: {task_id}")
    
    # 立即检查任务报告
    initial_report = await TaskReportAPI({"taskID": task_id})
    initial_status = initial_report.get("workflowStatus", {}).get("status", "unknown")
    print(f"初始状态: {initial_status}")
    
    # 等待工作流执行完成
    print("等待工作流执行完成...")
    max_attempts = 10
    final_status = None
    
    for i in range(max_attempts):
        await asyncio.sleep(1)  # 等待1秒
        report = await TaskReportAPI({"taskID": task_id})
        status = report.get("workflowStatus", {}).get("status", "unknown")
        print(f"检查 #{i+1}: 状态 = {status}")
        
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

def simulate_curl_requests():
    """模拟curl请求进行测试"""
    print("\n=== 测试2: 模拟curl请求 ===")
    
    # 这个函数在当前环境中可能无法执行，因为我们无法启动HTTP服务器
    # 但我们可以提供代码，用户可以在自己的环境中运行
    print("注意: 此测试需要在本地环境中运行，确保FastAPI服务器已启动在 http://localhost:4000")
    
    # 模拟TaskRun请求
    print("模拟 TaskRun 请求...")
    task_run_code = """
    import requests
    import json
    import time
    
    # TaskRun请求
    response = requests.post(
        'http://localhost:4000/api/task/run',
        headers={'Content-Type': 'application/json'},
        json={
            "inputs": {
                "model_name": "ep-20250206192339-nnr9m",
                "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
                "api_host": "https://ark.cn-beijing.volces.com/api/v3",
                "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
            },
            "schema": "{\\"nodes\\":[{\\"id\\":\\"start_0\\",\\"type\\":\\"start\\",\\"meta\\":{\\"position\\":{\\"x\\":0,\\"y\\":0}},\\"data\\":{\\"title\\":\\"Start\\",\\"outputs\\":{\\"type\\":\\"object\\",\\"properties\\":{\\"model_name\\":{\\"key\\":14,\\"name\\":\\"model_name\\",\\"type\\":\\"string\\",\\"extra\\":{\\"index\\":1},\\"isPropertyRequired\\":true},\\"prompt\\":{\\"key\\":5,\\"name\\":\\"prompt\\",\\"type\\":\\"string\\",\\"extra\\":{\\"index\\":3},\\"isPropertyRequired\\":true},\\"api_key\\":{\\"key\\":19,\\"name\\":\\"api_key\\",\\"type\\":\\"string\\",\\"extra\\":{\\"index\\":4},\\"isPropertyRequired\\":true},\\"api_host\\":{\\"key\\":20,\\"name\\":\\"api_host\\",\\"type\\":\\"string\\",\\"extra\\":{\\"index\\":5},\\"isPropertyRequired\\":true}},\\"required\\":[\\"model_name\\",\\"prompt\\",\\"api_key\\",\\"api_host\\"]}}},{\\"id\\":\\"end_0\\",\\"type\\":\\"end\\",\\"meta\\":{\\"position\\":{\\"x\\":1000,\\"y\\":0}},\\"data\\":{\\"title\\":\\"End\\",\\"inputsValues\\":{\\"answer\\":{\\"type\\":\\"ref\\",\\"content\\":[\\"llm_0\\",\\"result\\"]}},\\"inputs\\":{\\"type\\":\\"object\\",\\"properties\\":{\\"answer\\":{\\"type\\":\\"string\\"}}}}},{\\"id\\":\\"llm_0\\",\\"type\\":\\"llm\\",\\"meta\\":{\\"position\\":{\\"x\\":500,\\"y\\":0}},\\"data\\":{\\"title\\":\\"LLM_0\\",\\"inputsValues\\":{\\"modelName\\":{\\"type\\":\\"ref\\",\\"content\\":[\\"start_0\\",\\"model_name\\"]},\\"apiKey\\":{\\"type\\":\\"ref\\",\\"content\\":[\\"start_0\\",\\"api_key\\"]},\\"apiHost\\":{\\"type\\":\\"ref\\",\\"content\\":[\\"start_0\\",\\"api_host\\"]},\\"temperature\\":{\\"type\\":\\"constant\\",\\"content\\":0},\\"prompt\\":{\\"type\\":\\"ref\\",\\"content\\":[\\"start_0\\",\\"prompt\\"]},\\"systemPrompt\\":{\\"type\\":\\"constant\\",\\"content\\":\\"You are a helpful AI assistant.\\"}},\\"inputs\\":{\\"type\\":\\"object\\",\\"required\\":[\\"modelName\\",\\"temperature\\",\\"prompt\\"],\\"properties\\":{\\"modelName\\":{\\"type\\":\\"string\\"},\\"apiKey\\":{\\"type\\":\\"string\\"},\\"apiHost\\":{\\"type\\":\\"string\\"},\\"temperature\\":{\\"type\\":\\"number\\"},\\"systemPrompt\\":{\\"type\\":\\"string\\"},\\"prompt\\":{\\"type\\":\\"string\\"}}},\\"outputs\\":{\\"type\\":\\"object\\",\\"properties\\":{\\"result\\":{\\"type\\":\\"string\\"}}}}}}],\\"edges\\":[{\\"sourceNodeID\\":\\"start_0\\",\\"targetNodeID\\":\\"llm_0\\"},{\\"sourceNodeID\\":\\"llm_0\\",\\"targetNodeID\\":\\"end_0\\"}]}"
        }
    )
    
    task_run_result = response.json()
    task_id = task_run_result["taskID"]
    print(f"工作流任务已启动，taskID: {task_id}")
    
    # 等待工作流执行完成
    max_attempts = 10
    final_status = None
    
    for i in range(max_attempts):
        time.sleep(1)  # 等待1秒
        
        # TaskReport请求
        report_response = requests.get(f'http://localhost:4000/api/task/report?taskID={task_id}')
        report = report_response.json()
        status = report.get("workflowStatus", {}).get("status", "unknown")
        print(f"检查 #{i+1}: 状态 = {status}")
        
        if status in ["succeeded", "failed", "cancelled", "Success", "Failed", "Cancelled", "Succeeded"]:
            final_status = status
            print(f"工作流已完成，最终状态: {final_status}")
            print(f"完整报告: {json.dumps(report, indent=2)}")
            break
    
    # 验证状态是否已更新
    if final_status:
        print("✅ 测试通过: 状态已从 'processing' 更新为终止状态")
    else:
        print("❌ 测试失败: 状态未更新，仍然是 'processing'")
    """
    
    print("请在本地环境中运行以下Python代码：")
    print(task_run_code)

async def main():
    """主函数"""
    print("开始最终验证测试...")
    
    # 测试1: 直接调用API函数
    api_test_result = await test_direct_api_calls()
    
    # 测试2: 模拟curl请求（提供代码，用户可以在自己的环境中运行）
    simulate_curl_requests()
    
    print("\n=== 测试总结 ===")
    if api_test_result:
        print("✅ 直接API调用测试通过: TaskReport API能够正确返回工作流的最终状态")
        print("✅ 修复已成功应用，TaskReport API不再永远返回'processing'状态")
    else:
        print("❌ 直接API调用测试失败: TaskReport API可能仍有问题")
    
    print("\n对于HTTP请求测试，请在本地环境中运行提供的代码，确保FastAPI服务器已启动。")

if __name__ == "__main__":
    asyncio.run(main())