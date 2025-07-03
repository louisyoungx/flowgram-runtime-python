"""
Test API functions with a complete workflow.
"""
import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional

from src.api.task_run_api import TaskRunAPI
from src.api.task_result_api import TaskResultAPI
from src.api.task_report_api import TaskReportAPI

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s:%(filename)s:%(lineno)d %(message)s')
logger = logging.getLogger(__name__)

# 工作流模式
WORKFLOW_SCHEMA = """{
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
}"""

# 工作流输入
WORKFLOW_INPUTS = {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
}

async def test_task_run_api():
    """测试 TaskRunAPI"""
    logger.info("测试 TaskRunAPI...")
    
    input_data = {
        "schema": WORKFLOW_SCHEMA,
        "inputs": WORKFLOW_INPUTS
    }
    
    result = await TaskRunAPI(input_data)
    task_id = result["taskID"]
    
    logger.info(f"TaskRunAPI 成功, taskID: {task_id}")
    return task_id

async def test_task_report_api(task_id: str):
    """测试 TaskReportAPI"""
    logger.info(f"测试 TaskReportAPI, taskID: {task_id}...")
    
    input_data = {
        "taskID": task_id
    }
    
    try:
        report = await TaskReportAPI(input_data)
        logger.info(f"TaskReportAPI 响应: {report}")
        
        # 检查报告是否包含必要的字段
        if not report:
            logger.error("TaskReportAPI 失败: 报告为空")
            return False
            
        if "id" not in report:
            logger.error("TaskReportAPI 失败: 报告缺少id字段")
            return False
            
        if "inputs" not in report:
            logger.error("TaskReportAPI 失败: 报告缺少inputs字段")
            return False
            
        if "workflowStatus" not in report:
            logger.error("TaskReportAPI 失败: 报告缺少workflowStatus字段")
            return False
            
        if "reports" not in report:
            logger.error("TaskReportAPI 失败: 报告缺少reports字段")
            return False
            
        # 检查报告中的输入是否与预期一致
        inputs = report.get("inputs", {})
        for key, value in WORKFLOW_INPUTS.items():
            if key not in inputs:
                logger.error(f"TaskReportAPI 失败: inputs中缺少{key}字段")
                return False
                
            if inputs[key] != value:
                logger.error(f"TaskReportAPI 失败: inputs中{key}字段的值不一致，预期{value}，实际{inputs[key]}")
                return False
        
        # 检查工作流状态
        workflow_status = report.get("workflowStatus", {})
        status = workflow_status.get("status")
        terminated = workflow_status.get("terminated")
        
        if status not in ["processing", "succeeded", "failed", "cancelled"]:
            logger.error(f"TaskReportAPI 失败: 工作流状态无效: {status}")
            return False
            
        return True
    except Exception as e:
        logger.error(f"TaskReportAPI 失败: {str(e)}")
        return False

async def test_task_result_api(task_id: str):
    """测试 TaskResultAPI"""
    logger.info(f"测试 TaskResultAPI, taskID: {task_id}...")
    
    input_data = {
        "taskID": task_id
    }
    
    try:
        result = await TaskResultAPI(input_data)
        logger.info(f"TaskResultAPI 响应: {result}")
        
        # 检查结果是否包含预期的输出
        if not result:
            logger.error("TaskResultAPI 失败: 结果为空")
            return False
            
        if "answer" not in result:
            logger.error("TaskResultAPI 失败: 结果缺少answer字段")
            return False
            
        if result["answer"] != "2":
            logger.error(f"TaskResultAPI 失败: answer字段的值不是2，实际是{result['answer']}")
            return False
            
        return True
    except Exception as e:
        logger.error(f"TaskResultAPI 失败: {str(e)}")
        return False

async def wait_for_workflow_completion(task_id: str, timeout: int = 30):
    """等待工作流执行完成"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        input_data = {"taskID": task_id}
        report = await TaskReportAPI(input_data)
        
        if not report:
            await asyncio.sleep(1)
            continue
            
        workflow_status = report.get("workflowStatus", {})
        status = workflow_status.get("status")
        terminated = workflow_status.get("terminated")
        
        if terminated:
            logger.info(f"工作流执行完成，状态: {status}")
            return True
            
        logger.info(f"工作流正在执行中，状态: {status}，继续等待...")
        await asyncio.sleep(1)
    
    logger.error(f"等待工作流执行超时，已等待{timeout}秒")
    return False

async def main():
    """主函数"""
    # 测试 TaskRunAPI
    task_id = await test_task_run_api()
    if not task_id:
        logger.error("测试失败: TaskRunAPI 未返回有效的任务ID")
        return
        
    # 等待工作流执行完成
    completed = await wait_for_workflow_completion(task_id)
    if not completed:
        logger.error("测试失败: 工作流执行未在规定时间内完成")
        return
        
    # 测试 TaskReportAPI
    report_success = await test_task_report_api(task_id)
    if not report_success:
        logger.error("测试失败: TaskReportAPI 测试未通过")
        return
        
    # 测试 TaskResultAPI
    result_success = await test_task_result_api(task_id)
    if not result_success:
        logger.error("测试失败: TaskResultAPI 测试未通过")
        return
        
    logger.info("所有测试通过!")

if __name__ == "__main__":
    asyncio.run(main())