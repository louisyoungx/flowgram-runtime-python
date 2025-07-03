"""
Test API functions with the fixed TaskReport API.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional

from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI

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

async def test_api_functions():
    """Test API functions."""
    # Test TaskRunAPI
    logger.info("测试 TaskRunAPI...")
    task_run_input = {
        "inputs": TEST_INPUTS,
        "schema": TEST_SCHEMA
    }
    
    try:
        task_run_output = await TaskRunAPI(task_run_input)
        task_id = task_run_output["taskID"]
        logger.info(f"TaskRunAPI 成功, taskID: {task_id}")
        
        # Wait for the workflow to complete
        logger.info("等待工作流执行完成...")
        await asyncio.sleep(5)
        
        # Test TaskReportAPI
        logger.info(f"测试 TaskReportAPI, taskID: {task_id}...")
        task_report_input = {"taskID": task_id}
        report = await TaskReportAPI(task_report_input)
        
        if report:
            logger.info(f"TaskReportAPI 响应: {json.dumps(report, indent=2)}")
            
            # Verify report structure
            assert "id" in report, "报告中缺少id字段"
            assert "inputs" in report, "报告中缺少inputs字段"
            assert "outputs" in report, "报告中缺少outputs字段"
            assert "workflowStatus" in report, "报告中缺少workflowStatus字段"
            assert "reports" in report, "报告中缺少reports字段"
            
            # Verify inputs
            assert "model_name" in report["inputs"], "inputs中缺少model_name字段"
            assert "api_key" in report["inputs"], "inputs中缺少api_key字段"
            assert "api_host" in report["inputs"], "inputs中缺少api_host字段"
            assert "prompt" in report["inputs"], "inputs中缺少prompt字段"
            
            # Verify workflowStatus
            assert "status" in report["workflowStatus"], "workflowStatus中缺少status字段"
            assert "terminated" in report["workflowStatus"], "workflowStatus中缺少terminated字段"
            assert "startTime" in report["workflowStatus"], "workflowStatus中缺少startTime字段"
            
            # Verify reports
            assert "start_0" in report["reports"], "reports中缺少start_0节点"
            assert "llm_0" in report["reports"], "reports中缺少llm_0节点"
            assert "end_0" in report["reports"], "reports中缺少end_0节点"
            
            logger.info("TaskReportAPI 验证成功!")
        else:
            logger.error("TaskReportAPI 失败: 返回空报告")
            
        # Test TaskResultAPI
        logger.info(f"测试 TaskResultAPI, taskID: {task_id}...")
        task_result_input = {"taskID": task_id}
        result = await TaskResultAPI(task_result_input)
        
        if result:
            logger.info(f"TaskResultAPI 响应: {result}")
            assert "answer" in result, "结果中缺少answer字段"
            logger.info("TaskResultAPI 验证成功!")
        else:
            logger.error("TaskResultAPI 失败: 返回空结果")
            
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_api_functions())