# runtime-py-core 接口定义总结

本文档总结了 runtime-py-core 项目中实现的接口定义，这些接口是基于原始 JavaScript 项目 runtime-js-core 中的接口定义转换而来。所有接口都使用 Python 的 `abc` 模块和 `typing` 模块来定义抽象基类和类型注解，确保类型安全。

## 接口概览

runtime-py-core 项目的接口定义分为以下几个主要部分：

1. **引擎接口**：定义工作流引擎的接口
2. **任务接口**：定义工作流任务的接口
3. **上下文接口**：定义工作流上下文的接口
4. **节点接口**：定义工作流节点的接口
5. **执行器接口**：定义节点执行器的接口
6. **模式接口**：定义工作流模式的接口

所有接口都位于 `src/interface` 目录下，并通过 `__init__.py` 文件导出。

## 引擎接口 (engine.py)

### IEngine

工作流引擎的接口，负责调用工作流并管理其执行。

```python
class IEngine(ABC):
    @abstractmethod
    def invoke(self, params: InvokeParams) -> ITask:
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        pass
```

## 任务接口 (task.py)

### ITask

工作流任务的接口，表示一个运行中的工作流实例。

```python
class ITask(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def status(self) -> str:
        pass
    
    @property
    @abstractmethod
    def context(self) -> 'IContext':
        pass
    
    @abstractmethod
    def run(self) -> Any:
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        pass
    
    @abstractmethod
    def on_complete(self, callback: Callable[[Any], None]) -> None:
        pass
    
    @abstractmethod
    def on_error(self, callback: Callable[[Exception], None]) -> None:
        pass
```

### TaskParams

创建任务的参数类。

```python
class TaskParams:
    def __init__(self, context: 'IContext', processing: Callable[[], Any]):
        self.context = context
        self.processing = processing
```

## 上下文接口 (context.py)

### IContext

工作流上下文的接口，提供对工作流运行时各个组件的访问。

```python
class IContext(ABC):
    @property
    @abstractmethod
    def document(self) -> IDocument:
        pass
    
    @property
    @abstractmethod
    def variable_store(self) -> IVariableStore:
        pass
    
    @property
    @abstractmethod
    def state(self) -> IState:
        pass
    
    @property
    @abstractmethod
    def io_center(self) -> IIOCenter:
        pass
    
    @property
    @abstractmethod
    def status_center(self) -> IStatusCenter:
        pass
    
    @property
    @abstractmethod
    def snapshot_center(self) -> ISnapshotCenter:
        pass
    
    @property
    @abstractmethod
    def reporter(self) -> IReporter:
        pass
    
    @abstractmethod
    def init(self, params: InvokeParams) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def sub(self) -> 'IContext':
        pass
```

### IDocument

工作流文档的接口，表示工作流定义，包括节点和边。

```python
class IDocument(ABC):
    @property
    @abstractmethod
    def start(self) -> 'INode':
        pass
    
    @abstractmethod
    def init(self, schema: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
```

### IVariableStore

变量存储的接口，管理工作流中使用的变量。

```python
class IVariableStore(ABC):
    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def get(self, key: str) -> Any:
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass
    
    @abstractmethod
    def has(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        pass
    
    @abstractmethod
    def set_parent(self, parent: 'IVariableStore') -> None:
        pass
```

### IState

工作流状态的接口，管理工作流的执行状态。

```python
class IState(ABC):
    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def get_node_inputs(self, node: 'INode') -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def set_node_outputs(self, node: 'INode', outputs: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def add_executed_node(self, node: 'INode') -> None:
        pass
    
    @abstractmethod
    def is_executed_node(self, node: 'INode') -> bool:
        pass
    
    @abstractmethod
    def parse_ref(self, ref: str) -> Any:
        pass
    
    @abstractmethod
    def parse_value(self, value: Any) -> Any:
        pass
```

### IIOCenter

输入输出中心的接口，管理工作流的输入和输出。

```python
class IIOCenter(ABC):
    @property
    @abstractmethod
    def outputs(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def init(self, inputs: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
```

### IStatusCenter

状态中心的接口，管理工作流和节点的状态。

```python
class IStatusCenter(ABC):
    @property
    @abstractmethod
    def workflow(self) -> 'IWorkflowStatus':
        pass
    
    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def node_status(self, node_id: str) -> 'INodeStatus':
        pass
    
    @abstractmethod
    def get_status_node_ids(self, status: str) -> List[str]:
        pass
```

### IWorkflowStatus

工作流状态的接口，管理工作流的状态。

```python
class IWorkflowStatus(ABC):
    @property
    @abstractmethod
    def terminated(self) -> bool:
        pass
    
    @abstractmethod
    def process(self) -> None:
        pass
    
    @abstractmethod
    def success(self) -> None:
        pass
    
    @abstractmethod
    def fail(self) -> None:
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        pass
```

### INodeStatus

节点状态的接口，管理节点的状态。

```python
class INodeStatus(ABC):
    @abstractmethod
    def process(self) -> None:
        pass
    
    @abstractmethod
    def success(self) -> None:
        pass
    
    @abstractmethod
    def fail(self) -> None:
        pass
    
    @abstractmethod
    def cancel(self) -> None:
        pass
```

### ISnapshotCenter

快照中心的接口，管理工作流执行的快照。

```python
class ISnapshotCenter(ABC):
    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def create(self, params: Dict[str, Any]) -> 'ISnapshot':
        pass
```

### ISnapshot

快照的接口，表示节点执行的状态。

```python
class ISnapshot(ABC):
    @abstractmethod
    def add_data(self, data: Dict[str, Any]) -> None:
        pass
```

### IReporter

报告器的接口，生成工作流执行的报告。

```python
class IReporter(ABC):
    @abstractmethod
    def init(self) -> None:
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def export(self) -> 'IReport':
        pass
```

### IReport

报告的接口，包含工作流执行的信息。

```python
class IReport(ABC):
    pass
```

### ContextData

创建上下文的数据类。

```python
class ContextData:
    def __init__(
        self,
        document: IDocument,
        variable_store: IVariableStore,
        state: IState,
        io_center: IIOCenter,
        snapshot_center: ISnapshotCenter,
        status_center: IStatusCenter,
        reporter: IReporter
    ):
        self.document = document
        self.variable_store = variable_store
        self.state = state
        self.io_center = io_center
        self.snapshot_center = snapshot_center
        self.status_center = status_center
        self.reporter = reporter
```

### IContainer

依赖注入容器的接口，管理依赖并提供它们的实例。

```python
class IContainer(Generic[T], ABC):
    @abstractmethod
    def get(self, key: Any) -> T:
        pass
```

## 节点接口 (node.py)

### INode

工作流节点的接口，表示工作流中的处理单元。

```python
class INode(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def type(self) -> str:
        pass
    
    @property
    @abstractmethod
    def data(self) -> Dict[str, Any]:
        pass
    
    @property
    @abstractmethod
    def prev(self) -> List['INode']:
        pass
    
    @property
    @abstractmethod
    def next(self) -> List['INode']:
        pass
    
    @property
    @abstractmethod
    def ports(self) -> IPorts:
        pass
```

### IPort

节点端口的接口，表示节点的输入或输出点。

```python
class IPort(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def type(self) -> str:
        pass
    
    @property
    @abstractmethod
    def node_id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def key(self) -> str:
        pass
```

### IEdge

边的接口，表示两个端口之间的连接。

```python
class IEdge(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def source_port_id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def target_port_id(self) -> str:
        pass
```

### IPorts

节点端口集合的接口，提供对节点输入和输出端口的访问。

```python
class IPorts(ABC):
    @property
    @abstractmethod
    def inputs(self) -> Dict[str, IPort]:
        pass
    
    @property
    @abstractmethod
    def outputs(self) -> Dict[str, IPort]:
        pass
```

### FlowGramNode

节点类型的枚举。

```python
class FlowGramNode(str, Enum):
    Start = "start"
    End = "end"
    LLM = "llm"
    Condition = "condition"
    Loop = "loop"
```

### WorkflowVariableType

工作流变量类型的枚举。

```python
class WorkflowVariableType(str, Enum):
    String = "string"
    Number = "number"
    Boolean = "boolean"
    Object = "object"
    Array = "array"
    Null = "null"
```

## 执行器接口 (executor.py)

### IExecutor

工作流执行器的接口，负责执行工作流中的节点。

```python
class IExecutor(ABC):
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        pass
```

### INodeExecutor

节点执行器的接口，负责执行特定类型的节点。

```python
class INodeExecutor(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        pass
    
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        pass
```

### INodeExecutorFactory

节点执行器工厂的接口，为特定类型的节点创建执行器。

```python
class INodeExecutorFactory(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        pass
    
    @abstractmethod
    def create(self) -> INodeExecutor:
        pass
```

### ExecutionContext

节点执行的上下文类。

```python
class ExecutionContext:
    def __init__(self, node: INode, inputs: Dict[str, Any], runtime: IContext, container: Any):
        self.node = node
        self.inputs = inputs
        self.runtime = runtime
        self.container = container
```

### ExecutionResult

节点执行的结果类。

```python
class ExecutionResult:
    def __init__(self, outputs: Dict[str, Any], branch: Optional[str] = None):
        self.outputs = outputs
        self.branch = branch
```

### EngineServices

工作流引擎的服务类。

```python
class EngineServices:
    def __init__(self, executor: IExecutor):
        self.Executor = executor
```

## 模式接口 (schema.py)

### WorkflowSchema

工作流模式的类型定义。

```python
class WorkflowSchema(TypedDict):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]
```

### NodeSchema

节点模式的类型定义。

```python
class NodeSchema(TypedDict):
    id: str
    type: str
    data: Dict[str, Any]
    ports: Dict[str, List[PortSchema]]
```

### PortSchema

端口模式的类型定义。

```python
class PortSchema(TypedDict):
    id: str
    type: str
    nodeId: str
    key: str
```

### EdgeSchema

边模式的类型定义。

```python
class EdgeSchema(TypedDict):
    id: str
    sourcePortId: str
    targetPortId: str
```

### InvokeParams

调用工作流的参数类。

```python
class InvokeParams:
    def __init__(self, schema: Union[str, Dict[str, Any]], inputs: Dict[str, Any]):
        self.schema = schema
        self.inputs = inputs
```

### WorkflowOutputs

工作流输出的类型定义。

```python
class WorkflowOutputs(TypedDict):
    outputs: Dict[str, Any]
```

### TaskRunInput

任务运行 API 的输入类型定义。

```python
class TaskRunInput(TypedDict):
    schema: str
    inputs: Dict[str, Any]
```

### TaskRunOutput

任务运行 API 的输出类型定义。

```python
class TaskRunOutput(TypedDict):
    taskID: str
```

### TaskReportInput

任务报告 API 的输入类型定义。

```python
class TaskReportInput(TypedDict):
    taskID: str
```

### TaskResultInput

任务结果 API 的输入类型定义。

```python
class TaskResultInput(TypedDict):
    taskID: str
```

### TaskCancelInput

任务取消 API 的输入类型定义。

```python
class TaskCancelInput(TypedDict):
    taskID: str
```

### WorkflowStatus

工作流状态的枚举。

```python
class WorkflowStatus(str, Enum):
    Processing = "processing"
    Success = "success"
    Failed = "failed"
    Cancelled = "cancelled"
```

### FlowGramAPIName

FlowGram API 名称的枚举。

```python
class FlowGramAPIName(str, Enum):
    TaskRun = "taskRun"
    TaskReport = "taskReport"
    TaskResult = "taskResult"
    TaskCancel = "taskCancel"
    ServerInfo = "serverInfo"
    Validation = "validation"
```

## 接口导出 (__init__.py)

所有接口和类型都通过 `__init__.py` 文件导出，按照以下分类组织：

```python
# Engine interfaces
from .engine import IEngine

# Task interfaces
from .task import ITask, TaskParams

# Context interfaces
from .context import (
    IContext, IVariableStore, IDocument, IState, IIOCenter,
    IStatusCenter, IWorkflowStatus, INodeStatus, ISnapshotCenter,
    ISnapshot, IReporter, IReport, ContextData, IContainer
)

# Node interfaces
from .node import (
    INode, IPort, IEdge, IPorts,
    FlowGramNode, WorkflowVariableType
)

# Executor interfaces
from .executor import (
    IExecutor, INodeExecutor, INodeExecutorFactory,
    ExecutionContext, ExecutionResult, EngineServices
)

# Schema interfaces
from .schema import (
    WorkflowSchema, NodeSchema, PortSchema, EdgeSchema,
    InvokeParams, WorkflowOutputs, TaskRunInput, TaskRunOutput,
    TaskReportInput, TaskResultInput, TaskCancelInput,
    WorkflowStatus, FlowGramAPIName
)
```

## 接口依赖关系

接口之间的依赖关系如下：

1. `IEngine` 依赖于 `ITask` 和 `InvokeParams`
2. `ITask` 依赖于 `IContext`
3. `IContext` 依赖于 `IDocument`、`IVariableStore`、`IState`、`IIOCenter`、`IStatusCenter`、`ISnapshotCenter`、`IReporter` 和 `InvokeParams`
4. `IDocument` 依赖于 `INode`
5. `IState` 依赖于 `INode`
6. `INodeExecutor` 依赖于 `ExecutionContext` 和 `ExecutionResult`
7. `ExecutionContext` 依赖于 `INode`、`IContext` 和 `IContainer`

为了避免循环导入问题，我们使用了 Python 的前向引用（forward reference）机制，在需要的地方使用字符串类型注解，如 `'IContext'`、`'INode'` 等。

## 总结

runtime-py-core 项目的接口定义完整、准确，并与原始 JavaScript 代码保持一致。我们使用了 Python 的 `abc` 模块和 `typing` 模块来定义抽象基类和类型注解，确保类型安全。所有接口都按照功能分类组织，并通过 `__init__.py` 文件导出，方便其他模块导入使用。

接口之间的依赖关系也得到了正确处理，避免了循环导入问题。这些接口定义为后续实现具体的功能提供了良好的基础。