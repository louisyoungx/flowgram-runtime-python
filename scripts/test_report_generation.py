"""
Test script for report generation.
This script directly tests the report generation functionality by creating a mock workflow context
and manually adding node statuses and snapshots.
"""
import asyncio
import json
import time
import uuid
from src.domain.context import WorkflowRuntimeContext
from src.domain.report import WorkflowRuntimeReport
from src.interface.schema import InvokeParams

async def test_report_generation():
    """Test the report generation functionality."""
    print("测试报告生成功能...")
    
    # Create a mock workflow context
    params = {
        "schema": {
            "nodes": [
                {
                    "id": "start_0",
                    "type": "start",
                    "data": {"title": "Start"},
                },
                {
                    "id": "llm_0",
                    "type": "llm",
                    "data": {"title": "LLM"},
                },
                {
                    "id": "end_0",
                    "type": "end",
                    "data": {"title": "End"},
                },
            ],
            "edges": [
                {"sourceNodeID": "start_0", "targetNodeID": "llm_0"},
                {"sourceNodeID": "llm_0", "targetNodeID": "end_0"},
            ],
        },
        "inputs": {
            "model_name": "test-model",
            "prompt": "test prompt",
        },
    }
    
    # Create the context
    context = WorkflowRuntimeContext.create()
    context.init(params)
    
    # Set workflow status
    import time
    context.status_center.workflow.process()
    context.status_center.workflow._start_time = int(time.time() * 1000)
    
    # Set node statuses
    for node_id in ["start_0", "llm_0", "end_0"]:
        node_status = context.status_center.node_status(node_id)
        node_status.process()
        node_status._start_time = int(time.time() * 1000)
        await asyncio.sleep(0.1)  # Small delay to make times different
        node_status.success()
        node_status._end_time = int(time.time() * 1000)
    
    # Create snapshots
    for node_id in ["start_0", "llm_0", "end_0"]:
        snapshot_id = str(uuid.uuid4())
        snapshot = context.snapshot_center.create({
            "id": snapshot_id,
            "node_id": node_id,
            "data": {"title": f"Node {node_id}"},
            "inputs": {"input": f"Input for {node_id}"},
        })
        snapshot.add_data({"outputs": {"output": f"Output from {node_id}"}})
    
    # Set workflow status to success
    context.status_center.workflow.success()
    context.status_center.workflow._end_time = int(time.time() * 1000)
    
    # Generate the report
    report = context.reporter.export()
    
    # Print the report
    if isinstance(report, WorkflowRuntimeReport):
        report_dict = {
            "id": getattr(report, "id", ""),
            "inputs": getattr(report, "inputs", {}),
            "outputs": getattr(report, "outputs", {}),
            "workflowStatus": getattr(report, "workflowStatus", {}),
            "reports": getattr(report, "reports", {})
        }
        print("\n生成的报告:")
        print(json.dumps(report_dict, indent=2))
        
        # Check if we have node reports
        if report_dict.get("reports") and len(report_dict["reports"]) > 0:
            print(f"找到 {len(report_dict['reports'])} 个节点报告")
            for node_id, node_report in report_dict["reports"].items():
                print(f"节点 {node_id}: {node_report.get('status', 'unknown')}")
                print(f"  快照数量: {len(node_report.get('snapshots', []))}")
        else:
            print("没有找到节点报告")
    else:
        print("错误: 报告不是 WorkflowRuntimeReport 类型")

if __name__ == "__main__":
    asyncio.run(test_report_generation())