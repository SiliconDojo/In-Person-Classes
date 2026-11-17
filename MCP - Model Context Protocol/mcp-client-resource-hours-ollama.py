import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python3", 
        args=["mcp-server-resource-hours.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            user_query = input("Ask a question about the business: ")

            resource_uri = "hours://business"
            resource_result = await session.read_resource(resource_uri)
            business_hours_context = resource_result.contents[0].text

            prompt = f"""
            You are a helpful business assistant. Use the following context to answer the user question.
            If the answer isn't in the context, say you don't know.

            CONTEXT:
            {business_hours_context}

            USER QUESTION: 
            {user_query}
            """
            response = ollama.chat(model='granite4.1:3b', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])

            print(response['message']['content'])

if __name__ == "__main__":
    asyncio.run(main())
