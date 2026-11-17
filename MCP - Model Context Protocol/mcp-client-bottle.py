import asyncio
import ollama
import subprocess
from mcp import ClientSession, StdioServerParameters
#from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

# must support tool calling - gemma4:31b - granite4.1:3b
OLLAMA_MODEL = "gemma4:31b"
MCP_SERVER = "http://localhost:8080/mcp"
#MCP_SERVER = "mcp-ping-server.py"
# mcp-basic-server-full.py
# mcp-system-health-server.py
# mcp-ping-server.py

server_params = StdioServerParameters(
    command="python3",
    args=[MCP_SERVER],  # path to your MCP server script
)

def mcp_tools_to_ollama_format(mcp_tools):
    tools = []
    for t in mcp_tools:
        tools.append({
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.input_schema or {"type": "object", "properties": {}},
            },
        })
    return tools

async def query_ai(query):
    async with streamable_http_client(MCP_SERVER) as (read, write):
    # async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available tools from the MCP server
            tools_result = await session.list_tools()
            ollama_tools = mcp_tools_to_ollama_format(tools_result.tools)

            ### ADD RESOURCE CODE HERE

            messages = [
                {
                    "role": "system", 
                    "content":  "You are a helpful assistant with access to local system tools and automation. "
                                "Use the provided tools to answer the user's request whenever necessary. "
                                "Be brief"
                },
                {"role": "user", "content": query}
            ]
            for _ in range(10):

                response = ollama.chat(
                    model=OLLAMA_MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )

                msg = response["message"]
                messages.append(msg)

                # If the model wants to call tools, execute them via MCP
                if msg.get("tool_calls"):
                    for call in msg["tool_calls"]:
                        name = call["function"]["name"]
                        args = call["function"]["arguments"]

                        result = await session.call_tool(name, arguments=args)
                        tool_output = "".join(
                            c.text for c in result.content if hasattr(c, "text")
                        )

                        messages.append({
                            "role": "tool",
                            "content": tool_output,
                            "name": name,
                        })

                    # Send tool results back to the model for a final answer
                    final = ollama.chat(model=OLLAMA_MODEL, messages=messages)
                    result = final["message"]["content"]
                    print('--- TOOLS')
                    print(ollama_tools)
                    print('--- TOOL CALL')
                    print(response)
                    print('--- TOOL RESPOSE')
                    print(tool_output)
                    print('--- LLM RESPONSE')
                    print(final)

                else:
                    result = msg["content"]
    return result

while True:
    query = input('Query About System: ')
    subprocess.run(['clear']) # Clear screen
    response = asyncio.run(query_ai(query))
    print(query)
    print(response)