import asyncio
from pathlib import Path
import dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

dotenv.load_dotenv()

async def main():
    server_script_path = str(Path(__file__).parent.parent / "mcp_server" / "weather_mcp_server_stdio.py")
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", server_script_path],
    )
    
    print("Starting LangChain client for OpenWeather MCP...")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to OpenWeather MCP server")
            
            tools = await load_mcp_tools(session)
            print(f"Loaded {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
            agent = create_react_agent(llm, tools)
            
            print("\nLangChain agent created successfully!")
            print("Enter your weather questions (or 'exit' to quit):")
            print("-" * 60)
            
            while True:
                try:
                    user_input = input("\nQuestion: ").strip()
                    
                    if user_input.lower() in ['sair', 'exit', 'quit']:
                        print("Shutting down client...")
                        break
                    
                    if not user_input:
                        continue
                    
                    print("Processing...")
                    
                    response = await agent.ainvoke({
                        "messages": [{"role": "user", "content": user_input}]
                    })
                    
                    last_message = response["messages"][-1]
                    print(f"\nResponse: {last_message.content}")
                    
                except KeyboardInterrupt:
                    print("\nShutting down client...")
                    break
                except Exception as e:
                    print(f"\nError: {e}")


def run_examples():
    
    async def run_example_queries():
        server_script_path = str(Path(__file__).parent.parent / "mcp_server" / "weather_mcp_server_stdio.py")
        
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", server_script_path],
        )
        
        print("Running examples with LangChain client...")
        print("=" * 60)
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                
                llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
                agent = create_react_agent(llm, tools)
                
                examples = [
                    "What is the current temperature in Prague?",
                    "Give me the weather forecast for London in the coming days",
                    "¿Cuál es la temperatura actual en Madrid?",
                    "¿Cómo estará el clima en Barcelona mañana?",
                    "Qual è la temperatura corrente a Roma?",
                    "Che tempo farà a Milano nei prossimi giorni?",
                    "Qual é a temperatura atual em São Paulo?",
                    "Como estará o tempo no Rio de Janeiro amanhã?"
                ]
                
                for i, question in enumerate(examples, 1):
                    print(f"\nExample {i}: {question}")
                    print("-" * 40)
                    
                    try:
                        response = await agent.ainvoke({
                            "messages": [{"role": "user", "content": question}]
                        })
                        
                        last_message = response["messages"][-1]
                        print(f"Response: {last_message.content}")
                        
                    except Exception as e:
                        print(f"Error: {e}")
                    
                    print()
    
    asyncio.run(run_example_queries())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        run_examples()
    else:
        asyncio.run(main())