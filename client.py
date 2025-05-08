import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv
from google import generativeai as genai
load_dotenv()

genai.configure(api_key="")  # Use env var in real code

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script should be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.sessions = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.sessions.initialize()

        # List available tools
        response = await self.sessions.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

        available_tools = []
        for tool in tools:
            tool_definition = {
                "function_declarations": [
                    {
                        "name": tool.name,
                        "description": tool.description
                    }
                ]
            }
            available_tools.append(tool_definition)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            tools=available_tools
        )

        self.chat = self.model.start_chat()

    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and available tools"""

        final_text = []
        tool_results = []

        # Send the initial message to the chat - Gemini API is not async
        response = self.chat.send_message(query)

        # Iterate through the parts of the response
        for part in response.parts:
            if part.text:
                final_text.append(part.text)

            elif hasattr(part, "function_call"):
                tool_name = part.function_call.name
                tool_args = part.function_call.args

                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Await the async call to tool
                result = await self.sessions.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                
                # Extract text content from TextContent object
                result_text = result.content.text if hasattr(result.content, 'text') else str(result.content)
                final_text.append(f"Tool Result: {result_text}")

                # Continue the chat with the result of the tool - Gemini API is not async
                followup = self.chat.send_message(result_text)
                for followup_part in followup.parts:
                    if followup_part.text:
                        final_text.append(followup_part.text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
