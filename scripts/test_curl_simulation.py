"""
测试脚本：模拟curl请求场景，验证TaskReport API响应格式
"""
import asyncio
import json
import logging
import time
from src.api.task_run_api import TaskRunAPI
from src.api.task_report_api import TaskReportAPI

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 测试数据
TEST_SCHEMA = """{
    "nodes":[
        {
            "id":"start_0",
            "type":"start",
            "meta":{"position":{"x":0,"y":0}},
            "data":{
                "title":"Start",
                "outputs":{
                    "type":"object",
                    "properties":{
                        "model_name":{"key":14,"name":"model_name","type":"string","extra":{"index":1},"isPropertyRequired":true},
                        "prompt":{"key":5,"name":"prompt","type":"string","extra":{"index":3},"isPropertyRequired":true},
                        "api_key":{"key":19,"name":"api_key","type":"string","extra":{"index":4},"isPropertyRequired":true},
                        "api_host":{"key":20,"name":"api_host","type":"string","extra":{"index":5},"isPropertyRequired":true}
                    },
                    "required":["model_name","prompt","api_key","api_host"]
                }
            }
        },
        {
            "id":"end_0",
            "type":"end",
            "meta":{"position":{"x":1000,"y":0}},
            "data":{
                "title":"End",
                "inputsValues":{"answer":{"type":"ref","content":["llm_0","result"]}},
                "inputs":{"type":"object","properties":{"answer":{"type":"string"}}}
            }
        },
        {
            "id":"llm_0",
            "type":"llm",
            "meta":{"position":{"x":500,"y":0}},
            "data":{
                "title":"LLM_0",
                "inputsValues":{
                    "modelName":{"type":"ref","content":["start_0","model_name"]},
                    "apiKey":{"type":"ref","content":["start_0","api_key"]},
                    "apiHost":{"type":"ref","content":["start_0","api_host"]},
                    "temperature":{"type":"constant","content":0},
                    "prompt":{"type":"ref","content":["start_0","prompt"]},
                    "systemPrompt":{"type":"constant","content":"You are a helpful AI assistant."}
                },
                "inputs":{
                    "type":"object",
                    "required":["modelName","temperature","prompt"],
                    "properties":{
                        "modelName":{"type":"string"},
                        "apiKey":{"type":"string"},
                        "apiHost":{"type":"string"},
                        "temperature":{"type":"number"},
                        "systemPrompt":{"type":"string"},
                        "prompt":{"type":"string"}
                    }
                },
                "outputs":{"type":"object","properties":{"result":{"type":"string"}}}
            }
        }
    ],
    "edges":[
        {"sourceNodeID":"start_0","targetNodeID":"llm_0"},
        {"sourceNodeID":"llm_0","targetNodeID":"end_0"}
    ]
}"""

TEST_INPUTS = {
    "model_name": "ep-20250206192339-nnr9m",
    "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
    "api_host": "https://ark.cn-beijing.volces.com/api/v3",
    "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
}

EXPECTED_REPORT_STRUCTURE = {
    "id": "<task_id>",  # 将被替换为实际的task_id
    "inputs": {
        "model_name": "ep-20250206192339-nnr9m",
        "api_key": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
        "api_host": "https://ark.cn-beijing.volces.com/api/v3",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    },
    "outputs": {
        "answer": "2"
    },
    "workflowStatus": {
        "status": "succeeded",
        "terminated": True
    },
    "reports": {
        "start_0": {
            "id": "start_0",
            "status": "succeeded",
            "terminated": True,
            "snapshots": []
        },
        "llm_0": {
            "id": "llm_0",
            "status": "succeeded",
            "terminated": True,
            "snapshots": []
        },
        "end_0": {
            "id": "end_0",
            "status": "succeeded",
            "terminated": True,
            "snapshots": []
        }
    }
}

async def test_curl_scenario():
    """模拟curl请求场景，执行TaskRun和TaskReport API调用"""
    logger.info("开始测试curl请求场景")
    
    # 步骤1：执行TaskRunAPI，相当于curl --location 'http://localhost:4000/api/task/run'
    task_run_input = {
        "inputs": TEST_INPUTS,
        "schema": TEST_SCHEMA
    }
    
    task_run_result = await TaskRunAPI(task_run_input)
    task_id = task_run_result["taskID"]
    logger.info(f"TaskRunAPI 执行成功，taskID: {task_id}")
    
    # 步骤2：等待5秒，让工作流有时间执行
    logger.info("等待5秒...")
    await asyncio.sleep(5)
    
    # 步骤3：执行TaskReportAPI，相当于curl --location 'http://localhost:4000/api/task/report?taskID=xxx'
    task_report_input = {
        "taskID": task_id
    }
    
    task_report_result = await TaskReportAPI(task_report_input)
    logger.info(f"TaskReportAPI 响应: {json.dumps(task_report_result, indent=2)}")
    
    # 步骤4：验证报告结构
    logger.info("验证报告结构...")
    
    # 验证基本字段存在
    assert "id" in task_report_result, "报告中缺少id字段"
    assert "inputs" in task_report_result, "报告中缺少inputs字段"
    assert "outputs" in task_report_result, "报告中缺少outputs字段"
    assert "workflowStatus" in task_report_result, "报告中缺少workflowStatus字段"
    assert "reports" in task_report_result, "报告中缺少reports字段"
    
    # 验证id是否为传入的task_id
    assert task_report_result["id"] == task_id, f"报告id不匹配: {task_report_result['id']} != {task_id}"
    
    # 验证inputs是否包含预期的输入
    for key, value in TEST_INPUTS.items():
        assert key in task_report_result["inputs"], f"inputs中缺少{key}字段"
        assert task_report_result["inputs"][key] == value, f"inputs.{key}值不匹配"
    
    # 验证workflowStatus包含status和terminated
    assert "status" in task_report_result["workflowStatus"], "workflowStatus中缺少status字段"
    assert "terminated" in task_report_result["workflowStatus"], "workflowStatus中缺少terminated字段"
    
    # 验证reports包含所有节点
    for node_id in ["start_0", "llm_0", "end_0"]:
        assert node_id in task_report_result["reports"], f"reports中缺少{node_id}节点"
        node_report = task_report_result["reports"][node_id]
        assert "id" in node_report, f"{node_id}报告中缺少id字段"
        assert "status" in node_report, f"{node_id}报告中缺少status字段"
        assert "terminated" in node_report, f"{node_id}报告中缺少terminated字段"
        assert "snapshots" in node_report, f"{node_id}报告中缺少snapshots字段"
    
    # 验证outputs中是否有answer字段，值为"2"
    if "answer" in task_report_result["outputs"] and task_report_result["outputs"]["answer"] == "2":
        logger.info("✅ 测试通过：outputs.answer = 2")
    else:
        logger.warning(f"⚠️ outputs中没有answer=2: {task_report_result['outputs']}")
    
    # 验证workflowStatus.status是否为"succeeded"
    status = task_report_result["workflowStatus"]["status"]
    if status == "succeeded":
        logger.info("✅ 测试通过：workflowStatus.status = succeeded")
    else:
        logger.warning(f"⚠️ workflowStatus.status不是succeeded: {status}")
    
    logger.info("测试完成")
    return task_report_result

if __name__ == "__main__":
    try:
        result = asyncio.run(test_curl_scenario())
        print("\n最终结果:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"测试过程中出错: {e}", exc_info=True)