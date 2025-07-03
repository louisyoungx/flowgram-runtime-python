"""
Test API functions with curl-like requests.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional

from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI
from src.api.task_cancel_api import TaskCancelAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test data
TEST_INPUTS = {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
}

TEST_SCHEMA = """{"nodes":[{"id":"start_0","type":"start","meta":{"position":{"x":0,"y":0}},"data":{"title":"Start","outputs":{"type":"object","properties":{"model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},"prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},"api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},"api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}},"required":["model_name","prompt","api_key","api_host"]}}},{"id":"end_0","type":"end","meta":{"position":{"x":1000,"y":0}},"data":{"title":"End","inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},"inputs":{"type":"object","properties":{"answer":{"type":"string"}}}}},{"id":"llm_0","type":"llm","meta":{"position":{"x":500,"y":0}},"data":{"title":"LLM_0","inputsValues":{"modelName":{"type":"ref","content":["start_0","model_name"]},"apiKey":{"type":"ref","content":["start_0","api_key"]},"apiHost":{"type":"ref","content":["start_0","api_host"]},"temperature":{"type":"constant","content":0},"prompt":{"type":"ref","content":["start_0","prompt"]},"systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}},"inputs":{"type":"object","required":["modelName","temperature","prompt"],"properties":{"modelName":{"type":"string"},"apiKey":{"type":"string"},"apiHost":{"type":"string"},"temperature":{"type":"number"},"systemPrompt":{"type":"string"},"prompt":{"type":"string"}}},"outputs":{"type":"object","properties":{"result":{"type":"string"}}}}}],"edges":[{"sourceNodeID":"start_0","targetNodeID":"llm_0"},{"sourceNodeID":"llm_0","targetNodeID":"end_0"}]}"""

async def test_task_run_api():
    """Test TaskRunAPI."""
    logger.info("测试 TaskRunAPI...")
    input_data = {
        "inputs": TEST_INPUTS,
        "schema": TEST_SCHEMA
    }
    
    try:
        result = await TaskRunAPI(input_data)
        task_id = result["taskID"]
        logger.info(f"TaskRunAPI 成功, taskID: {task_id}")
        return task_id
    except Exception as e:
        logger.error(f"TaskRunAPI 失败: {str(e)}")
        return None

async def test_task_report_api(task_id: str):
    """Test TaskReportAPI."""
    logger.info(f"测试 TaskReportAPI, taskID: {task_id}...")
    input_data = {
        "taskID": task_id
    }
    
    try:
        # Wait for the task to complete
        await asyncio.sleep(5)
        
        result = await TaskReportAPI(input_data)
        logger.info(f"TaskReportAPI 响应: {json.dumps(result, indent=2)}")
        
        # Verify the response structure
        assert "id" in result, "响应中缺少id字段"
        assert "inputs" in result, "响应中缺少inputs字段"
        assert "outputs" in result, "响应中缺少outputs字段"
        assert "workflowStatus" in result, "响应中缺少workflowStatus字段"
        assert "reports" in result, "响应中缺少reports字段"
        
        # Verify inputs
        assert "model_name" in result["inputs"], "inputs中缺少model_name字段"
        assert "api_key" in result["inputs"], "inputs中缺少api_key字段"
        assert "api_host" in result["inputs"], "inputs中缺少api_host字段"
        assert "prompt" in result["inputs"], "inputs中缺少prompt字段"
        
        # Verify workflowStatus
        assert "status" in result["workflowStatus"], "workflowStatus中缺少status字段"
        assert result["workflowStatus"]["status"] in ["processing", "succeeded", "failed", "cancelled"], f"workflowStatus.status字段值不正确: {result['workflowStatus']['status']}"
        
        # Verify reports
        assert "start_0" in result["reports"], "reports中缺少start_0节点"
        assert "llm_0" in result["reports"], "reports中缺少llm_0节点"
        assert "end_0" in result["reports"], "reports中缺少end_0节点"
        
        # Verify node reports
        for node_id in ["start_0", "llm_0", "end_0"]:
            node_report = result["reports"][node_id]
            assert "status" in node_report, f"{node_id}节点报告中缺少status字段"
            assert "snapshots" in node_report, f"{node_id}节点报告中缺少snapshots字段"
            assert len(node_report["snapshots"]) > 0, f"{node_id}节点报告中snapshots为空"
        
        logger.info("TaskReportAPI 验证通过")
        return result
    except Exception as e:
        logger.error(f"TaskReportAPI 失败: {str(e)}")
        return None

async def test_task_result_api(task_id: str):
    """Test TaskResultAPI."""
    logger.info(f"测试 TaskResultAPI, taskID: {task_id}...")
    input_data = {
        "taskID": task_id
    }
    
    try:
        result = await TaskResultAPI(input_data)
        logger.info(f"TaskResultAPI 响应: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        logger.error(f"TaskResultAPI 失败: {str(e)}")
        return None

async def test_task_cancel_api(task_id: str):
    """Test TaskCancelAPI."""
    logger.info(f"测试 TaskCancelAPI, taskID: {task_id}...")
    input_data = {
        "taskID": task_id
    }
    
    try:
        result = await TaskCancelAPI(input_data)
        logger.info(f"TaskCancelAPI 响应: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        logger.error(f"TaskCancelAPI 失败: {str(e)}")
        return None

async def main():
    """Main function."""
    # Test TaskRunAPI
    task_id = await test_task_run_api()
    if not task_id:
        logger.error("TaskRunAPI 测试失败，无法继续测试")
        return
    
    # Test TaskReportAPI
    report = await test_task_report_api(task_id)
    if not report:
        logger.error("TaskReportAPI 测试失败，无法继续测试")
    
    # Test TaskResultAPI
    result = await test_task_result_api(task_id)
    if not result:
        logger.error("TaskResultAPI 测试失败，无法继续测试")
    
    # Test TaskCancelAPI (optional)
    # await test_task_cancel_api(task_id)

if __name__ == "__main__":
    asyncio.run(main())