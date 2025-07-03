import json
import sys
import os
import asyncio

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 导入 WorkflowApplication
from src.application.workflow_application import WorkflowApplication

def test_workflow_application():
    """直接测试 WorkflowApplication"""
    print("测试 WorkflowApplication...")
    
    # 获取 WorkflowApplication 实例
    app = WorkflowApplication.instance()
    
    # 准备输入数据
    schema_str = """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # 解析 schema
    schema = json.loads(schema_str)
    
    try:
        # 运行工作流
        task_id = app.run({
            "schema": schema,
            "inputs": inputs,
        })
        print(f"任务ID: {task_id}")
        
        # 等待一段时间，让任务有时间执行
        print("等待任务执行...")
        import time
        time.sleep(2)
        
        # 获取任务结果
        result = app.result(task_id)
        print(f"任务结果: {result}")
        
        # 获取任务报告
        report = app.report(task_id)
        print(f"任务报告: {report}")
        
        # 取消任务
        cancel_result = app.cancel(task_id)
        print(f"取消任务结果: {cancel_result}")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 确保有事件循环可用
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    # 运行测试
    test_workflow_application()