import asyncio
import dotenv
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
dotenv.load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("ANTHROPIC_API_KEY not found in environment")
    print("To use the full client, set: export ANTHROPIC_API_KEY=your_key_here")
    print("Running basic MCP tools test...")
    
    async def test_mcp_tools():
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        from langchain_mcp_adapters.tools import load_mcp_tools
        
        server_script_path = str(Path(__file__).parent.parent / "mcp_server" / "weather_mcp_server_stdio.py")
        
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", server_script_path],
        )
        
        print("Testing MCP connection...")
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    print("Connected to MCP server")
                    
                    tools = await load_mcp_tools(session)
                    print(f"Tools loaded: {len(tools)}")
                    
                    for tool in tools:
                        print(f"  - {tool.name}: {tool.description}")
                    
                    print("\nTesting tool directly...")
                    
                    temp_tool = None
                    for tool in tools:
                        if "temperatura" in tool.name.lower() or "temperature" in tool.name.lower():
                            temp_tool = tool
                            break
                    
                    if temp_tool:
                        print(f"Testing {temp_tool.name} with Prague...")
                        result = await temp_tool.ainvoke({"city": "Prague"})
                        print(f"Result: {result}")
                    else:
                        print("Temperature tool not found")
                        
        except Exception as e:
            print(f"Error: {e}")
    
    asyncio.run(test_mcp_tools())

else:
    print("ANTHROPIC_API_KEY found")
    print("Running full LangChain client...")
    
    from clients.weather_client_anthropic import run_examples
    run_examples()