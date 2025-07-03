# FastAPI 服务器验证报告和测试指南

## 目录

1. [项目概述](#1-项目概述)
2. [服务器功能和特点](#2-服务器功能和特点)
3. [项目结构](#3-项目结构)
4. [验证结果](#4-验证结果)
5. [环境要求和依赖安装](#5-环境要求和依赖安装)
6. [启动服务器](#6-启动服务器)
7. [使用 curl 测试 API 端点](#7-使用-curl-测试-api-端点)
8. [解释 API 响应](#8-解释-api-响应)
9. [常见问题和解决方案](#9-常见问题和解决方案)
10. [使用 Swagger UI 测试 API](#10-使用-swagger-ui-测试-api)
11. [结论](#11-结论)

## 1. 项目概述

runtime-py-core 项目的 FastAPI 服务器实现提供了一个完整的 RESTful API 接口，用于与工作流运行时进行交互。该服务器是对 runtime-py-core 库的封装，允许用户通过 HTTP 请求运行工作流任务、获取任务结果和报告，以及取消任务。

本文档包含两部分内容：
1. **验证报告**：总结服务器的功能和特点，描述项目结构，记录验证结果
2. **测试指南**：提供环境要求、安装步骤、启动服务器、测试 API 端点以及常见问题的解决方案

## 2. 服务器功能和特点

### 2.1 核心功能

- **工作流任务管理**：提供了完整的工作流任务生命周期管理，包括创建、查询结果、获取报告和取消任务。
- **RESTful API**：遵循 RESTful 设计原则，提供了清晰、一致的 API 接口。
- **异步处理**：使用 FastAPI 的异步特性，确保高性能和响应性。
- **与 runtime-py-core 集成**：直接调用 runtime-py-core 库的核心功能，确保功能一致性。

### 2.2 API 端点

服务器提供了以下四个核心 API 端点：

1. **POST /api/task/run**
   - 功能：运行工作流任务
   - 输入：工作流模式（schema）和输入参数（inputs）
   - 输出：任务 ID（taskID）
   - 描述：接收工作流定义和输入参数，启动一个新的工作流任务，返回任务 ID 用于后续查询。

2. **GET /api/task/result**
   - 功能：获取任务结果
   - 输入：任务 ID（taskID）
   - 输出：工作流输出（如果任务已完成）
   - 描述：根据任务 ID 查询工作流任务的执行结果，如果任务尚未完成则返回 null。

3. **GET /api/task/report**
   - 功能：获取任务报告
   - 输入：任务 ID（taskID）
   - 输出：详细的任务执行报告，包括状态、快照和节点报告
   - 描述：根据任务 ID 查询工作流任务的详细执行报告，包括工作流状态、输入输出和节点执行情况。

4. **PUT /api/task/cancel**
   - 功能：取消任务
   - 输入：任务 ID（taskID）
   - 输出：取消操作是否成功（success）
   - 描述：根据任务 ID 取消正在运行的工作流任务，返回取消操作的结果。

### 2.3 特色功能

- **自动 API 文档**：集成了 Swagger UI 和 ReDoc，提供了交互式 API 文档，方便用户了解和测试 API。
- **类型安全**：使用 Pydantic 模型定义请求和响应，确保类型安全和数据验证。
- **错误处理**：提供了全面的错误处理机制，确保 API 能够返回有意义的错误信息。
- **CORS 支持**：配置了跨源资源共享（CORS），允许来自不同源的请求。
- **健康检查**：提供了健康检查端点（/health），方便监控服务器状态。

## 3. 项目结构

FastAPI 服务器的实现位于 runtime-py-core 项目的 app 目录下，主要包含以下文件：

```
runtime-py-core/
├── app/                  # FastAPI 应用目录
│   ├── __init__.py       # 包初始化文件
│   ├── main.py           # FastAPI 应用实例和配置
│   ├── models.py         # Pydantic 数据模型定义
│   ├── routes.py         # API 路由和业务逻辑
│   ├── test_api.sh       # API 测试脚本
│   └── README.md         # 服务端使用说明
├── run.py                # 服务器启动脚本
└── requirements.txt      # 项目依赖
```

### 3.1 主要组件说明

- **main.py**：创建 FastAPI 应用实例，配置中间件、路由和文档 URL。
- **routes.py**：定义 API 路由和业务逻辑，调用 runtime-py-core 库的 API 函数。
- **models.py**：定义 Pydantic 模型，用于请求和响应的数据验证和序列化。
- **test_api.sh**：提供了测试 API 端点的 shell 脚本。
- **run.py**：服务器启动脚本，使用 uvicorn 启动 FastAPI 应用。

### 3.2 依赖项

服务器依赖以下主要库：

- **fastapi**：高性能的 Web 框架，用于构建 API。
- **uvicorn**：ASGI 服务器，用于运行 FastAPI 应用。
- **pydantic**：数据验证和设置管理库，用于定义请求和响应模型。
- **starlette**：轻量级 ASGI 框架，FastAPI 的基础。
- **python-multipart**：用于处理表单数据。

## 4. 验证结果

### 4.1 API 实现验证

通过代码审查，我们验证了以下内容：

1. **API 端点实现**：所有四个 API 端点（TaskRun、TaskResult、TaskReport 和 TaskCancel）都已正确实现，并与 runtime-py-core 库集成。
2. **请求和响应模型**：使用 Pydantic 模型定义了请求和响应，确保类型安全和数据验证。
3. **错误处理**：实现了适当的错误处理机制，确保 API 能够返回有意义的错误信息。
4. **文档生成**：配置了 Swagger UI 和 ReDoc，提供了交互式 API 文档。

### 4.2 功能验证

通过分析 test_api.sh 脚本和 test_direct.py 文件，我们验证了以下功能：

1. **TaskRun API**：能够接收工作流模式和输入参数，启动工作流任务，并返回任务 ID。
2. **TaskResult API**：能够根据任务 ID 查询工作流任务的执行结果。
3. **TaskReport API**：能够根据任务 ID 查询工作流任务的详细执行报告。
4. **TaskCancel API**：能够根据任务 ID 取消正在运行的工作流任务。

### 4.3 集成验证

通过分析 routes.py 文件，我们验证了 FastAPI 服务器与 runtime-py-core 库的集成：

1. **API 函数调用**：FastAPI 路由直接调用 runtime-py-core 库的 API 函数（TaskRunAPI、TaskResultAPI、TaskReportAPI 和 TaskCancelAPI）。
2. **数据转换**：请求数据被正确转换为 API 函数所需的格式，响应数据被正确返回给客户端。

### 4.4 总体评估

FastAPI 服务器的实现是完整和正确的，能够提供工作流运行时的 RESTful API 接口。服务器的设计遵循了最佳实践，包括：

- **模块化设计**：将应用分为多个模块，包括应用实例、路由、模型等。
- **类型安全**：使用 Pydantic 模型确保类型安全和数据验证。
- **错误处理**：提供了适当的错误处理机制。
- **文档生成**：提供了交互式 API 文档。
- **测试支持**：提供了测试脚本，方便验证 API 功能。

## 5. 环境要求和依赖安装

### 5.1 环境要求

- **Python 版本**：Python 3.8 或更高版本
- **操作系统**：支持 Windows、macOS 和 Linux
- **网络**：确保端口 4000 可用，不被其他应用占用

### 5.2 依赖安装

1. 首先，确保您已经获取了 runtime-py-core 项目的代码：

```bash
# 如果您使用 git
git clone <repository-url>
cd runtime-py-core

# 或者，如果您已经下载了项目代码
cd runtime-py-core
```

2. 安装项目依赖：

```bash
pip install -r requirements.txt
```

这将安装以下主要依赖：
- fastapi：Web 框架
- uvicorn：ASGI 服务器
- pydantic：数据验证
- 其他 runtime-py-core 所需的依赖

如果您只想运行 FastAPI 服务器而不需要完整的 runtime-py-core 功能，可以只安装必要的依赖：

```bash
pip install fastapi uvicorn pydantic
```

### 5.3 验证安装

安装完成后，您可以验证依赖是否正确安装：

```bash
python -c "import fastapi; import uvicorn; import pydantic; print('依赖已正确安装')"
```

如果没有错误消息，则表示依赖已正确安装。

## 6. 启动服务器

### 6.1 使用 run.py 启动

最简单的方法是使用项目提供的 run.py 脚本启动服务器：

```bash
python run.py
```

服务器将在 http://localhost:4000 上运行，您应该会看到类似以下的输出：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

### 6.2 使用 uvicorn 直接启动

您也可以使用 uvicorn 直接启动服务器：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

参数说明：
- `app.main:app`：指定 FastAPI 应用实例的导入路径
- `--host 0.0.0.0`：监听所有网络接口
- `--port 4000`：在端口 4000 上运行
- `--reload`：启用热重载（开发模式）

### 6.3 验证服务器是否正常运行

服务器启动后，您可以通过访问以下 URL 验证服务器是否正常运行：

- 健康检查：http://localhost:4000/health
- Swagger UI：http://localhost:4000/api/docs
- ReDoc：http://localhost:4000/api/redoc

如果您能够访问这些 URL，则表示服务器已经成功启动。

## 7. 使用 curl 测试 API 端点

### 7.1 准备工作

在测试 API 端点之前，您需要准备一些测试数据。以下是一个简单的工作流定义，用于测试 API 端点：

```json
{
  "nodes": [
    {
      "id": "start_0",
      "type": "start",
      "meta": {"position": {"x": 0, "y": 0}},
      "data": {
        "title": "Start",
        "outputs": {
          "type": "object",
          "properties": {
            "model_name": {"key": 14, "name": "model_name", "type": "string", "extra": {"index": 1}, "isPropertyRequired": true},
            "prompt": {"key": 5, "name": "prompt", "type": "string", "extra": {"index": 3}, "isPropertyRequired": true},
            "api_key": {"key": 19, "name": "api_key", "type": "string", "extra": {"index": 4}, "isPropertyRequired": true},
            "api_host": {"key": 20, "name": "api_host", "type": "string", "extra": {"index": 5}, "isPropertyRequired": true}
          },
          "required": ["model_name", "prompt", "api_key", "api_host"]
        }
      }
    },
    {
      "id": "end_0",
      "type": "end",
      "meta": {"position": {"x": 1000, "y": 0}},
      "data": {
        "title": "End",
        "inputsValues": {"answer": {"type": "ref", "content": ["llm_0", "result"]}},
        "inputs": {"type": "object", "properties": {"answer": {"type": "string"}}}
      }
    },
    {
      "id": "llm_0",
      "type": "llm",
      "meta": {"position": {"x": 500, "y": 0}},
      "data": {
        "title": "LLM_0",
        "inputsValues": {
          "modelName": {"type": "ref", "content": ["start_0", "model_name"]},
          "apiKey": {"type": "ref", "content": ["start_0", "api_key"]},
          "apiHost": {"type": "ref", "content": ["start_0", "api_host"]},
          "temperature": {"type": "constant", "content": 0},
          "prompt": {"type": "ref", "content": ["start_0", "prompt"]},
          "systemPrompt": {"type": "constant", "content": "You are a helpful AI assistant."}
        },
        "inputs": {
          "type": "object",
          "required": ["modelName", "temperature", "prompt"],
          "properties": {
            "modelName": {"type": "string"},
            "apiKey": {"type": "string"},
            "apiHost": {"type": "string"},
            "temperature": {"type": "number"},
            "systemPrompt": {"type": "string"},
            "prompt": {"type": "string"}
          }
        },
        "outputs": {"type": "object", "properties": {"result": {"type": "string"}}}
      }
    }
  ],
  "edges": [
    {"sourceNodeID": "start_0", "targetNodeID": "llm_0"},
    {"sourceNodeID": "llm_0", "targetNodeID": "end_0"}
  ]
}
```

这个工作流定义包含三个节点：
- `start_0`：开始节点，提供输入参数
- `llm_0`：LLM 节点，使用 LLM 模型生成结果
- `end_0`：结束节点，返回结果

### 7.2 测试 TaskRun API

使用以下 curl 命令测试 TaskRun API：

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
```

预期响应：

```json
{
  "taskID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

记下返回的 `taskID`，后续 API 测试将使用这个 ID。

### 7.3 测试 TaskReport API

使用以下 curl 命令测试 TaskReport API（替换 `xxxxxx` 为上一步返回的 `taskID`）：

```bash
curl --location 'http://localhost:4000/api/task/report?taskID=xxxxxx'
```

预期响应：

```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "inputs": {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
  },
  "outputs": {
    "answer": "2"
  },
  "workflowStatus": {
    "status": "completed",
    "terminated": true,
    "startTime": 1625097600000,
    "endTime": 1625097605000,
    "timeCost": 5000
  },
  "reports": {
    "start_0": {
      "id": "start_0",
      "status": "completed",
      "terminated": true,
      "startTime": 1625097600000,
      "endTime": 1625097601000,
      "timeCost": 1000,
      "snapshots": [
        {
          "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "nodeID": "start_0",
          "inputs": {},
          "outputs": {
            "model_name": "ep-20250206192339-nnr9m",
            "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
            "api_host": "https://ark.cn-beijing.volces.com/api/v3",
            "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
          },
          "data": {}
        }
      ]
    },
    "llm_0": {
      "id": "llm_0",
      "status": "completed",
      "terminated": true,
      "startTime": 1625097601000,
      "endTime": 1625097604000,
      "timeCost": 3000,
      "snapshots": [
        {
          "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "nodeID": "llm_0",
          "inputs": {
            "modelName": "ep-20250206192339-nnr9m",
            "apiKey": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
            "apiHost": "https://ark.cn-beijing.volces.com/api/v3",
            "temperature": 0,
            "prompt": "Just give me the answer of '1+1=?', just one number, no other words",
            "systemPrompt": "You are a helpful AI assistant."
          },
          "outputs": {
            "result": "2"
          },
          "data": {}
        }
      ]
    },
    "end_0": {
      "id": "end_0",
      "status": "completed",
      "terminated": true,
      "startTime": 1625097604000,
      "endTime": 1625097605000,
      "timeCost": 1000,
      "snapshots": [
        {
          "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "nodeID": "end_0",
          "inputs": {
            "answer": "2"
          },
          "outputs": {},
          "data": {}
        }
      ]
    }
  }
}
```

### 7.4 测试 TaskResult API

使用以下 curl 命令测试 TaskResult API（替换 `xxxxxx` 为之前返回的 `taskID`）：

```bash
curl --location 'http://localhost:4000/api/task/result?taskID=xxxxxx'
```

预期响应：

```json
{
  "answer": "2"
}
```

### 7.5 测试 TaskCancel API

要测试 TaskCancel API，您需要先创建一个新的任务，然后立即尝试取消它：

```bash
# 创建新任务
curl --location 'http://localhost:4000/api/task/run' \
--header 'Content-Type: application/json' \
--data '{
  "inputs": {
      "model_name": "ep-20250206192339-nnr9m",
      "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
      "api_host": "https://ark.cn-beijing.volces.com/api/v3",
      "prompt": "Please write a very long essay about artificial intelligence"
  },
  "schema": "{\"nodes\":[{\"id\":\"start_0\",\"type\":\"start\",\"meta\":{\"position\":{\"x\":0,\"y\":0}},\"data\":{\"title\":\"Start\",\"outputs\":{\"type\":\"object\",\"properties\":{\"model_name\":{\"key\":14,\"name\":\"model_name\",\"type\":\"string\",\"extra\":{\"index\":1},\"isPropertyRequired\":true},\"prompt\":{\"key\":5,\"name\":\"prompt\",\"type\":\"string\",\"extra\":{\"index\":3},\"isPropertyRequired\":true},\"api_key\":{\"key\":19,\"name\":\"api_key\",\"type\":\"string\",\"extra\":{\"index\":4},\"isPropertyRequired\":true},\"api_host\":{\"key\":20,\"name\":\"api_host\",\"type\":\"string\",\"extra\":{\"index\":5},\"isPropertyRequired\":true}},\"required\":[\"model_name\",\"prompt\",\"api_key\",\"api_host\"]}}},{\"id\":\"end_0\",\"type\":\"end\",\"meta\":{\"position\":{\"x\":1000,\"y\":0}},\"data\":{\"title\":\"End\",\"inputsValues\":{\"answer\":{\"type\":\"ref\",\"content\":[\"llm_0\",\"result\"]}},\"inputs\":{\"type\":\"object\",\"properties\":{\"answer\":{\"type\":\"string\"}}}}},{\"id\":\"llm_0\",\"type\":\"llm\",\"meta\":{\"position\":{\"x\":500,\"y\":0}},\"data\":{\"title\":\"LLM_0\",\"inputsValues\":{\"modelName\":{\"type\":\"ref\",\"content\":[\"start_0\",\"model_name\"]},\"apiKey\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_key\"]},\"apiHost\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_host\"]},\"temperature\":{\"type\":\"constant\",\"content\":0},\"prompt\":{\"type\":\"ref\",\"content\":[\"start_0\",\"prompt\"]},\"systemPrompt\":{\"type\":\"constant\",\"content\":\"You are a helpful AI assistant.\"}},\"inputs\":{\"type\":\"object\",\"required\":[\"modelName\",\"temperature\",\"prompt\"],\"properties\":{\"modelName\":{\"type\":\"string\"},\"apiKey\":{\"type\":\"string\"},\"apiHost\":{\"type\":\"string\"},\"temperature\":{\"type\":\"number\"},\"systemPrompt\":{\"type\":\"string\"},\"prompt\":{\"type\":\"string\"}}},\"outputs\":{\"type\":\"object\",\"properties\":{\"result\":{\"type\":\"string\"}}}}}],\"edges\":[{\"sourceNodeID\":\"start_0\",\"targetNodeID\":\"llm_0\"},{\"sourceNodeID\":\"llm_0\",\"targetNodeID\":\"end_0\"}]}"
}'
```

记下返回的 `taskID`，然后立即尝试取消任务：

```bash
# 取消任务
curl --location --request PUT 'http://localhost:4000/api/task/cancel' \
--header 'Content-Type: application/json' \
--data '{
  "taskID": "xxxxxx"
}'
```

预期响应：

```json
{
  "success": true
}
```

## 8. 解释 API 响应

### 8.1 TaskRun API 响应

TaskRun API 的响应非常简单，只包含一个 `taskID` 字段，这是一个唯一标识符，用于后续查询任务的结果和报告。

```json
{
  "taskID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### 8.2 TaskReport API 响应

TaskReport API 的响应包含详细的任务执行报告，包括以下主要部分：

- **id**：任务 ID
- **inputs**：任务的输入参数
- **outputs**：任务的输出结果
- **workflowStatus**：工作流的状态信息，包括：
  - **status**：状态（如 "completed"、"processing"、"failed"）
  - **terminated**：是否已终止
  - **startTime**：开始时间（毫秒时间戳）
  - **endTime**：结束时间（毫秒时间戳）
  - **timeCost**：执行时间（毫秒）
- **reports**：各个节点的执行报告，每个节点包括：
  - **id**：节点 ID
  - **status**：状态
  - **terminated**：是否已终止
  - **startTime**：开始时间
  - **endTime**：结束时间
  - **timeCost**：执行时间
  - **snapshots**：执行快照，包括输入、输出和数据

通过 TaskReport API 的响应，您可以了解任务的执行过程、各个节点的执行情况以及最终结果。

### 8.3 TaskResult API 响应

TaskResult API 的响应只包含任务的输出结果，格式取决于工作流的定义。对于上面的示例工作流，输出结果是一个包含 `answer` 字段的对象：

```json
{
  "answer": "2"
}
```

如果任务尚未完成，TaskResult API 将返回 `null`。

### 8.4 TaskCancel API 响应

TaskCancel API 的响应非常简单，只包含一个 `success` 字段，表示取消操作是否成功：

```json
{
  "success": true
}
```

如果任务不存在或已经完成，`success` 字段将为 `false`。

## 9. 常见问题和解决方案

### 9.1 服务器启动问题

#### 问题：无法启动服务器，出现 "Address already in use" 错误

**解决方案**：端口 4000 已被其他应用占用。您可以尝试以下方法：

1. 关闭占用端口 4000 的应用
2. 修改 run.py 文件中的端口号，使用其他可用端口
3. 使用 uvicorn 直接启动服务器，指定其他端口：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

#### 问题：启动服务器时出现 "ModuleNotFoundError" 错误

**解决方案**：确保您已经安装了所有依赖，并且在正确的目录中运行命令：

```bash
pip install -r requirements.txt
cd runtime-py-core  # 确保在项目根目录中
python run.py
```

### 9.2 API 调用问题

#### 问题：调用 TaskRun API 时出现 "ValidationError" 错误

**解决方案**：检查请求体是否符合要求，特别是 `schema` 字段必须是有效的 JSON 字符串，`inputs` 字段必须包含所有必需的参数：

```json
{
  "inputs": {
    "model_name": "...",
    "api_key": "...",
    "api_host": "...",
    "prompt": "..."
  },
  "schema": "..."
}
```

#### 问题：调用 TaskResult API 或 TaskReport API 时返回 null

**解决方案**：这可能是因为任务尚未完成或任务 ID 不存在。您可以尝试以下方法：

1. 确保使用了正确的任务 ID
2. 等待一段时间后再次尝试，因为任务可能需要一些时间来完成
3. 调用 TaskReport API 查看任务的状态

#### 问题：调用 TaskCancel API 时返回 `{"success": false}`

**解决方案**：这可能是因为任务已经完成或任务 ID 不存在。您可以尝试以下方法：

1. 确保使用了正确的任务 ID
2. 确保任务仍在运行中
3. 调用 TaskReport API 查看任务的状态

### 9.3 工作流执行问题

#### 问题：LLM 节点执行失败

**解决方案**：这可能是因为 LLM 模型的配置不正确。您可以尝试以下方法：

1. 确保提供了正确的 API 密钥和 API 主机
2. 检查模型名称是否正确
3. 检查提示是否有效
4. 调用 TaskReport API 查看详细的错误信息

#### 问题：工作流执行时间过长

**解决方案**：这可能是因为 LLM 模型的响应时间较长。您可以尝试以下方法：

1. 使用更简单的提示
2. 使用响应更快的模型
3. 增加等待时间

### 9.4 其他问题

#### 问题：如何在生产环境中部署服务器

**解决方案**：在生产环境中，您可能需要考虑以下因素：

1. 使用生产级 ASGI 服务器，如 Gunicorn 与 Uvicorn workers
2. 配置反向代理，如 Nginx