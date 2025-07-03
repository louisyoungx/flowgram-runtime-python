"""
Test script for TaskReportAPI
"""
import asyncio
import json
import logging
import time
import uuid
from typing import Dict, Any

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# 导入必要的模块
from src.api import TaskRunAPI, TaskReportAPI
from src.domain.report.workflow_runtime_reporter import WorkflowRuntimeReport
from src.application.workflow_application import WorkflowApplication


async def test_task_report_api():
    """测试TaskReportAPI"""
    # 准备测试数据
    schema = """
    {
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
                            "model_name": {"key": 14, "name": "model_name", "type": "string", "extra": {"index": 1}, "isPropertyRequired": true},
                            "prompt": {"key": 5, "name": "prompt", "type": "string", "extra": {"index": 3}, "isPropertyRequired": true},
                            "api_key": {"key": 19, "name": "api_key", "type": "string", "extra": {"index": 4}, "isPropertyRequired": true},
                            "api_host": {"key": 20, "name": "api_host", "type": "string", "extra": {"index": 5}, "isPropertyRequired": true}
                        },
                        "required": ["model_name", "prompt", "api_key", "api_host"]
                    }
                }
            },
            {
                "id": "end_0",
                "type": "end",
                "meta": {"position": {"x": 1000, "y": 0}},
                "data": {
                    "title": "End",
                    "inputsValues": {"answer": {"type": "ref", "content": ["llm_0", "result"]}},
                    "inputs": {"type": "object", "properties": {"answer": {"type": "string"}}}
                }
            },
            {
                "id": "llm_0",
                "type": "llm",
                "meta": {"position": {"x": 500, "y": 0}},
                "data": {
                    "title": "LLM_0",
                    "inputsValues": {
                        "modelName": {"type": "ref", "content": ["start_0", "model_name"]},
                        "apiKey": {"type": "ref", "content": ["start_0", "api_key"]},
                        "apiHost": {"type": "ref", "content": ["start_0", "api_host"]},
                        "temperature": {"type": "constant", "content": 0},
                        "prompt": {"type": "ref", "content": ["start_0", "prompt"]},
                        "systemPrompt": {"type": "constant", "content": "You are a helpful AI assistant."}
                    },
                    "inputs": {
                        "type": "object",
                        "required": ["modelName", "temperature", "prompt"],
                        "properties": {
                            "modelName": {"type": "string"},
                            "apiKey": {"type": "string"},
                            "apiHost": {"type": "string"},
                            "temperature": {"type": "number"},
                            "systemPrompt": {"type": "string"},
                            "prompt": {"type": "string"}
                        }
                    },
                    "outputs": {"type": "object", "properties": {"result": {"type": "string"}}}
                }
            }
        ],
        "edges": [
            {"sourceNodeID": "start_0", "targetNodeID": "llm_0"},
            {"sourceNodeID": "llm_0", "targetNodeID": "end_0"}
        ]
    }
    """
    
    inputs = {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # 运行任务
    print("运行任务...")
    task_run_input = {
        "schema": schema,
        "inputs": inputs
    }
    task_run_output = await TaskRunAPI(task_run_input)
    task_id = task_run_output["taskID"]
    print(f"任务ID: {task_id}")
    
    # 等待任务执行
    print("等待任务执行...")
    await asyncio.sleep(1)
    
    # 获取任务报告
    print("获取任务报告...")
    task_report_input = {"taskID": task_id}
    
    # 直接访问应用实例，确保报告生成正确
    app = WorkflowApplication.instance()
    task = app.tasks.get(task_id)
    
    if task:
        print("任务存在，检查上下文...")
        # 检查任务上下文
        context = task.context
        
        # 检查状态中心
        status_center = context.status_center
        workflow_status = status_center.workflow
        print(f"工作流状态: {workflow_status.status}")
        print(f"工作流终止: {workflow_status.terminated}")
        print(f"工作流开始时间: {workflow_status.startTime}")
        print(f"工作流结束时间: {workflow_status.endTime}")
        print(f"工作流耗时: {workflow_status.timeCost}")
        
        # 检查节点状态
        node_statuses = {}
        if hasattr(status_center, 'export_node_status'):
            node_statuses = status_center.export_node_status()
            print(f"节点状态数量: {len(node_statuses)}")
            for node_id, status in node_statuses.items():
                print(f"节点 {node_id} 状态: {status}")
        else:
            print("状态中心没有export_node_status方法")
        
        # 检查快照中心
        snapshot_center = context.snapshot_center
        snapshots = {}
        if hasattr(snapshot_center, 'export'):
            snapshots = snapshot_center.export()
            print(f"快照数量: {len(snapshots)}")
            for node_id, node_snapshots in snapshots.items():
                print(f"节点 {node_id} 快照数量: {len(node_snapshots)}")
        else:
            print("快照中心没有export方法")
        
        # 检查IO中心
        io_center = context.io_center
        print(f"输入: {io_center._inputs}")
        print(f"输出: {io_center._outputs}")
        
        # 直接生成报告
        report = context.reporter.export()
        print("直接生成的报告:")
        print(f"报告ID: {report.id}")
        print(f"报告输入: {report.inputs}")
        print(f"报告输出: {report.outputs}")
        print(f"报告工作流状态: {report.workflowStatus}")
        print(f"报告节点数量: {len(report.reports)}")
        for node_id, node_report in report.reports.items():
            print(f"节点 {node_id} 报告: {node_report}")
    else:
        print(f"任务 {task_id} 不存在")
    
    # 使用API获取报告
    report_data = await TaskReportAPI(task_report_input)
    
    # 打印报告数据
    print("\n通过API获取的报告数据:")
    print(f"报告ID: {report_data.get('id', '')}")
    print(f"报告输入: {report_data.get('inputs', {})}")
    print(f"报告输出: {report_data.get('outputs', {})}")
    print(f"报告工作流状态: {report_data.get('workflowStatus', {})}")
    print(f"报告节点数量: {len(report_data.get('reports', {}))}")
    
    # 将报告数据格式化为JSON字符串
    report_json = json.dumps(report_data, indent=2)
    print("\n报告JSON:")
    print(report_json)
    
    # 检查报告是否符合预期
    if report_data.get('id') == task_id:
        print("\n✅ 报告ID正确")
    else:
        print(f"\n❌ 报告ID不正确: {report_data.get('id')} != {task_id}")
    
    if report_data.get('inputs') == inputs:
        print("✅ 报告输入正确")
    else:
        print(f"❌ 报告输入不正确: {report_data.get('inputs')} != {inputs}")
    
    if report_data.get('workflowStatus', {}).get('status'):
        print(f"✅ 报告工作流状态正确: {report_data.get('workflowStatus', {}).get('status')}")
    else:
        print("❌ 报告工作流状态不正确")
    
    if len(report_data.get('reports', {})) > 0:
        print(f"✅ 报告包含节点报告: {len(report_data.get('reports', {}))} 个节点")
    else:
        print("❌ 报告不包含节点报告")
    
    return report_data


if __name__ == "__main__":
    # 运行测试
    report = asyncio.run(test_task_report_api())