from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, Dict, Any, List

from .models import (
    TaskRunInput, TaskRunOutput,
    TaskResultInput, TaskReportInput,
    TaskCancelInput, TaskCancelOutput,
    WorkflowIO, Report
)

# 导入 runtime-py-core 库
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.api import TaskRunAPI, TaskResultAPI, TaskReportAPI, TaskCancelAPI

# 创建路由器
router = APIRouter(prefix="/api", tags=["task"])


@router.post("/task/run", response_model=TaskRunOutput)
async def run_task(input_data: TaskRunInput):
    """
    运行工作流任务
    
    接收工作流模式和输入，启动任务执行，返回任务ID
    """
    try:
        result = await TaskRunAPI(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务运行失败: {str(e)}")


@router.get("/task/result", response_model=Optional[Dict[str, Any]])
async def get_task_result(taskID: str = Query(..., description="任务ID")):
    """
    获取任务结果
    
    根据任务ID获取工作流执行的结果
    """
    try:
        result = await TaskResultAPI({"taskID": taskID})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务结果失败: {str(e)}")


@router.get("/task/report", response_model=Report)
async def get_task_report(taskID: str = Query(..., description="任务ID")):
    """
    获取任务报告
    
    根据任务ID获取工作流执行的详细报告
    """
    try:
        # TaskReportAPI 现在总是返回一个字典，不再返回 None
        report = await TaskReportAPI({"taskID": taskID})
        
        # 直接返回报告字典，它已经符合 Report 模型的结构
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务报告失败: {str(e)}")


@router.put("/task/cancel", response_model=TaskCancelOutput)
async def cancel_task(input_data: TaskCancelInput):
    """
    取消任务
    
    根据任务ID取消正在运行的工作流任务
    """
    try:
        result = await TaskCancelAPI(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消任务失败: {str(e)}")
