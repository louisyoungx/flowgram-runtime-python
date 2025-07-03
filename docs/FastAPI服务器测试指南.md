# FastAPI 服务器测试指南

本指南将帮助您在正常环境中测试 runtime-py-core 项目的 FastAPI 服务器。指南包括环境要求、安装步骤、启动服务器、测试 API 端点以及常见问题的解决方案。

## 1. 环境要求和依赖安装

### 1.1 环境要求

- **Python 版本**：Python 3.8 或更高版本
- **操作系统**：支持 Windows、macOS 和 Linux
- **网络**：确保端口 4000 可用，不被其他应用占用

### 1.2 依赖安装

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

### 1.3 验证安装

安装完成后，您可以验证依赖是否正确安装：

```bash
python -c "import fastapi; import uvicorn; import pydantic; print('依赖已正确安装')"
```

如果没有错误消息，则表示依赖已正确安装。

## 2. 启动服务器

### 2.1 使用 run.py 启动

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

### 2.2 使用 uvicorn 直接启动

您也可以使用 uvicorn 直接启动服务器：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

参数说明：
- `app.main:app`：指定 FastAPI 应用实例的导入路径
- `--host 0.0.0.0`：监听所有网络接口
- `--port 4000`：在端口 4000 上运行
- `--reload`：启用热重载（开发模式）

### 2.3 验证服务器是否正常运行

服务器启动后，您可以通过访问以下 URL 验证服务器是否正常运行：

- 健康检查：http://localhost:4000/health
- Swagger UI：http://localhost:4000/api/docs
- ReDoc：http://localhost:4000/api/redoc

如果您能够访问这些 URL，则表示服务器已经成功启动。

## 3. 使用 curl 测试 API 端点

### 3.1 准备工作

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

### 3.2 测试 TaskRun API

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

### 3.3 测试 TaskReport API

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

### 3.4 测试 TaskResult API

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

### 3.5 测试 TaskCancel API

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

## 4. 解释 API 响应

### 4.1 TaskRun API 响应

TaskRun API 的响应非常简单，只包含一个 `taskID` 字段，这是一个唯一标识符，用于后续查询任务的结果和报告。

```json
{
  "taskID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### 4.2 TaskReport API 响应

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

### 4.3 TaskResult API 响应

TaskResult API 的响应只包含任务的输出结果，格式取决于工作流的定义。对于上面的示例工作流，输出结果是一个包含 `answer` 字段的对象：

```json
{
  "answer": "2"
}
```

如果任务尚未完成，TaskResult API 将返回 `null`。

### 4.4 TaskCancel API 响应

TaskCancel API 的响应非常简单，只包含一个 `success` 字段，表示取消操作是否成功：

```json
{
  "success": true
}
```

如果任务不存在或已经完成，`success` 字段将为 `false`。

## 5. 常见问题和解决方案

### 5.1 服务器启动问题

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

### 5.2 API 调用问题

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

### 5.3 工作流执行问题

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

### 5.4 其他问题

#### 问题：如何在生产环境中部署服务器

**解决方案**：在生产环境中，您可能需要考虑以下因素：

1. 使用生产级 ASGI 服务器，如 Gunicorn 与 Uvicorn workers
2. 配置反向代理，如 Nginx
3. 设置适当的安全措施，如 HTTPS、身份验证等
4. 禁用热重载
5. 配置日志记录

示例配置：

```bash
# 安装 gunicorn
pip install gunicorn

# 使用 gunicorn 启动服务器
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:4000
```

#### 问题：如何添加身份验证

**解决方案**：您可以使用 FastAPI 的安全功能添加身份验证，例如：

1. 基本身份验证
2. OAuth2 身份验证
3. API 密钥身份验证

示例代码（API 密钥身份验证）：

```python
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey

API_KEY = "your-api-key"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Invalid API Key")

app = FastAPI()

@app.get("/api/protected", dependencies=[Depends(get_api_key)])
async def protected_route():
    return {"message": "You have access"}
```

## 6. 使用 Swagger UI 测试 API

除了使用 curl 命令，您还可以使用 Swagger UI 交互式地测试 API：

1. 启动服务器后，打开浏览器访问 http://localhost:4000/api/docs
2. 您将看到所有可用的 API 端点
3. 点击要测试的端点，然后点击 "Try it out" 按钮
4. 输入必要的参数，然后点击 "Execute" 按钮
5. 查看响应

Swagger UI 提供了一个用户友好的界面，方便您测试 API 端点，而无需手动构建 curl 命令。

## 7. 总结

本指南介绍了如何在正常环境中测试 runtime-py-core 项目的 FastAPI 服务器。通过按照本指南的步骤，您应该能够成功安装依赖、启动服务器、测试 API 端点并解决常见问题。

如果您遇到本指南未涵盖的问题，请查阅 FastAPI 文档或 runtime-py-core 项目的文档，或者联系项目维护者寻求帮助。