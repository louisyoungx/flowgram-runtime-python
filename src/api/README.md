# API 层实现

本目录包含工作流运行时系统的 API 层实现，提供了与工作流交互的接口。

## 概述

API 层是工作流运行时系统的外部接口，提供了以下功能：

1. **任务运行 API**：启动工作流任务
2. **任务结果 API**：获取工作流任务的结果
3. **任务报告 API**：获取工作流任务的报告
4. **任务取消 API**：取消正在运行的工作流任务

所有 API 函数都是异步的，接收特定的输入参数，并返回相应的输出。

## 实现细节

### 1. TaskRunAPI

`TaskRunAPI` 函数用于启动工作流任务，接收包含工作流模式和输入的参数，返回任务 ID。

```python
async def TaskRunAPI(input_data: TaskRunInput) -> TaskRunOutput:
    app = WorkflowApplication.instance()
    schema_str = input_data["schema"]
    inputs = input_data["inputs"]
    
    # Parse the schema string to a dictionary
    schema = json.loads(schema_str)
    
    # Run the workflow with the schema and inputs
    task_id = app.run({
        "schema": schema,
        "inputs": inputs,
    })
    
    # Create the output with the task ID
    output: TaskRunOutput = {
        "taskID": task_id,
    }
    
    return output
```

### 2. TaskResultAPI

`TaskResultAPI` 函数用于获取工作流任务的结果，接收任务 ID，返回工作流输出。

```python
async def TaskResultAPI(input_data: TaskResultInput) -> WorkflowOutputs:
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Get the result of the task
    output = app.result(task_id)
    
    return output
```

### 3. TaskReportAPI

`TaskReportAPI` 函数用于获取工作流任务的报告，接收任务 ID，返回任务报告。

```python
async def TaskReportAPI(input_data: TaskReportInput) -> Optional[IReport]:
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Get the report of the task
    output = app.report(task_id)
    
    return output
```

### 4. TaskCancelAPI

`TaskCancelAPI` 函数用于取消正在运行的工作流任务，接收任务 ID，返回取消是否成功。

```python
async def TaskCancelAPI(input_data: TaskCancelInput) -> Dict[str, bool]:
    app = WorkflowApplication.instance()
    task_id = input_data["taskID"]
    
    # Cancel the task
    success = app.cancel(task_id)
    
    # Create the output with the success flag
    output = {
        "success": success
    }
    
    return output
```

### 5. WorkflowRuntimeAPIs

`WorkflowRuntimeAPIs` 是一个字典，将 API 名称映射到 API 函数，便于根据名称调用相应的 API 函数。

```python
WorkflowRuntimeAPIs: Dict[FlowGramAPIName, Callable[[Any], Any]] = {
    FlowGramAPIName.TaskRun: TaskRunAPI,
    FlowGramAPIName.TaskReport: TaskReportAPI,
    FlowGramAPIName.TaskResult: TaskResultAPI,
    FlowGramAPIName.TaskCancel: TaskCancelAPI,
    FlowGramAPIName.ServerInfo: lambda _: None,  # TODO
    FlowGramAPIName.Validation: lambda _: None,  # TODO
}
```

## 使用示例

以下是使用 API 函数的示例：

```python
import json
import asyncio
from runtime_py_core.src.api import TaskRunAPI, TaskResultAPI, TaskReportAPI, TaskCancelAPI
from runtime_py_core.src.interface.schema import TaskRunInput, TaskResultInput, TaskReportInput, TaskCancelInput

# 创建工作流模式
schema = {
    "nodes": [
        {
            "id": "node1",
            "type": "start",
            "data": {},
            "ports": {
                "output": [
                    {
                        "id": "port1",
                        "type": "output",
                        "nodeId": "node1",
                        "key": "output"
                    }
                ]
            }
        }
    ],
    "edges": []
}

# 运行工作流任务
async def run_workflow():
    input_data: TaskRunInput = {
        "schema": json.dumps(schema),
        "inputs": {"key": "value"}
    }
    result = await TaskRunAPI(input_data)
    task_id = result["taskID"]
    
    # 获取任务结果
    result_input: TaskResultInput = {
        "taskID": task_id
    }
    result = await TaskResultAPI(result_input)
    
    # 获取任务报告
    report_input: TaskReportInput = {
        "taskID": task_id
    }
    report = await TaskReportAPI(report_input)
    
    # 取消任务
    cancel_input: TaskCancelInput = {
        "taskID": task_id
    }
    cancel_result = await TaskCancelAPI(cancel_input)
    
    return result, report, cancel_result

# 运行示例
asyncio.run(run_workflow())
```

## 翻译过程中的关键点

在将 JavaScript 代码翻译为 Python 代码的过程中，有以下几个关键点需要注意：

1. **异步函数**：JavaScript 使用 `async/await` 关键字，Python 也使用 `async/await` 关键字，但语法略有不同。

2. **参数解构**：JavaScript 中的参数解构（如 `const { taskID } = input`）在 Python 中使用字典访问（如 `task_id = input_data["taskID"]`）。

3. **JSON 解析**：JavaScript 中的 `JSON.parse` 在 Python 中使用 `json.loads`。

4. **错误处理**：JavaScript 中的 `try/catch` 在 Python 中使用 `try/except`。

5. **日志记录**：JavaScript 中的 `console.log` 在 Python 中使用 `logging.info` 或 `logging.debug`。

6. **命名约定**：JavaScript 使用驼峰命名法（如 `taskID`），而 Python 使用下划线命名法（如 `task_id`）。但为了与接口定义保持一致，我们在 API 层中保留了驼峰命名法。

7. **单例模式**：JavaScript 中使用静态 getter 属性 `instance` 实现单例模式，Python 中使用类方法 `instance()` 实现单例模式。

8. **类型注解**：JavaScript 使用 TypeScript 的类型注解，Python 使用 `typing` 模块的类型注解。

## 测试

API 层的测试文件位于 `__tests__` 目录下，使用 Python 的 `unittest` 模块和 `unittest.mock` 模块进行测试。测试覆盖了所有四个 API 函数，验证了它们的行为是否符合预期。