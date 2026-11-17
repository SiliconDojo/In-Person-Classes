import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python3", 
        args=["mcp-server-resource-hours.py"], # Ensure server.py is in the same folder
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("--- Requesting Business Hours ---")
            
            resource_uri = "hours://business"
            result = await session.read_resource(resource_uri)
            
            content = result.contents[0].text
            print(f"Server responded with:\n\n{content}")

if __name__ == "__main__":
    asyncio.run(main())