import asyncio
import json
import logging
from typing import Dict, Any

from src.nodes.llm import LLMExecutor
from src.interface.executor import ExecutionContext

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_llm_executor():
    """测试LLM执行器"""
    print("测试LLM执行器...")
    
    # 创建LLM执行器
    executor = LLMExecutor()
    
    # 准备输入数据
    inputs = {
        "modelName": "ep-20250206192339-nnr9m",
        "apiKey": "7fe5b737-1fc1-43b4-a8ae-cf35491e7220",
        "apiHost": "https://ark.cn-beijing.volces.com/api/v3",
        "temperature": 0,
        "systemPrompt": "You are a helpful AI assistant.",
        "prompt": "Just give me the answer of '1+1=?', just one number, no other words"
    }
    
    # 创建执行上下文
    context = ExecutionContext(
        node={"id": "llm_0", "type": "llm"},
        inputs=inputs,
        runtime=None,
        container=None
    )
    
    try:
        # 执行LLM节点
        print("执行LLM节点...")
        result = await executor.execute(context)
        
        # 打印结果
        print(f"执行结果: {result}")
        print(f"输出: {result.outputs}")
        
        return True
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 确保有事件循环可用
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    # 运行测试
    asyncio.run(test_llm_executor())