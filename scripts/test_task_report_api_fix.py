import asyncio
import json
import logging
import sys
from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_task_report_api():
    # 测试数据
    schema_str = """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # 测试 TaskRunAPI
    print("测试 TaskRunAPI...")
    run_input = {"schema": schema_str, "inputs": inputs}
    run_output = await TaskRunAPI(run_input)
    task_id = run_output["taskID"]
    print(f"TaskRunAPI 成功, taskID: {task_id}")
    
    # 立即测试 TaskReportAPI
    print(f"测试 TaskReportAPI, taskID: {task_id}...")
    report_input = {"taskID": task_id}
    report_output = await TaskReportAPI(report_input)
    print(f"TaskReportAPI 响应: {json.dumps(report_output, indent=4, ensure_ascii=False)}")
    
    # 等待一段时间后再次测试 TaskReportAPI
    print("等待3秒后再次测试 TaskReportAPI...")
    await asyncio.sleep(3)
    report_output = await TaskReportAPI(report_input)
    print(f"3秒后 TaskReportAPI 响应: {json.dumps(report_output, indent=4, ensure_ascii=False)}")

if __name__ == "__main__":
    asyncio.run(test_task_report_api())