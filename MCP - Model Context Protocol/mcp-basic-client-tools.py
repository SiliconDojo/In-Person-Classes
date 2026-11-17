import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python3",
    args=["mcp-basic-server.py"],  # path to your MCP server script
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available tools from the MCP server
            tools_result = await session.list_tools()
            print(tools_result) # Print Raw Tool Response
            print(type(tools_result)) # Print Data Type of Response (Class)

            for tool in tools_result.tools:
                print(f'Name: {tool.name}')
                print(f'Description: {tool.description}')

if __name__ == "__main__":
    asyncio.run(main())