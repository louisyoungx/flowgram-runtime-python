# Runtime-py-core FastAPI 服务器

这是 runtime-py-core 的 FastAPI 服务器实现，提供了工作流运行时的 RESTful API 接口。

## 功能特点

- 基于 FastAPI 框架，提供高性能的异步 API
- 支持 Swagger 文档，方便 API 测试和浏览
- 与 runtime-py-core 库无缝集成
- 提供工作流任务的运行、结果查询、报告生成和取消功能

## API 端点

服务器提供以下 API 端点：

1. **POST /api/task/run** - 运行工作流任务
2. **GET /api/task/result** - 获取任务结果
3. **GET /api/task/report** - 获取任务报告
4. **PUT /api/task/cancel** - 取消任务

## 安装和使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务器

```bash
python run.py
```

服务器将在 http://localhost:4000 上运行，Swagger 文档可在 http://localhost:4000/api/docs 访问。

### 测试 API

可以使用提供的测试脚本测试 API 端点：

```bash
chmod +x app/test_api.sh
./app/test_api.sh
```

或者使用 curl 命令手动测试：

```bash
# 运行任务
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

## Swagger 文档

服务器启动后，可以通过以下 URL 访问 Swagger 文档：

- Swagger UI: http://localhost:4000/api/docs
- ReDoc: http://localhost:4000/api/redoc
- OpenAPI 规范: http://localhost:4000/api/openapi.json

通过 Swagger UI，您可以直接在浏览器中测试所有 API 端点。