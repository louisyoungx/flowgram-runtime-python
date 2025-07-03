# 工作流运行时任务模块

本模块包含工作流运行时任务的实现，主要是 `WorkflowRuntimeTask` 类，它实现了 `ITask` 接口。

## 实现概述

`WorkflowRuntimeTask` 类表示一个工作流任务，包含以下功能：

1. **任务创建和初始化**：通过构造函数和静态 `create` 方法创建任务实例。
2. **任务执行**：通过 `run` 方法执行任务，返回任务处理的结果。
3. **任务取消**：通过 `cancel` 方法取消任务，停止工作流执行。
4. **任务状态管理**：通过 `status` 属性获取任务状态，包括 "processing"、"completed"、"failed" 和 "cancelled"。
5. **完成和错误回调**：通过 `on_complete` 和 `on_error` 方法注册回调函数，在任务完成或出错时调用。

## 与原始 JavaScript 代码的区别

本实现与原始 JavaScript 代码保持了一致的功能和逻辑，但有以下几点区别：

1. **命名约定**：使用 Python 的下划线命名法（如 `status_center` 而不是 `statusCenter`）。
2. **属性访问**：使用属性装饰器（`@property`）实现属性访问，而不是直接访问实例变量。
3. **异步处理**：JavaScript 中使用 Promise，而在 Python 中使用类似 Promise 的对象或异步函数。
4. **接口实现**：Python 中使用抽象基类（ABC）实现接口，而 JavaScript 中使用 `implements` 关键字。

## 使用示例

```python
from runtime_py_core.interface.task import TaskParams
from runtime_py_core.domain.task import WorkflowRuntimeTask

# 创建任务参数
params = TaskParams(
    context=context,  # IContext 实例
    processing=lambda: {"result": "success"}  # 处理函数
)

# 创建任务
task = WorkflowRuntimeTask.create(params)

# 获取任务 ID 和状态
task_id = task.id
status = task.status

# 执行任务
result = task.run()

# 注册完成回调
task.on_complete(lambda result: print(f"Task completed with result: {result}"))

# 注册错误回调
task.on_error(lambda error: print(f"Task failed with error: {error}"))

# 取消任务
task.cancel()
```

## 测试

本模块包含两个测试文件：

1. `test_task.py`：测试基本功能，包括任务创建、执行、取消和回调。
2. `test_task_async.py`：测试异步操作，包括异步处理和异步错误处理。

运行测试：

```bash
python -m unittest src/domain/__tests__/test_task.py
python -m unittest src/domain/__tests__/test_task_async.py
```

## 注意事项

1. **异步操作**：在 Python 中，异步操作通常使用 `asyncio` 模块和 `async`/`await` 语法。本实现中使用了类似 Promise 的对象来模拟 JavaScript 中的异步操作，但在实际使用中，可能需要根据具体环境进行调整。

2. **回调处理**：在 JavaScript 中，Promise 的 `then` 和 `catch` 方法用于处理异步操作的结果和错误。在 Python 中，我们使用回调函数来实现类似的功能。

3. **状态管理**：任务状态包括 "processing"、"completed"、"failed" 和 "cancelled"，与原始 JavaScript 代码保持一致。

4. **资源释放**：在任务完成或取消后，应该释放相关资源，特别是上下文对象中的资源。