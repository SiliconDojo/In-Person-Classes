import asyncio

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MODEL = "gemma4:31b"   # must be a model with tool support

SYSTEM = (
    "You are a network assistant that tells users what the connection quality is. "
)

server_params = StdioServerParameters(
    command="python3",
    args=["mcp-ping-server.py"],
)

async def main(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Convert MCP tool definitions to Ollama's (OpenAI-style) format
            mcp_tools = (await session.list_tools()).tools
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": t.input_schema,
                    },
                }
                for t in mcp_tools
            ]

            messages = [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": query},
            ]

            while True:
                response = ollama.chat(model=MODEL, messages=messages, tools=tools)
                msg = response.message
                messages.append(msg)

                if not msg.tool_calls:
                    break  # no more tool requests; msg.content is the final answer

                for call in msg.tool_calls:
                    name = call.function.name
                    args = call.function.arguments  
                    print(f"-> calling {name}({args})")
                    result = await session.call_tool(name, args)
                    text = "\n".join(
                        c.text for c in result.content if c.type == "text"
                    )
                    messages.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": text,
                    })
            print(messages)
            for x in messages:
                print(x)
                print()
            print("\n" + (msg.content or ""))

if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        asyncio.run(main(q))