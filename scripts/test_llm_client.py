import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

async def test_chat_openai():
    """测试ChatOpenAI是否能正确处理API请求"""
    print("测试ChatOpenAI...")
    
    # 使用与curl命令相同的参数
    model_name = "ep-20250206192339-nnr9m"
    api_key = "7fe5b737-1fc1-43b4-a8ae-cf35491e7220"
    api_host = "https://ark.cn-beijing.volces.com/api/v3"
    temperature = 0
    system_prompt = "You are a helpful AI assistant."
    prompt = "Just give me the answer of '1+1=?', just one number, no other words"
    
    try:
        # 创建ChatOpenAI实例
        model = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key,
            openai_api_base=api_host
        )
        
        # 创建消息列表
        messages = []
        messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        # 调用API
        print("发送API请求...")
        api_message = await model.ainvoke(messages)
        
        # 打印响应
        print(f"API响应: {api_message.content}")
        
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
    asyncio.run(test_chat_openai())