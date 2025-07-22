import random
from mcp.server.fastmcp import FastMCP
# Create server
mcp = FastMCP("Secret Word")

@mcp.tool()
def get_secret_word() -> str:
    print("使用工具 get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])

if __name__ == "__main__":
    mcp.run(transport="sse")