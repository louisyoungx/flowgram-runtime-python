#!/bin/bash

# 设置API基础URL
BASE_URL="http://localhost:4000/api"

# 运行任务并获取taskID
echo "1. 测试 TaskRun API..."
TASK_RUN_RESPONSE=$(curl -s --location "$BASE_URL/task/run" \
--header 'Content-Type: application/json' \
--data '{
  "inputs": {
      "model_name": "ep-20250206192339-nnr9m",
      "api_key": "c5720be8-e02d-4584-8cd7-27bcbcc14dab",
      "api_host": "https://ark.cn-beijing.volces.com/api/v3",
      "prompt": "Just give me the answer of '\''1+1=?'\'', just one number, no other words"
  },
  "schema": "{\"nodes\":[{\"id\":\"start_0\",\"type\":\"start\",\"meta\":{\"position\":{\"x\":0,\"y\":0}},\"data\":{\"title\":\"Start\",\"outputs\":{\"type\":\"object\",\"properties\":{\"model_name\":{\"key\":14,\"name\":\"model_name\",\"type\":\"string\",\"extra\":{\"index\":1},\"isPropertyRequired\":true},\"prompt\":{\"key\":5,\"name\":\"prompt\",\"type\":\"string\",\"extra\":{\"index\":3},\"isPropertyRequired\":true},\"api_key\":{\"key\":19,\"name\":\"api_key\",\"type\":\"string\",\"extra\":{\"index\":4},\"isPropertyRequired\":true},\"api_host\":{\"key\":20,\"name\":\"api_host\",\"type\":\"string\",\"extra\":{\"index\":5},\"isPropertyRequired\":true}},\"required\":[\"model_name\",\"prompt\",\"api_key\",\"api_host\"]}}},{\"id\":\"end_0\",\"type\":\"end\",\"meta\":{\"position\":{\"x\":1000,\"y\":0}},\"data\":{\"title\":\"End\",\"inputsValues\":{\"answer\":{\"type\":\"ref\",\"content\":[\"llm_0\",\"result\"]}},\"inputs\":{\"type\":\"object\",\"properties\":{\"answer\":{\"type\":\"string\"}}}}},{\"id\":\"llm_0\",\"type\":\"llm\",\"meta\":{\"position\":{\"x\":500,\"y\":0}},\"data\":{\"title\":\"LLM_0\",\"inputsValues\":{\"modelName\":{\"type\":\"ref\",\"content\":[\"start_0\",\"model_name\"]},\"apiKey\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_key\"]},\"apiHost\":{\"type\":\"ref\",\"content\":[\"start_0\",\"api_host\"]},\"temperature\":{\"type\":\"constant\",\"content\":0},\"prompt\":{\"type\":\"ref\",\"content\":[\"start_0\",\"prompt\"]},\"systemPrompt\":{\"type\":\"constant\",\"content\":\"You are a helpful AI assistant.\"}},\"inputs\":{\"type\":\"object\",\"required\":[\"modelName\",\"temperature\",\"prompt\"],\"properties\":{\"modelName\":{\"type\":\"string\"},\"apiKey\":{\"type\":\"string\"},\"apiHost\":{\"type\":\"string\"},\"temperature\":{\"type\":\"number\"},\"systemPrompt\":{\"type\":\"string\"},\"prompt\":{\"type\":\"string\"}}},\"outputs\":{\"type\":\"object\",\"properties\":{\"result\":{\"type\":\"string\"}}}}}],\"edges\":[{\"sourceNodeID\":\"start_0\",\"targetNodeID\":\"llm_0\"},{\"sourceNodeID\":\"llm_0\",\"targetNodeID\":\"end_0\"}]}"
}')

echo "TaskRun 响应:"
echo "$TASK_RUN_RESPONSE" | python -m json.tool

# 提取taskID
TASK_ID=$(echo "$TASK_RUN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['taskID'])")
echo "获取到的taskID: $TASK_ID"

# 立即测试TaskReport API
echo -e "\n2. 立即测试 TaskReport API..."
TASK_REPORT_RESPONSE=$(curl -s --location "$BASE_URL/task/report?taskID=$TASK_ID")
echo "TaskReport 响应:"
echo "$TASK_REPORT_RESPONSE" | python -m json.tool

# 等待3秒后再次测试TaskReport API
echo -e "\n3. 等待3秒后再次测试 TaskReport API..."
sleep 3
TASK_REPORT_RESPONSE=$(curl -s --location "$BASE_URL/task/report?taskID=$TASK_ID")
echo "3秒后 TaskReport 响应:"
echo "$TASK_REPORT_RESPONSE" | python -m json.tool

# 测试TaskResult API
echo -e "\n4. 测试 TaskResult API..."
TASK_RESULT_RESPONSE=$(curl -s --location "$BASE_URL/task/result?taskID=$TASK_ID")
echo "TaskResult 响应:"
echo "$TASK_RESULT_RESPONSE" | python -m json.tool

# 测试TaskCancel API
echo -e "\n5. 测试 TaskCancel API..."
TASK_CANCEL_RESPONSE=$(curl -s --location --request PUT "$BASE_URL/task/cancel" \
--header 'Content-Type: application/json' \
--data "{\"taskID\": \"$TASK_ID\"}")
echo "TaskCancel 响应:"
echo "$TASK_CANCEL_RESPONSE" | python -m json.tool