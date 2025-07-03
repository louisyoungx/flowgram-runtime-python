# 节点执行器实现

本目录包含了工作流运行时的节点执行器实现。节点执行器负责执行工作流中的各种类型的节点，包括开始节点、结束节点、LLM节点、条件节点和循环节点。

## 节点执行器类型

以下是实现的节点执行器类型：

1. **StartExecutor**：执行开始节点，返回IO中心的输入作为输出。
2. **EndExecutor**：执行结束节点，将输入设置为IO中心的输出，并返回相同的输入作为输出。
3. **LLMExecutor**：执行LLM节点，使用LangChain的ChatOpenAI模型来执行LLM调用，并返回结果。
4. **ConditionExecutor**：执行条件节点，评估条件并确定要遵循的分支。
5. **LoopExecutor**：执行循环节点，为循环数组中的每个项目执行子节点。

## 代码结构

每个节点执行器都实现了`INodeExecutor`接口，提供了以下功能：

- `type`属性：返回节点执行器可以处理的节点类型。
- `execute`方法：执行节点并返回结果。

此外，条件节点执行器还包含了条件处理的相关组件：

- `type.py`：定义了条件类型和操作。
- `rules.py`：定义了不同类型变量的条件操作规则。
- `handlers/`：包含了不同类型变量的条件处理器实现。

## 使用示例

以下是使用节点执行器的示例：

```python
# 创建节点执行器
start_executor = StartExecutor()
end_executor = EndExecutor()
llm_executor = LLMExecutor()
condition_executor = ConditionExecutor()
loop_executor = LoopExecutor()

# 创建执行上下文
context = ExecutionContext(
    node=node,
    inputs=inputs,
    runtime=runtime,
    container=container
)

# 执行节点
result = await executor.execute(context)

# 处理结果
outputs = result.outputs
branch = result.branch  # 仅对条件节点有效
```

## 测试

节点执行器的测试位于`__tests__/test_node_executors.py`文件中，包含了对每个节点执行器类型和执行功能的测试。

## 实现细节

1. **异步执行**：所有节点执行器的`execute`方法都是异步的，使用`async/await`语法。
2. **类型安全**：使用Python的类型注解确保类型安全。
3. **错误处理**：使用适当的异常处理确保代码的健壮性。
4. **代码风格**：遵循Python的PEP 8编码规范和最佳实践。
5. **文档**：为所有类和方法添加了详细的文档字符串。

## 与原始JavaScript代码的区别

本实现与原始JavaScript代码保持了一致的功能和逻辑，但有以下几点区别：

1. **命名约定**：使用Python的下划线命名法（如`variable_store`而不是`variableStore`）。
2. **属性访问**：使用属性装饰器（`@property`）实现属性访问。
3. **异步处理**：JavaScript中使用Promise，而在Python中使用`async/await`。
4. **接口实现**：Python中使用抽象基类（ABC）实现接口，而JavaScript中使用`implements`关键字。