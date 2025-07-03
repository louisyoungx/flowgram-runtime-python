# 工作流运行时上下文 (WorkflowRuntimeContext)

## 概述

工作流运行时上下文是工作流运行时的核心组件，它提供了工作流执行过程中所需的各种组件，包括：

- **文档 (Document)**：存储工作流定义（节点和边）
- **变量存储 (Variable Store)**：管理工作流中使用的变量
- **状态 (State)**：管理工作流的执行状态
- **IO 中心 (IO Center)**：管理工作流的输入和输出
- **快照中心 (Snapshot Center)**：创建和管理工作流执行的快照
- **状态中心 (Status Center)**：管理工作流和节点的状态
- **报告器 (Reporter)**：生成工作流执行的报告

上下文还可以创建子上下文，子上下文从父上下文继承某些组件（如文档和 IO 中心），同时拥有自己的变量存储和状态。

## 实现细节

### WorkflowRuntimeContext 类

`WorkflowRuntimeContext` 类实现了 `IContext` 接口，提供了以下功能：

1. **初始化**：通过 `init` 方法初始化上下文，包括初始化文档、变量存储、状态等组件。
2. **资源释放**：通过 `dispose` 方法释放上下文的资源，包括释放子上下文的资源。
3. **子上下文创建**：通过 `sub` 方法创建子上下文，子上下文继承父上下文的某些组件。
4. **静态创建方法**：通过 `create` 静态方法创建一个新的上下文，包括创建所有必要的组件。

### 组件

上下文包含以下组件：

1. **文档 (Document)**：由 `WorkflowRuntimeDocument` 类实现，负责解析工作流模式并提供对节点和边的访问。
2. **变量存储 (Variable Store)**：由 `WorkflowRuntimeVariableStore` 类实现，负责存储和访问工作流中的变量。
3. **状态 (State)**：由 `WorkflowRuntimeState` 类实现，负责管理工作流的执行状态，包括跟踪已执行的节点和节点的输出。
4. **IO 中心 (IO Center)**：由 `WorkflowRuntimeIOCenter` 类实现，负责管理工作流的输入和输出。
5. **快照中心 (Snapshot Center)**：由 `WorkflowRuntimeSnapshotCenter` 类实现，负责创建和管理工作流执行的快照。
6. **状态中心 (Status Center)**：由 `WorkflowRuntimeStatusCenter` 类实现，负责管理工作流和节点的状态。
7. **报告器 (Reporter)**：由 `WorkflowRuntimeReporter` 类实现，负责生成工作流执行的报告。

### 子上下文

子上下文是通过 `sub` 方法创建的，它继承父上下文的以下组件：

- 文档 (Document)
- IO 中心 (IO Center)
- 快照中心 (Snapshot Center)
- 状态中心 (Status Center)
- 报告器 (Reporter)

同时，子上下文拥有自己的变量存储和状态。子上下文的变量存储设置父上下文的变量存储为父级，这样子上下文可以访问父上下文的变量，但父上下文无法访问子上下文的变量。

## 使用示例

```python
# 创建上下文
context = WorkflowRuntimeContext.create()

# 初始化上下文
params = {
    "schema": {
        "nodes": [],
        "edges": []
    },
    "inputs": {
        "input1": "value1",
        "input2": "value2"
    }
}
context.init(params)

# 创建子上下文
sub_context = context.sub()

# 使用变量存储
context.variable_store.set("key1", "value1")
value = context.variable_store.get("key1")  # 返回 "value1"

# 子上下文可以访问父上下文的变量
value = sub_context.variable_store.get("key1")  # 返回 "value1"

# 子上下文可以设置自己的变量
sub_context.variable_store.set("key2", "value2")

# 父上下文无法访问子上下文的变量
value = context.variable_store.get("key2")  # 返回 None

# 释放资源
context.dispose()
```

## 翻译过程中的关键点

在将 JavaScript 代码翻译为 Python 代码的过程中，我注意到以下几个关键点：

1. **命名约定**：JavaScript 使用驼峰命名法（如 `variableStore`），而 Python 使用下划线命名法（如 `variable_store`）。在接口定义中，我们使用了下划线命名法，但在实现中，我们需要确保与接口定义保持一致。

2. **私有属性**：JavaScript 使用 `private` 关键字来定义私有属性，而 Python 使用下划线前缀（如 `_variable_store`）来表示私有属性。在 Python 实现中，我们使用下划线前缀来表示私有属性，并通过属性装饰器 (`@property`) 来提供对这些属性的访问。

3. **类型注解**：JavaScript 使用 TypeScript 的类型注解，而 Python 使用自己的类型注解系统。在 Python 实现中，我们使用了 Python 的类型注解，确保代码的类型安全。

4. **参数传递**：JavaScript 使用对象解构赋值来传递参数，而 Python 没有直接对应的语法。在 Python 实现中，我们使用字典来模拟对象解构赋值，保持了相同的参数传递方式。

5. **接口实现**：JavaScript 使用 `implements` 关键字来表示一个类实现了一个接口，而 Python 没有直接对应的语法。在 Python 实现中，我们通过继承抽象基类来表示接口实现。

通过注意这些关键点，我成功地将 JavaScript 的工作流运行时上下文代码翻译为了 Python 代码，保持了代码的功能和逻辑与原始 JavaScript 代码一致，同时符合 Python 的编码规范和最佳实践。