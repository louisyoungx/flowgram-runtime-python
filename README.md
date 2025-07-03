# FlowGram Python Runtime

## 注意 ⚠️ 不可用于生产环境！

**本项目所有代码均为 AI 生成，仅作为技术交流和学习使用，不建议在生产环境中使用。**

这个仓库所有代码，包括代码编写、调试、测试等都是 AI 完成的，采用 Vibe Coding 的方式，用自然语言描述需求，没有写一行代码。

prompt 放在 [prompt.md](./prompt.md) 文件中了，主要是和 AI 斗志斗勇的过程，并没有采用很高深的 prompt engineering 技巧。

AI 生成的一些中间文档在 [docs](./docs) 目录中，包括代码生成的目录结构、类图、接口定义等。

AI 生成的调试代码在 [scripts](./scripts) 目录中，包括运行测试用例、调试代码等。注意这部分原本是在根目录下的，整理时为了项目可读性才单独建了个文件夹，如果想运行需要先移回根目录。

## 项目概述

FlowGram Python Runtime 是 [flowgram-runtime-js](https://github.com/bytedance/flowgram.ai/tree/main/packages/runtime/js-core) 的 Python 实现版本，旨在提供一个高效、可扩展的工作流运行时引擎。该项目保持与原始 JavaScript 版本相同的目录结构和功能，但利用了 Python 的语言特性和最佳实践。

### 核心功能

- **工作流执行**：执行由节点和边组成的工作流图
- **节点执行**：支持多种类型的节点，包括开始节点、结束节点、LLM 节点、条件节点和循环节点
- **状态管理**：跟踪工作流执行的状态，包括已执行的节点和节点的输出
- **变量存储**：管理工作流中的变量，支持父子变量存储的继承关系
- **上下文管理**：提供工作流执行的上下文，包括文档、变量存储、状态等组件
- **报告生成**：生成工作流执行的报告，包括执行时间、执行路径等信息

## 安装说明

### 前提条件

- Python 3.8 或更高版本
- pip 包管理器

### 安装

1. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

2. 安装依赖项

```bash
pip install -r requirements.txt
```

依赖项包括：
- pydantic>=2.0.0
- typing-extensions>=4.0.0
- uuid>=1.30
- fastapi>=0.100.0
- uvicorn>=0.22.0
- starlette>=0.27.0
- python-multipart>=0.0.6

### 启动服务器

项目提供了一个基于 FastAPI 的 RESTful API 服务器，用于通过 HTTP 接口与工作流运行时交互。

```bash
python run.py
```

服务器将在 http://localhost:4000 上运行，Swagger 文档可在 http://localhost:4000/api/docs 访问。

#### API 端点

服务器提供以下 API 端点：

1. **POST /api/task/run** - 运行工作流任务
2. **GET /api/task/result** - 获取任务结果
3. **GET /api/task/report** - 获取任务报告
4. **PUT /api/task/cancel** - 取消任务

#### 使用 curl 测试 API

```bash
# 运行任务
curl --location 'http://localhost:4000/api/task/run' \
--header 'Content-Type: application/json' \
--data '{
  "inputs": {
      "model_name": "ep-20250206192339-nnr9m",
      "api_key": "your-api-key",
      "api_host": "https://api-host/api/v3",
      "prompt": "Just give me the answer of '\''1+1=?'\'', just one number, no other words"
  },
  "schema": "{\"nodes\":[{\"id\":\"start_0\",\"type\":\"start\",\"meta\":{\"position\":{\"x\":0,\"y\":0}},\"data\":{\"title\":\"Start\",\"outputs\":{\"type\":\"object\",\"properties\":{\"model_name\":{\"key\":14,\"name\":\"model_name\",\"type\":\"string\",\"extra\":{\"index\":1},\"isPropertyRequired\":true},\"prompt\":{\"key\":5,\"name\":\"prompt\",\"type\":\"string\",\"extra\":{\"index\":3},\"isPropertyRequired\":true},\"api_key\":{\"key\":19,\"name\":\"api_key\",\"type\":\"string\",\"extra\":{\"index\":4},\"isPropertyRequired\":true},\"api_host\":{\"key\":20,\"name\":\"api_host\",\"type\":\"string\",\"extra\":{\"index\":5},\"isPropertyRequired\":true}},\"required\":[\"model_name\",\"prompt\",\"api_key\",\"api_host\"]}}},{\"id\":\"end_0\",\"type\":\"end\",\"meta\":{\"position\":{\"x\":1000,\"y\":0}},\"data\":{\"title\":\"End\",\"inputsValues\":{\"answer\":{\"type\":\"ref\",\"content\":[\"llm_0\",\"result\"]}},\"inputs\":{\"type\":\"object\",\"properties\":{\"answer\":{\"type\":\"string\"}}}}},{\"id\":\"llm_0\",\"type\":\"llm\",\"meta\":{\"position\":{\"x\":500,\"y\":0}},\"data\":{\"title\":\"LLM_0\",\"inputsValues\":{\"modelName\":{\"type\":\"ref\",\"content\":[\"start_0\",\"model_name\"]},\"apiKey\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_key\"]},\"apiHost\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_host\"]},\"temperature\":{\"type\":\"constant\",\"content\":0},\"prompt\":{\"type\":\"ref\",\"content\":[\"start_0\",\"prompt\"]},\"systemPrompt\":{\"type\":\"constant\",\"content\":\"You are a helpful AI assistant.\"}},\"inputs\":{\"type\":\"object\",\"required\":[\"modelName\",\"temperature\",\"prompt\"],\"properties\":{\"modelName\":{\"type\":\"string\"},\"apiKey\":{\"type\":\"string\"},\"apiHost\":{\"type\":\"string\"},\"temperature\":{\"type\":\"number\"},\"systemPrompt\":{\"type\":\"string\"},\"prompt\":{\"type\":\"string\"}}},\"outputs\":{\"type\":\"object\",\"properties\":{\"result\":{\"type\":\"string\"}}}}}],\"edges\":[{\"sourceNodeID\":\"start_0\",\"targetNodeID\":\"llm_0\"},{\"sourceNodeID\":\"llm_0\",\"targetNodeID\":\"end_0\"}]}"
}'

# 获取任务结果（替换 taskID）
curl --location 'http://localhost:4000/api/task/result?taskID=YOUR_TASK_ID'

# 获取任务报告（替换 taskID）
curl --location 'http://localhost:4000/api/task/report?taskID=YOUR_TASK_ID'

# 取消任务（替换 taskID）
curl --location --request PUT 'http://localhost:4000/api/task/cancel' \
--header 'Content-Type: application/json' \
--data '{
  "taskID": "YOUR_TASK_ID"
}'
```

#### 使用测试脚本

项目提供了一个测试脚本，用于验证 API 端点的功能：

```bash
# 先启动服务器
python run.py

# 在另一个终端中运行测试脚本
python scripts/test_api_functions.py
```

测试脚本将执行以下操作：
1. 调用 TaskRunAPI 启动一个简单的工作流
2. 等待工作流执行完成
3. 调用 TaskReportAPI 获取工作流执行报告
4. 调用 TaskResultAPI 获取工作流执行结果
5. 验证返回的结果是否符合预期

## API 文档

### TaskRun API

TaskRun API 用于启动工作流执行，接收工作流模式和输入参数，返回任务 ID。

**请求参数：**

| 参数名 | 类型   | 描述                     |
| ------ | ------ | ------------------------ |
| schema | string | 工作流模式的 JSON 字符串 |
| inputs | object | 工作流的输入参数         |

**响应参数：**

| 参数名 | 类型   | 描述                                |
| ------ | ------ | ----------------------------------- |
| taskID | string | 任务 ID，用于后续查询任务状态和结果 |

**示例：**

```python
task_run_output = await TaskRunAPI({
    "schema": json.dumps(workflow_schema),
    "inputs": inputs
})
task_id = task_run_output["taskID"]
```

### TaskReport API

TaskReport API 用于获取工作流执行的报告，包括工作流状态、节点状态和快照信息。

**请求参数：**

| 参数名 | 类型   | 描述    |
| ------ | ------ | ------- |
| taskID | string | 任务 ID |

**响应参数：**

| 参数名         | 类型   | 描述             |
| -------------- | ------ | ---------------- |
| id             | string | 任务 ID          |
| inputs         | object | 工作流的输入参数 |
| outputs        | object | 工作流的输出结果 |
| workflowStatus | object | 工作流的状态信息 |
| reports        | object | 节点的报告信息   |

**workflowStatus 结构：**

| 参数名     | 类型    | 描述                                                   |
| ---------- | ------- | ------------------------------------------------------ |
| status     | string  | 工作流状态（processing、succeeded、failed、cancelled） |
| terminated | boolean | 工作流是否已终止                                       |
| startTime  | number  | 工作流开始时间（毫秒时间戳）                           |
| endTime    | number  | 工作流结束时间（毫秒时间戳），可选                     |
| timeCost   | number  | 工作流执行耗时（毫秒）                                 |

**reports 结构：**

每个节点的报告包含以下字段：

| 参数名     | 类型    | 描述                                                 |
| ---------- | ------- | ---------------------------------------------------- |
| id         | string  | 节点 ID                                              |
| status     | string  | 节点状态（processing、succeeded、failed、cancelled） |
| terminated | boolean | 节点是否已终止                                       |
| startTime  | number  | 节点开始时间（毫秒时间戳）                           |
| endTime    | number  | 节点结束时间（毫秒时间戳），可选                     |
| timeCost   | number  | 节点执行耗时（毫秒）                                 |
| snapshots  | array   | 节点执行的快照数组                                   |

**示例：**

```python
report = await TaskReportAPI({"taskID": task_id})
```

### TaskResult API

TaskResult API 用于获取工作流执行的结果，仅在工作流终止后返回结果。

**请求参数：**

| 参数名 | 类型   | 描述    |
| ------ | ------ | ------- |
| taskID | string | 任务 ID |

**响应参数：**

工作流的输出结果，类型为 object。结果的具体结构取决于工作流的定义。

**示例：**

```python
result = await TaskResultAPI({"taskID": task_id})
```

### TaskCancel API

TaskCancel API 用于取消工作流执行，返回取消操作是否成功。

**请求参数：**

| 参数名 | 类型   | 描述    |
| ------ | ------ | ------- |
| taskID | string | 任务 ID |

**响应参数：**

| 参数名  | 类型    | 描述             |
| ------- | ------- | ---------------- |
| success | boolean | 取消操作是否成功 |

**示例：**

```python
cancel_result = await TaskCancelAPI({"taskID": task_id})
```

## 内核使用说明（高级）

### 示例

```python
from runtime_py_core.api import TaskRunAPI, TaskResultAPI, TaskReportAPI, TaskCancelAPI
import json
import asyncio

# 创建一个简单的工作流模式
workflow_schema = {
    "nodes": [
        {
            "id": "start",
            "type": "start",
            "position": {"x": 0, "y": 0},
            "ports": {
                "out": [{"id": "out", "type": "out"}]
            }
        },
        {
            "id": "end",
            "type": "end",
            "position": {"x": 200, "y": 0},
            "ports": {
                "in": [{"id": "in", "type": "in"}]
            }
        }
    ],
    "edges": [
        {
            "id": "edge1",
            "source": {"nodeId": "start", "portId": "out"},
            "target": {"nodeId": "end", "portId": "in"}
        }
    ]
}

# 创建输入参数
inputs = {
    "message": "Hello, World!"
}

# 运行工作流
async def run_workflow():
    # 运行工作流
    task_run_output = await TaskRunAPI({
        "schema": json.dumps(workflow_schema),
        "inputs": inputs
    })
    
    task_id = task_run_output["taskID"]
    print(f"Task ID: {task_id}")
    
    # 获取任务结果
    result = await TaskResultAPI({"taskID": task_id})
    print(f"Task Result: {result}")
    
    # 获取任务报告
    report = await TaskReportAPI({"taskID": task_id})
    print(f"Task Report: {report}")
    
    # 取消任务（如果需要）
    # cancel_result = await TaskCancelAPI({"taskID": task_id})
    # print(f"Task Cancel Result: {cancel_result}")

# 运行示例
asyncio.run(run_workflow())
```

### 用法

```python
from runtime_py_core.application import WorkflowApplication
from runtime_py_core.domain.engine import WorkflowRuntimeEngine
from runtime_py_core.domain.context import WorkflowRuntimeContext

# 获取工作流应用实例
app = WorkflowApplication.instance()

# 直接运行工作流
task_id = app.run({
    "schema": workflow_schema,
    "inputs": inputs
})

# 获取任务结果
result = app.result(task_id)

# 获取任务报告
report = app.report(task_id)

# 取消任务
app.cancel(task_id)
```

## 项目结构说明

项目采用领域驱动设计（DDD）架构，主要包含以下目录：

### 核心目录

- `src/api`：API 层实现，提供对外接口
  - `task_run_api.py`：任务运行 API
  - `task_result_api.py`：任务结果 API
  - `task_report_api.py`：任务报告 API
  - `task_cancel_api.py`：任务取消 API

- `src/application`：应用层实现，协调领域对象
  - `workflow_application.py`：工作流应用，管理工作流任务的生命周期

- `src/domain`：领域层实现，包含核心业务逻辑
  - `engine`：工作流引擎，负责执行工作流
  - `context`：工作流上下文，提供工作流执行的环境
  - `task`：工作流任务，表示一个工作流执行实例
  - `document`：工作流文档，解析工作流模式
  - `variable`：变量存储，管理工作流中的变量
  - `state`：状态管理，跟踪工作流执行的状态
  - `io_center`：IO 中心，管理工作流的输入和输出
  - `snapshot`：快照中心，创建和管理工作流执行的快照
  - `status`：状态中心，管理工作流和节点的状态
  - `report`：报告生成，生成工作流执行的报告

- `src/infrastructure`：基础设施层实现，提供底层支持
  - `utils`：工具函数，包括 UUID 生成、延迟函数等

- `src/nodes`：节点实现，包括不同类型的节点执行器
  - `start`：开始节点执行器
  - `end`：结束节点执行器
  - `llm`：LLM 节点执行器
  - `condition`：条件节点执行器
  - `loop`：循环节点执行器

- `src/interface`：接口定义，存放所有类型定义
  - `workflow.py`：工作流相关接口
  - `container.py`：容器和依赖注入相关接口
  - `report.py`：报告相关接口
  - `snapshot.py`：快照相关接口
  - `status.py`：状态相关接口
  - `variable.py`：变量相关接口

### FastAPI 服务器目录

- `app`：FastAPI 服务器实现
  - `main.py`：FastAPI 应用实例和配置
  - `routes.py`：API 路由定义
  - `models.py`：Pydantic 模型定义

- `run.py`：服务器启动脚本，在 localhost:4000 上运行服务器

### 测试目录

- `src/api/__tests__`：API 层测试
- `src/application/__tests__`：应用层测试
- `src/domain/__tests__`：领域层测试
- `src/nodes/__tests__`：节点测试

## 开发指南

### 开发环境设置

1. 克隆仓库

```bash
git clone https://github.com/your-organization/runtime-py-core.git
cd runtime-py-core
```

2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

3. 安装开发依赖项

```bash
pip install -r requirements-dev.txt
```

4. 安装项目

```bash
pip install -e .
```

### 运行测试

```bash
pytest
```

### 代码风格

项目遵循 PEP 8 编码规范，使用 flake8 进行代码风格检查。

```bash
flake8 src
```

### 贡献流程

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 常见问题解答

### 1. 如何解决 TaskReport API 一直返回 "processing" 状态的问题？

这个问题可能是由于工作流状态没有正确更新导致的。确保在异步任务完成时正确更新工作流状态，可以通过以下方法解决：

1. 检查 `WorkflowRuntimeTask` 类中的异步任务处理逻辑
2. 确保在任务完成时调用 `workflow.success()` 或 `workflow.fail()`
3. 在 `TaskReportAPI` 中获取最新的工作流状态

示例修复代码：

```python
# 在 WorkflowRuntimeTask 类中
def _handle_promise_success(self, result):
    # 更新工作流状态
    self.context.status_center.workflow.success()
    return result

def _handle_promise_error(self, error):
    # 更新工作流状态
    self.context.status_center.workflow.fail()
    raise error
```

### 2. 为什么 TaskResult API 总是返回空结果？

这个问题可能是由于结果收集逻辑不完善导致的。可以通过以下方法解决：

1. 确保工作流已经终止（状态为 succeeded、failed 或 cancelled）
2. 优先从 IO 中心获取结果
3. 如果 IO 中心没有结果，尝试从 End 节点快照获取结果
4. 增强结果获取逻辑，添加更严格的空结果检查

示例修复代码：

```python
# 在 TaskResultAPI 中
async def __call__(self, input_data):
    task_id = input_data["taskID"]
    app = WorkflowApplication.instance()
    task = app.get_task(task_id)
    
    if not task:
        return {}
        
    # 检查工作流是否已终止
    if not task.context.status_center.workflow.terminated:
        return {}
        
    # 优先从 IO 中心获取结果
    result = task.context.io_center.outputs
    if result:
        return result
        
    # 尝试从 End 节点快照获取结果
    end_snapshots = [s for s in task.context.snapshot_center.export_all() if s.node_id.startswith("end_")]
    if end_snapshots:
        for snapshot in end_snapshots:
            if snapshot.outputs:
                return snapshot.outputs
                
    # 回退到应用层方法
    return app.result(task_id) or {}
```

### 3. 如何自定义节点类型？

要自定义节点类型，需要以下步骤：

1. 在 `src/nodes` 目录下创建新的节点目录
2. 实现节点执行器，继承 `BaseNodeExecutor` 类
3. 在节点执行器中实现 `execute` 方法
4. 在 `src/domain/executor/workflow_runtime_executor.py` 中注册节点类型

示例代码：

```python
# 1. 创建节点执行器
from src.domain.executor import BaseNodeExecutor

class CustomNodeExecutor(BaseNodeExecutor):
    async def execute(self, node, context):
        # 实现节点执行逻辑
        inputs = await self._get_node_inputs(node, context)
        # 处理输入
        outputs = {"result": "处理结果"}
        # 设置输出
        await self._set_node_outputs(node, outputs, context)
        return outputs

# 2. 注册节点类型
# 在 workflow_runtime_executor.py 中
def _register_node_executors(self):
    self._node_executors = {
        # 其他节点类型
        "custom": CustomNodeExecutor(),
    }
```

### 4. 如何处理工作流执行中的错误？

工作流执行中的错误处理包括以下方面：

1. 节点执行错误：在节点执行器中捕获异常，更新节点状态为 failed
2. 工作流执行错误：在工作流执行器中捕获异常，更新工作流状态为 failed
3. 异步任务错误：在异步任务处理中捕获异常，更新工作流状态为 failed

示例代码：

```python
# 节点执行错误处理
async def execute_node(self, node_id, context):
    try:
        node = context.document.get_node(node_id)
        executor = self._get_node_executor(node.type)
        context.status_center.node_status(node_id).processing()
        result = await executor.execute(node, context)
        context.status_center.node_status(node_id).success()
        return result
    except Exception as e:
        context.status_center.node_status(node_id).fail()
        raise e
```

### 5. 如何优化工作流执行性能？

优化工作流执行性能的方法包括：

1. 使用异步 IO：利用 Python 的 asyncio 库进行异步 IO 操作
2. 并行执行：对于没有依赖关系的节点，可以并行执行
3. 缓存结果：对于重复执行的节点，可以缓存结果
4. 优化节点执行：减少节点执行的时间复杂度
5. 使用更高效的数据结构：选择适合的数据结构存储工作流数据

示例代码：

```python
# 并行执行节点
async def execute_parallel_nodes(self, node_ids, context):
    tasks = [self.execute_node(node_id, context) for node_id in node_ids]
    return await asyncio.gather(*tasks)
```

## 许可证

MIT

## 项目状态

本项目目前处于开发阶段，API 可能会发生变化。

## 联系方式

如有任何问题或建议，请通过 [issues](https://github.com/your-organization/runtime-py-core/issues) 联系我们。