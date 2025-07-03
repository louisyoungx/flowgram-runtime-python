# runtime-js-core 接口定义摘要

本文档总结了 runtime-js-core 项目中使用的主要接口和类型定义，特别是从 @flowgram.ai/runtime-interface 包中导入的接口。这些接口将在 Python 版本中转换为接口定义。

## API 层接口

### TaskRunInput 和 TaskRunOutput

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { TaskRunInput, TaskRunOutput } from '@flowgram.ai/runtime-interface';

// TaskRunAPI 函数签名
export const TaskRunAPI = async (input: TaskRunInput): Promise<TaskRunOutput> => {
  // ...
};

// TaskRunInput 包含工作流模式和输入
// 示例用法
const { schema: stringSchema, inputs } = input;
const schema = JSON.parse(stringSchema);

// TaskRunOutput 包含任务 ID
// 示例用法
const output: TaskRunOutput = {
  taskID,
};
```

### FlowGramAPIName

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { FlowGramAPIName } from '@flowgram.ai/runtime-interface';

// WorkflowRuntimeAPIs 对象使用 FlowGramAPIName 作为键
export const WorkflowRuntimeAPIs: Record<FlowGramAPIName, (i: any) => any> = {
  [FlowGramAPIName.TaskRun]: TaskRunAPI,
  [FlowGramAPIName.TaskReport]: TaskReportAPI,
  [FlowGramAPIName.TaskResult]: TaskResultAPI,
  [FlowGramAPIName.TaskCancel]: TaskCancelAPI,
  [FlowGramAPIName.ServerInfo]: () => {}, // TODO
  [FlowGramAPIName.Validation]: () => {}, // TODO
};
```

## 应用层接口

### InvokeParams

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { InvokeParams } from '@flowgram.ai/runtime-interface';

// InvokeParams 用于调用工作流
// 示例用法
public run(params: InvokeParams): string {
  const engine = this.container.get<IEngine>(IEngine);
  const task = engine.invoke(params);
  // ...
}
```

### IContainer

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IContainer } from '@flowgram.ai/runtime-interface';

// IContainer 用于依赖注入
// 示例用法
private container: IContainer;

// 获取依赖
const engine = this.container.get<IEngine>(IEngine);
```

### IEngine

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IEngine } from '@flowgram.ai/runtime-interface';

// IEngine 是工作流引擎的接口
// 示例用法
const engine = this.container.get<IEngine>(IEngine);
const task = engine.invoke(params);
```

### ITask

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { ITask } from '@flowgram.ai/runtime-interface';

// ITask 是工作流任务的接口
// 示例用法
public tasks: Map<string, ITask>;

// 任务方法
task.cancel();
task.context.reporter.export();
task.context.ioCenter.outputs;
```

### IReport

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IReport } from '@flowgram.ai/runtime-interface';

// IReport 是工作流报告的接口
// 示例用法
public report(taskID: string): IReport | undefined {
  // ...
  return task.context.reporter.export();
}
```

### WorkflowOutputs

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { WorkflowOutputs } from '@flowgram.ai/runtime-interface';

// WorkflowOutputs 是工作流输出的类型
// 示例用法
public result(taskID: string): WorkflowOutputs | undefined {
  // ...
  return task.context.ioCenter.outputs;
}
```

## 领域层接口

### EngineServices

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { EngineServices } from '@flowgram.ai/runtime-interface';

// EngineServices 用于提供引擎服务
// 示例用法
constructor(service: EngineServices) {
  this.executor = service.Executor;
}
```

### IExecutor

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IExecutor } from '@flowgram.ai/runtime-interface';

// IExecutor 是节点执行器的接口
// 示例用法
private readonly executor: IExecutor;

// 执行节点
const result = await this.executor.execute({
  node,
  inputs,
  runtime: context,
  container: WorkflowRuntimeContainer.instance,
});
```

### INode

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { INode } from '@flowgram.ai/runtime-interface';

// INode 是工作流节点的接口
// 示例用法
public async executeNode(params: { context: IContext; node: INode }) {
  const { node, context } = params;
  // ...
}

// 节点属性
node.id
node.type
node.data
node.prev
node.next
node.ports.outputs
```

### IContext

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IContext } from '@flowgram.ai/runtime-interface';

// IContext 是工作流上下文的接口
// 示例用法
public readonly context: IContext;

// 上下文方法和属性
context.init(params);
context.dispose();
context.sub();
context.document.start;
context.variableStore;
context.state;
context.ioCenter;
context.snapshotCenter;
context.statusCenter;
context.reporter;
```

### TaskParams

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { TaskParams } from '@flowgram.ai/runtime-interface';

// TaskParams 是创建任务的参数类型
// 示例用法
constructor(params: TaskParams) {
  this.id = uuid();
  this.context = params.context;
  this.processing = params.processing;
}
```

### WorkflowStatus

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { WorkflowStatus } from '@flowgram.ai/runtime-interface';

// WorkflowStatus 是工作流状态的枚举
// 示例用法
const cancelNodeIDs = this.context.statusCenter.getStatusNodeIDs(WorkflowStatus.Processing);
```

### FlowGramNode

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { FlowGramNode } from '@flowgram.ai/runtime-interface';

// FlowGramNode 是节点类型的枚举
// 示例用法
public type = FlowGramNode.LLM;
public type = FlowGramNode.Condition;

// 判断节点类型
if (node.type === FlowGramNode.End) {
  return;
}
```

### ContextData

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { ContextData } from '@flowgram.ai/runtime-interface';

// ContextData 是创建上下文的数据类型
// 示例用法
constructor(data: ContextData) {
  this.id = uuid();
  this.document = data.document;
  this.variableStore = data.variableStore;
  this.state = data.state;
  this.ioCenter = data.ioCenter;
  this.snapshotCenter = data.snapshotCenter;
  this.statusCenter = data.statusCenter;
  this.reporter = data.reporter;
}
```

### IDocument

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IDocument } from '@flowgram.ai/runtime-interface';

// IDocument 是工作流文档的接口
// 示例用法
public readonly document: IDocument;

// 文档方法和属性
this.document.init(schema);
this.document.dispose();
context.document.start;
```

### IState

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IState } from '@flowgram.ai/runtime-interface';

// IState 是工作流状态的接口
// 示例用法
public readonly state: IState;

// 状态方法
this.state.init();
this.state.dispose();
context.state.getNodeInputs(node);
context.state.setNodeOutputs({ node, outputs });
context.state.addExecutedNode(node);
context.state.isExecutedNode(prevNode);
context.state.parseRef(left);
context.state.parseValue(right);
```

### ISnapshotCenter

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { ISnapshotCenter } from '@flowgram.ai/runtime-interface';

// ISnapshotCenter 是快照中心的接口
// 示例用法
public readonly snapshotCenter: ISnapshotCenter;

// 快照中心方法
this.snapshotCenter.init();
this.snapshotCenter.dispose();
const snapshot = context.snapshotCenter.create({
  nodeID: node.id,
  data: node.data,
  inputs,
});
snapshot.addData({ outputs, branch });
```

### IVariableStore

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IVariableStore } from '@flowgram.ai/runtime-interface';

// IVariableStore 是变量存储的接口
// 示例用法
public readonly variableStore: IVariableStore;

// 变量存储方法
this.variableStore.init();
this.variableStore.dispose();
variableStore.setParent(this.variableStore);
```

### IStatusCenter

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IStatusCenter } from '@flowgram.ai/runtime-interface';

// IStatusCenter 是状态中心的接口
// 示例用法
public readonly statusCenter: IStatusCenter;

// 状态中心方法和属性
this.statusCenter.init();
this.statusCenter.dispose();
context.statusCenter.workflow.process();
context.statusCenter.workflow.success();
context.statusCenter.workflow.fail();
context.statusCenter.workflow.cancel();
context.statusCenter.workflow.terminated;
context.statusCenter.nodeStatus(node.id).process();
context.statusCenter.nodeStatus(node.id).success();
context.statusCenter.nodeStatus(node.id).fail();
context.statusCenter.nodeStatus(node.id).cancel();
context.statusCenter.getStatusNodeIDs(WorkflowStatus.Processing);
```

### IReporter

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IReporter } from '@flowgram.ai/runtime-interface';

// IReporter 是报告器的接口
// 示例用法
public readonly reporter: IReporter;

// 报告器方法
this.reporter.init();
this.reporter.dispose();
task.context.reporter.export();
```

### IIOCenter

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { IIOCenter } from '@flowgram.ai/runtime-interface';

// IIOCenter 是输入输出中心的接口
// 示例用法
public readonly ioCenter: IIOCenter;

// 输入输出中心方法和属性
this.ioCenter.init(inputs);
this.ioCenter.dispose();
context.ioCenter.outputs;
```

## 节点层接口

### INodeExecutorFactory

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { INodeExecutorFactory } from '@flowgram.ai/runtime-interface';

// INodeExecutorFactory 是节点执行器工厂的接口
// 示例用法
export const WorkflowRuntimeNodeExecutors: INodeExecutorFactory[] = [
  StartExecutor,
  EndExecutor,
  LLMExecutor,
  ConditionExecutor,
  LoopExecutor,
];
```

### ExecutionContext

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { ExecutionContext } from '@flowgram.ai/runtime-interface';

// ExecutionContext 是节点执行的上下文
// 示例用法
public async execute(context: ExecutionContext): Promise<ExecutionResult> {
  const inputs = context.inputs as LLMExecutorInputs;
  // ...
}
```

### ExecutionResult

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { ExecutionResult } from '@flowgram.ai/runtime-interface';

// ExecutionResult 是节点执行的结果
// 示例用法
return {
  outputs: {
    result,
  },
};

// 带分支的结果
return {
  outputs: {},
  branch: activatedCondition.key,
};
```

### INodeExecutor

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { INodeExecutor } from '@flowgram.ai/runtime-interface';

// INodeExecutor 是节点执行器的接口
// 示例用法
export class LLMExecutor implements INodeExecutor {
  public type = FlowGramNode.LLM;
  
  public async execute(context: ExecutionContext): Promise<ExecutionResult> {
    // ...
  }
}
```

### WorkflowVariableType

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { WorkflowVariableType } from '@flowgram.ai/runtime-interface';

// WorkflowVariableType 是工作流变量类型的枚举
// 示例用法
const leftType = parsedLeft?.type ?? WorkflowVariableType.Null;
const rightType = parsedRight?.type ?? WorkflowVariableType.Null;
```

## 其他类型

### WorkflowSchema

```typescript
// 从 @flowgram.ai/runtime-interface 导入
import { WorkflowSchema } from '@flowgram.ai/runtime-interface';

// WorkflowSchema 是工作流模式的类型
// 示例用法（从测试文件）
export const basicSchema: WorkflowSchema = {
  nodes: [
    // 节点定义
  ],
  edges: [
    // 边定义
  ],
};
```

## 自定义接口

### LLMExecutorInputs

```typescript
// LLM 节点执行器的输入接口
export interface LLMExecutorInputs {
  modelName: string;
  apiKey: string;
  apiHost: string;
  temperature: number;
  systemPrompt?: string;
  prompt: string;
}
```

### ConditionItem, ConditionValue, Conditions

```typescript
// 条件节点的类型定义
import { ConditionItem, ConditionValue, Conditions } from './type';

// 示例用法
const conditions: Conditions = context.node.data?.conditions;
const parsedConditions = conditions
  .map((item) => this.parseCondition(item, context))
  .filter((item) => this.checkCondition(item));
```

## 总结

runtime-js-core 项目使用了大量的接口和类型定义，主要来自 @flowgram.ai/runtime-interface 包。这些接口定义了工作流运行时的核心组件，包括引擎、任务、上下文、节点等。在将项目转换为 Python 版本时，需要将这些接口转换为 Python 的接口定义，保持接口的一致性和兼容性。