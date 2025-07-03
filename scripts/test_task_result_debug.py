"""
Debug the TaskResultAPI issue.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional

from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI
from src.api.task_result_api import TaskResultAPI
from src.application.workflow_application import WorkflowApplication
from src.interface.engine import IEngine
from src.domain.container import WorkflowRuntimeContainer

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

async def test_task_result_debug():
    """Debug the TaskResultAPI issue."""
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
        
        # Get the task directly from WorkflowApplication
        app = WorkflowApplication.instance()
        task = app.tasks.get(task_id)
        
        if task:
            # Wait for the workflow to complete
            logger.info("等待工作流执行完成...")
            start_time = time.time()
            timeout = 10  # 10 seconds timeout
            
            while not task.context.status_center.workflow.terminated and time.time() - start_time < timeout:
                await asyncio.sleep(0.1)
            
            # Check if workflow is terminated
            if task.context.status_center.workflow.terminated:
                logger.info(f"工作流已终止，状态: {task.context.status_center.workflow.status}")
                
                # Check IO center outputs directly
                io_outputs = task.context.io_center.outputs
                logger.info(f"IO center outputs (直接访问): {io_outputs}")
                
                # Check IO center _outputs directly
                if hasattr(task.context.io_center, "_outputs"):
                    logger.info(f"IO center _outputs (直接访问): {task.context.io_center._outputs}")
                
                # Check end node snapshots
                snapshots = task.context.snapshot_center.export_all()
                end_snapshots = [s for s in snapshots if s.get("nodeID") == "end_0"]
                if end_snapshots:
                    logger.info(f"End node snapshot: {end_snapshots[0]}")
                    if "outputs" in end_snapshots[0]:
                        logger.info(f"End node outputs: {end_snapshots[0]['outputs']}")
                
                # Test TaskResultAPI
                logger.info(f"测试 TaskResultAPI, taskID: {task_id}...")
                task_result_input = {"taskID": task_id}
                result = await TaskResultAPI(task_result_input)
                
                logger.info(f"TaskResultAPI 响应: {result}")
                
                # Check app.result directly
                direct_result = app.result(task_id)
                logger.info(f"Direct app.result: {direct_result}")
                
                # Try to manually set outputs and test again
                logger.info("尝试手动设置outputs并再次测试...")
                if end_snapshots and "outputs" in end_snapshots[0]:
                    task.context.io_center.set_outputs(end_snapshots[0]["outputs"])
                    logger.info(f"手动设置后的IO center outputs: {task.context.io_center.outputs}")
                    
                    # Test TaskResultAPI again
                    result = await TaskResultAPI(task_result_input)
                    logger.info(f"手动设置后的TaskResultAPI响应: {result}")
            else:
                logger.error(f"工作流未在超时时间内终止")
        else:
            logger.error(f"找不到任务: {task_id}")
            
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_task_result_debug())