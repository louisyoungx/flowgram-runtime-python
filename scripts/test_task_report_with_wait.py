"""
Test script for TaskReport API functionality with longer wait times.
"""
import asyncio
import json
import uuid
import time
from src.api.task_report_api import TaskReportAPI
from src.api.task_run_api import TaskRunAPI

async def test_task_report():
    """Test the TaskReport API functionality with longer wait times."""
    print("测试 TaskReport API 功能...")
    
    # First, run a task to get a task ID
    schema_str = """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""
    
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    task_run_input = {
        "schema": schema_str,
        "inputs": inputs
    }
    
    # Run the task
    task_run_output = await TaskRunAPI(task_run_input)
    task_id = task_run_output["taskID"]
    print(f"任务 ID: {task_id}")
    
    # Wait longer for the task to process (5 seconds)
    print("等待任务处理完成...")
    await asyncio.sleep(5)
    
    # Get the task report
    task_report_input = {
        "taskID": task_id
    }
    
    # Try multiple times to get a complete report
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"尝试获取报告 (尝试 {attempt+1}/{max_attempts})...")
        report = await TaskReportAPI(task_report_input)
        
        # Print the report in a formatted way
        print("\n任务报告:")
        print(json.dumps(report, indent=2))
        
        # Check if we have node reports
        if report and report.get("reports") and len(report["reports"]) > 0:
            print(f"找到 {len(report['reports'])} 个节点报告")
            break
        
        # If not, wait and try again
        if attempt < max_attempts - 1:
            print("报告中没有节点信息，等待更长时间...")
            await asyncio.sleep(3)
    
    # Verify the report structure
    if report:
        print("\n验证报告结构...")
        assert "id" in report, "报告缺少 'id' 字段"
        assert "inputs" in report, "报告缺少 'inputs' 字段"
        assert "outputs" in report, "报告缺少 'outputs' 字段"
        assert "workflowStatus" in report, "报告缺少 'workflowStatus' 字段"
        assert "reports" in report, "报告缺少 'reports' 字段"
        
        # Check inputs
        assert len(report["inputs"]) > 0, "报告输入为空"
        
        # Check workflow status
        assert "status" in report["workflowStatus"], "工作流状态缺少 'status' 字段"
        assert "terminated" in report["workflowStatus"], "工作流状态缺少 'terminated' 字段"
        assert "startTime" in report["workflowStatus"], "工作流状态缺少 'startTime' 字段"
        
        # Check node reports
        if len(report["reports"]) > 0:
            print(f"找到 {len(report['reports'])} 个节点报告")
            for node_id, node_report in report["reports"].items():
                print(f"节点 {node_id}: {node_report.get('status', 'unknown')}")
                assert "id" in node_report, f"节点报告 {node_id} 缺少 'id' 字段"
                assert "status" in node_report, f"节点报告 {node_id} 缺少 'status' 字段"
                assert "terminated" in node_report, f"节点报告 {node_id} 缺少 'terminated' 字段"
                assert "startTime" in node_report, f"节点报告 {node_id} 缺少 'startTime' 字段"
                assert "snapshots" in node_report, f"节点报告 {node_id} 缺少 'snapshots' 字段"
                
                # Check snapshots
                if len(node_report["snapshots"]) > 0:
                    print(f"节点 {node_id} 有 {len(node_report['snapshots'])} 个快照")
                    for snapshot in node_report["snapshots"]:
                        assert "id" in snapshot, "快照缺少 'id' 字段"
                        assert "nodeID" in snapshot, "快照缺少 'nodeID' 字段"
                        assert "inputs" in snapshot, "快照缺少 'inputs' 字段"
        else:
            print("没有找到节点报告")
        
        print("报告结构验证通过!")
    else:
        print("错误: 没有返回报告")

if __name__ == "__main__":
    asyncio.run(test_task_report())