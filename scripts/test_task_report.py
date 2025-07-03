"""
Test script for TaskReport API functionality.
"""
import asyncio
import json
import uuid
from src.api.task_report_api import TaskReportAPI
from src.api.task_run_api import TaskRunAPI

async def test_task_report():
    """Test the TaskReport API functionality."""
    print("Testing TaskReport API...")
    
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
    print(f"Task ID: {task_id}")
    
    # Wait a bit for the task to process
    await asyncio.sleep(1)
    
    # Get the task report
    task_report_input = {
        "taskID": task_id
    }
    
    report = await TaskReportAPI(task_report_input)
    
    # Print the report in a formatted way
    print("\nTask Report:")
    print(json.dumps(report, indent=2))
    
    # Verify the report structure
    if report:
        print("\nVerifying report structure...")
        assert "id" in report, "Report missing 'id' field"
        assert "inputs" in report, "Report missing 'inputs' field"
        assert "outputs" in report, "Report missing 'outputs' field"
        assert "workflowStatus" in report, "Report missing 'workflowStatus' field"
        assert "reports" in report, "Report missing 'reports' field"
        
        # Check inputs
        assert len(report["inputs"]) > 0, "Report inputs is empty"
        
        # Check workflow status
        assert "status" in report["workflowStatus"], "WorkflowStatus missing 'status' field"
        assert "terminated" in report["workflowStatus"], "WorkflowStatus missing 'terminated' field"
        assert "startTime" in report["workflowStatus"], "WorkflowStatus missing 'startTime' field"
        
        # Check node reports
        if len(report["reports"]) > 0:
            print(f"Found {len(report['reports'])} node reports")
            for node_id, node_report in report["reports"].items():
                print(f"Node {node_id}: {node_report['status']}")
                assert "id" in node_report, f"Node report {node_id} missing 'id' field"
                assert "status" in node_report, f"Node report {node_id} missing 'status' field"
                assert "terminated" in node_report, f"Node report {node_id} missing 'terminated' field"
                assert "startTime" in node_report, f"Node report {node_id} missing 'startTime' field"
                assert "snapshots" in node_report, f"Node report {node_id} missing 'snapshots' field"
        else:
            print("No node reports found")
        
        print("Report structure verification passed!")
    else:
        print("Error: No report returned")

if __name__ == "__main__":
    asyncio.run(test_task_report())