from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# 基础工作流模型
class WorkflowIO(Dict[str, Any]):
    """工作流输入/输出，键值对字典"""
    pass

class WorkflowIOModel(BaseModel):
    """工作流输入/输出模型"""
    model_config = {"arbitrary_types_allowed": True}
    
    # 允许像字典一样使用
    def __getitem__(self, key):
        return self.model_dump().get(key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)


class WorkflowSnapshot(BaseModel):
    """工作流快照"""
    id: str
    nodeID: str
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    data: Dict[str, Any]
    branch: Optional[str] = None


class WorkflowStatus(BaseModel):
    """工作流状态"""
    status: str
    terminated: bool
    startTime: int
    endTime: Optional[int] = None
    timeCost: int


class NodeReport(BaseModel):
    """节点报告"""
    id: str
    status: str
    terminated: bool
    startTime: int
    endTime: Optional[int] = None
    timeCost: int
    snapshots: List[WorkflowSnapshot]


class Report(BaseModel):
    """工作流报告"""
    id: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    workflowStatus: WorkflowStatus
    reports: Dict[str, NodeReport]


# API 请求和响应模型
class TaskRunInput(BaseModel):
    """任务运行请求"""
    inputs: Dict[str, Any]
    schema: str


class TaskRunOutput(BaseModel):
    """任务运行响应"""
    taskID: str


class TaskResultInput(BaseModel):
    """任务结果请求"""
    taskID: str = Field(..., description="任务ID")


class TaskReportInput(BaseModel):
    """任务报告请求"""
    taskID: str = Field(..., description="任务ID")


class TaskCancelInput(BaseModel):
    """任务取消请求"""
    taskID: str


class TaskCancelOutput(BaseModel):
    """任务取消响应"""
    success: bool
