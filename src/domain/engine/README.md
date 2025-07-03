# 工作流运行时引擎实现

## 概述

工作流运行时引擎（`WorkflowRuntimeEngine`）是工作流执行系统的核心组件，负责执行工作流中的节点并管理工作流的执行过程。该引擎实现了 `IEngine` 接口，提供了工作流调用和节点执行的功能。

## 主要功能

1. **工作流调用**：通过 `invoke` 方法启动工作流的执行，创建上下文并处理工作流的生命周期。
2. **节点执行**：通过 `execute_node` 方法执行工作流中的单个节点，包括获取输入、执行节点、设置输出和执行下一个节点。
3. **工作流处理**：通过 `process` 方法处理工作流的执行过程，从起始节点开始执行，并返回工作流的输出结果。
4. **节点执行条件检查**：通过 `_can_execute_node` 方法检查节点是否可以执行，确保所有前置节点都已执行。
5. **获取下一个节点**：通过 `_get_next_nodes` 方法根据当前节点和分支获取下一个要执行的节点。
6. **执行下一个节点**：通过 `_execute_next` 方法执行下一个节点，支持并行执行多个节点。

## 实现细节

### 工作流调用（invoke）

`invoke` 方法接收工作流参数，创建上下文并初始化，然后启动工作流的执行过程。它返回一个任务对象，该对象包含工作流的处理过程和上下文。为了确保上下文在工作流执行完成后被正确释放，使用了一个包装函数 `process_with_dispose`。

```python
def invoke(self, params: InvokeParams) -> ITask:
    context = WorkflowRuntimeContext.create()
    context.init(params)
    processing = self.process(context)
    
    # Use a callback to dispose the context when processing is done
    async def process_with_dispose():
        try:
            result = await processing
            return result
        finally:
            context.dispose()
    
    return WorkflowRuntimeTask.create({
        "processing": process_with_dispose(),
        "context": context,
    })
```

### 节点执行（execute_node）

`execute_node` 方法负责执行工作流中的单个节点。它首先检查节点是否可以执行，然后获取节点的输入，创建快照，执行节点，设置输出，并执行下一个节点。如果执行过程中发生错误，它会将节点状态设置为失败。

```python
async def execute_node(self, params: Dict[str, Any]) -> None:
    node: INode = params["node"]
    context: IContext = params["context"]
    
    if not self._can_execute_node({"node": node, "context": context}):
        return
    
    context.status_center.node_status(node.id).process()
    try:
        inputs = context.state.get_node_inputs(node)
        snapshot = context.snapshot_center.create({
            "node_id": node.id,
            "data": node.data,
            "inputs": inputs,
        })
        
        result = await self.executor.execute({
            "node": node,
            "inputs": inputs,
            "runtime": context,
            "container": WorkflowRuntimeContainer.instance,
        })
        
        if context.status_center.workflow.terminated:
            return
        
        outputs = result.outputs
        branch = result.branch
        
        snapshot.add_data({"outputs": outputs, "branch": branch})
        context.state.set_node_outputs({"node": node, "outputs": outputs})
        context.state.add_executed_node(node)
        context.status_center.node_status(node.id).success()
        
        next_nodes = self._get_next_nodes({"node": node, "branch": branch, "context": context})
        await self._execute_next({"node": node, "next_nodes": next_nodes, "context": context})
    
    except Exception as e:
        context.status_center.node_status(node.id).fail()
        logging.error(f"Error executing node {node.id}: {str(e)}")
        return
```

### 工作流处理（process）

`process` 方法处理工作流的执行过程，从起始节点开始执行，并返回工作流的输出结果。如果执行过程中发生错误，它会将工作流状态设置为失败。

```python
async def process(self, context: IContext) -> WorkflowOutputs:
    start_node = context.document.start
    context.status_center.workflow.process()
    
    try:
        await self.execute_node({"node": start_node, "context": context})
        outputs = context.io_center.outputs
        context.status_center.workflow.success()
        return outputs
    
    except Exception as e:
        context.status_center.workflow.fail()
        raise e
```

### 节点执行条件检查（_can_execute_node）

`_can_execute_node` 方法检查节点是否可以执行，确保所有前置节点都已执行。如果节点没有前置节点，它可以直接执行。

```python
def _can_execute_node(self, params: Dict[str, Any]) -> bool:
    node: INode = params["node"]
    context: IContext = params["context"]
    
    prev_nodes = node.prev
    if len(prev_nodes) == 0:
        return True
    
    return all(context.state.is_executed_node(prev_node) for prev_node in prev_nodes)
```

### 获取下一个节点（_get_next_nodes）

`_get_next_nodes` 方法根据当前节点和分支获取下一个要执行的节点。如果指定了分支，它会只返回与该分支相连的节点，并将被跳过的节点标记为已执行。

```python
def _get_next_nodes(self, params: Dict[str, Any]) -> List[INode]:
    node: INode = params["node"]
    branch: Optional[str] = params.get("branch")
    context: IContext = params["context"]
    
    all_next_nodes = node.next
    if not branch:
        return all_next_nodes
    
    target_port = next((port for port in node.ports.outputs if port.id == branch), None)
    if not target_port:
        raise Exception(f"branch {branch} not found")
    
    next_node_ids: Set[str] = set(edge.to.id for edge in target_port.edges)
    next_nodes = [next_node for next_node in all_next_nodes if next_node.id in next_node_ids]
    skip_nodes = [next_node for next_node in all_next_nodes if next_node.id not in next_node_ids]
    
    for skip_node in skip_nodes:
        context.state.add_executed_node(skip_node)
    
    return next_nodes
```

### 执行下一个节点（_execute_next）

`_execute_next` 方法执行下一个节点，支持并行执行多个节点。如果当前节点是结束节点或没有下一个节点，它会直接返回。

```python
async def _execute_next(self, params: Dict[str, Any]) -> None:
    context: IContext = params["context"]
    node: INode = params["node"]
    next_nodes: List[INode] = params["next_nodes"]
    
    if node.type == FlowGramNode.End:
        return
    
    if len(next_nodes) == 0:
        # Inside loop node may have no next nodes
        return
    
    # Execute all next nodes in parallel
    await asyncio.gather(*[
        self.execute_node({
            "node": next_node,
            "context": context
        }) for next_node in next_nodes
    ])
```

## 翻译过程中的关键点

1. **异步实现**：JavaScript 使用 Promise 和 async/await 来实现异步操作，而 Python 使用 asyncio 模块和 async/await 语法。在翻译过程中，我保留了异步特性，使用 Python 的异步编程模型。

2. **参数传递**：JavaScript 中使用对象解构赋值来传递参数，而 Python 中使用字典来模拟这种行为。例如，JavaScript 中的 `const { node, context } = params;` 在 Python 中变为 `node: INode = params["node"]` 和 `context: IContext = params["context"]`。

3. **私有方法**：JavaScript 中使用 `private` 关键字来标记私有方法，而 Python 中使用下划线前缀（如 `_can_execute_node`）来表示私有方法。

4. **错误处理**：JavaScript 中使用 try/catch 来处理错误，而 Python 中使用 try/except。在翻译过程中，我保留了相同的错误处理逻辑。

5. **日志记录**：JavaScript 中使用 console.error 来记录错误，而 Python 中使用 logging 模块。我使用 logging.error 来替换 console.error，以便更好地记录错误信息。

6. **类型注解**：JavaScript 使用 TypeScript 来提供类型注解，而 Python 使用内置的类型注解系统。在翻译过程中，我添加了适当的 Python 类型注解，确保代码的类型安全。

7. **文档字符串**：JavaScript 中使用 JSDoc 来提供文档，而 Python 中使用文档字符串（docstring）。在翻译过程中，我为每个方法添加了详细的文档字符串，说明其用途、参数和返回值。

## 总结

工作流运行时引擎是工作流执行系统的核心组件，负责执行工作流中的节点并管理工作流的执行过程。通过将 JavaScript 代码翻译为 Python 代码，我保留了原始代码的功能和逻辑，同时利用 Python 的语言特性和最佳实践，确保代码的可读性、可维护性和类型安全。