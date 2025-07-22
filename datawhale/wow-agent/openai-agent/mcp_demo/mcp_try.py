from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings
import os
from dotenv import load_dotenv
import asyncio

from litellm import completion


# 加载环境变量
load_dotenv()
# 从环境变量中读取api_key
api_key = os.getenv('mistral_key')
base_url = 'https://api.mistral.ai/v1'
chat_model = "mistral/mistral-small-latest"

set_tracing_disabled(disabled=True)
llm = LitellmModel(model=chat_model, api_key=api_key, base_url=base_url)


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        model=llm,
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    # 进入时：建立 SSE 连接，进行握手和能力发现
    # 退出时：自动关闭连接，清理资源
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://127.0.0.1:8000/sse",
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    asyncio.run(main())