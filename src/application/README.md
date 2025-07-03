# 工作流应用层

这个目录包含工作流应用层的实现，主要是`WorkflowApplication`类。

## 工作流应用类 (WorkflowApplication)

`WorkflowApplication`类是工作流运行时的主要入口点，它提供了运行工作流、取消任务、获取报告和结果等功能。

### 主要功能

1. **运行工作流**：通过`run`方法运行工作流，返回任务ID。
2. **取消任务**：通过`cancel`方法取消正在运行的任务。
3. **获取报告**：通过`report`方法获取任务的报告。
4. **获取结果**：通过`result`方法获取任务的结果。

### 单例模式

`WorkflowApplication`类实现了单例模式，通过`instance`类方法获取单例实例。

### 使用示例

```python
from runtime_py_core.application import WorkflowApplication

# 获取工作流应用实例
app = WorkflowApplication.instance()

# 运行工作流
params = {
    "workflow": {...},  # 工作流定义
    "inputs": {...}     # 工作流输入
}
task_id = app.run(params)

# 获取结果
result = app.result(task_id)

# 获取报告
report = app.report(task_id)

# 取消任务
app.cancel(task_id)
```

## 翻译过程中的关键点

1. **命名约定**：JavaScript使用驼峰命名法，而Python使用下划线命名法。在翻译过程中，我保持了类名的驼峰命名法，但将方法和属性名转换为下划线命名法。

2. **单例模式**：JavaScript中使用静态getter属性实现单例模式，而在Python中，我使用了类方法来实现类似的功能。

3. **异步处理**：JavaScript中使用Promise处理异步操作，而在Python中，我使用了回调函数来处理任务完成后的操作。

4. **日志记录**：JavaScript中使用`console.log`记录日志，而在Python中，我使用了`logging`模块记录日志。

5. **数据结构**：JavaScript中使用`Map`存储任务，而在Python中，我使用了字典来存储任务。