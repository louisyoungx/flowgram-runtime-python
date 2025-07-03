# TaskReport API 永远返回 processing 状态问题修复方案

## 问题描述

用户反馈在使用以下 curl 命令测试 TaskReport API 时，该 API 永远返回 "processing" 状态，即使工作流已经执行完成：

```bash
curl --location 'http://localhost:4000/api/task/run' \
--header 'Content-Type: application/json' \
--data '{
  "inputs": {
      "model_name": "ep-20250206192339-nnr9m",
      "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
      "api_host": "https://ark.cn-beijing.volces.com/api/v3",
      "prompt": "Just give me the answer of '\''1+1=?'\'', just one number, no other words"
  },
  "schema": "{\"nodes\":[{\"id\":\"start_0\",\"type\":\"start\",\"meta\":{\"position\":{\"x\":0,\"y\":0}},\"data\":{\"title\":\"Start\",\"outputs\":{\"type\":\"object\",\"properties\":{\"model_name\":{\"key\":14,\"name\":\"model_name\",\"type\":\"string\",\"extra\":{\"index\":1},\"isPropertyRequired\":true},\"prompt\":{\"key\":5,\"name\":\"prompt\",\"type\":\"string\",\"extra\":{\"index\":3},\"isPropertyRequired\":true},\"api_key\":{\"key\":19,\"name\":\"api_key\",\"type\":\"string\",\"extra\":{\"index\":4},\"isPropertyRequired\":true},\"api_host\":{\"key\":20,\"name\":\"api_host\",\"type\":\"string\",\"extra\":{\"index\":5},\"isPropertyRequired\":true}},\"required\":[\"model_name\",\"prompt\",\"api_key\",\"api_host\"]}}},{\"id\":\"end_0\",\"type\":\"end\",\"meta\":{\"position\":{\"x\":1000,\"y\":0}},\"data\":{\"title\":\"End\",\"inputsValues\":{\"answer\":{\"type\":\"ref\",\"content\":[\"llm_0\",\"result\"]}},\"inputs\":{\"type\":\"object\",\"properties\":{\"answer\":{\"type\":\"string\"}}}}},{\"id\":\"llm_0\",\"type\":\"llm\",\"meta\":{\"position\":{\"x\":500,\"y\":0}},\"data\":{\"title\":\"LLM_0\",\"inputsValues\":{\"modelName\":{\"type\":\"ref\",\"content\":[\"start_0\",\"model_name\"]},\"apiKey\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_key\"]},\"apiHost\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_host\"]},\"temperature\":{\"type\":\"constant\",\"content\":0},\"prompt\":{\"type\":\"ref\",\"content\":[\"start_0\",\"prompt\"]},\"systemPrompt\":{\"type\":\"constant\",\"content\":\"You are a helpful AI assistant.\"}},\"inputs\":{\"type\":\"object\",\"required\":[\"modelName\",\"temperature\",\"prompt\"],\"properties\":{\"modelName\":{\"type\":\"string\"},\"apiKey\":{\"type\":\"string\"},\"apiHost\":{\"type\":\"string\"},\"temperature\":{\"type\":\"number\"},\"systemPrompt\":{\"type\":\"string\"},\"prompt\":{\"type\":\"string\"}}},\"outputs\":{\"type\":\"object\",\"properties\":{\"result\":{\"type\":\"string\"}}}}}],\"edges\":[{\"sourceNodeID\":\"start_0\",\"targetNodeID\":\"llm_0\"},{\"sourceNodeID\":\"llm_0\",\"targetNodeID\":\"end_0\"}]}"
}'

curl --location 'http://localhost:4000/api/task/report?taskID=xxxxxx'
```

预期行为是 TaskReport API 应该返回工作流的实际状态，包括 "succeeded"、"failed" 或 "cancelled"，而不是永远返回 "processing"。

## 问题根源分析

通过详细分析代码，我们发现了以下几个关键问题：

### 1. 状态枚举值不一致

在代码中存在两种不同的 `WorkflowStatus` 枚举定义：
- 在 `interface/node.py` 中使用 `Succeeded`
- 在 `interface/schema.py` 中使用 `Success`

这种不一致导致了状态比较和转换时的混乱。

### 2. 异步任务状态更新问题

在 `workflow_runtime_task.py` 中，异步任务的处理逻辑存在缺陷：

```python
def handle_complete(self, result: Any) -> None:
    """Handle the completion of the task."""
    # 检查工作流状态，但没有正确更新任务状态
    if self._context.status_center.workflow.status == WorkflowStatus.Success:
        self._status = "completed"  # 使用字符串而非枚举
    # ...其他代码...
```

这段代码有两个问题：
- 使用字符串 "completed" 而非枚举值 `WorkflowStatus.Succeeded`
- 工作流状态检查使用 `WorkflowStatus.Success` 而非 `WorkflowStatus.Succeeded`

### 3. 工作流引擎状态设置问题

在 `workflow_runtime_engine.py` 中，工作流状态设置方式不正确：

```python
# 直接设置状态属性，而不是调用方法
context.status_center.workflow.status = WorkflowStatus.Success
```

但 `workflow_runtime_status_center.py` 中的 `WorkflowRuntimeWorkflowStatus` 类并没有为 `status` 属性提供 setter 方法，导致无法直接设置状态。

### 4. 状态导出格式问题

在 `workflow_runtime_status_center.py` 中，`export` 方法直接返回了枚举对象，而不是字符串值：

```python
return {
    "status": self._status,  # 返回枚举对象而非字符串
    # ...其他字段...
}
```

这导致在序列化为 JSON 时返回了完整的枚举类名（如 "WorkflowStatus.Succeeded"）。

### 5. 状态转换逻辑问题

在 `task_report_api.py` 中，状态转换逻辑只处理了 "success" 字符串：

```python
# 只处理 "success" 字符串，没有处理枚举值
if status_dict.get("status") == "success":
    status_dict["status"] = "succeeded"
```

## 修复方案

我们实施了以下修复措施：

### 1. 统一使用 WorkflowStatus 枚举

修改所有代码，确保一致地使用 `WorkflowStatus` 枚举：

```python
# 在 workflow_runtime_task.py 中
from ..interface.schema import WorkflowStatus

def handle_complete(self, result: Any) -> None:
    if self._context.status_center.workflow.status == WorkflowStatus.Success:
        self._status = WorkflowStatus.Success
    # ...
```

### 2. 修复异步任务状态更新

在 `workflow_runtime_task.py` 中，确保正确处理异步协程：

```python
@property
def processing(self) -> Any:
    """Get the processing promise."""
    if asyncio.iscoroutine(self._processing):
        # 创建一个任务来运行协程
        task = asyncio.create_task(self._processing)
        # 添加完成回调
        task.add_done_callback(
            lambda t: self.handle_complete(t.result()) if not t.exception() else self.handle_error(t.exception())
        )
        return task
    return self._processing
```

### 3. 修复工作流引擎状态设置

在 `workflow_runtime_engine.py` 中，使用方法调用而不是直接设置属性：

```python
# 修改前
context.status_center.workflow.status = WorkflowStatus.Success

# 修改后
context.status_center.workflow.success()
```

### 4. 修复状态导出格式

在 `workflow_runtime_status_center.py` 中，修改 `export` 方法以返回枚举值的名称：

```python
def export(self) -> Dict[str, Any]:
    # 提取枚举值的名称
    status_str = self._status
    if hasattr(self._status, 'name'):
        status_str = self._status.name
    elif self._status and isinstance(self._status, str) and '.' in self._status:
        status_str = self._status.split('.')[-1]
        
    return {
        "status": status_str if self._status else "unknown",
        # ...其他字段...
    }
```

### 5. 增强状态转换逻辑

在 `task_report_api.py` 中，增强状态转换逻辑：

```python
# 处理各种形式的 "success" 状态
status = status_dict.get("status", "")
if status == "success" or "Success" in status:
    status_dict["status"] = "succeeded"
```

## 验证结果

我们创建了一个测试脚本 `test_task_report_fix.py` 来验证修复效果。测试结果表明，TaskReport API 现在能够正确地返回工作流的最终状态（如 "Succeeded"），而不是一直返回 "processing"。

测试输出片段：
```
检查 #9: 状态 = Succeeded
工作流已完成，最终状态: Succeeded
✅ 测试通过: 状态已从 'processing' 更新为终止状态
```

## 修复的文件列表

以下是我们修改的文件列表：

1. `runtime-py-core/src/domain/task/workflow_runtime_task.py`
2. `runtime-py-core/src/domain/engine/workflow_runtime_engine.py`
3. `runtime-py-core/src/domain/status/workflow_runtime_status_center.py`
4. `runtime-py-core/src/api/task_report_api.py`
5. `runtime-py-core/src/interface/node.py`

## 结论

通过这次修复，我们解决了 TaskReport API 永远返回 "processing" 状态的问题。修复方案涉及多个模块的协同工作，包括状态管理、任务执行和 API 响应处理。这些修复确保了 TaskReport API 能够准确反映工作流的实际状态，提高了系统的可靠性和用户体验。

现在，用户可以使用提供的 curl 命令测试 TaskReport API，并且将看到工作流的实际状态，而不是永远的 "processing" 状态。