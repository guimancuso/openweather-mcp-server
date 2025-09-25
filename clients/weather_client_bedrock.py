import asyncio
import os
import sys
from pathlib import Path
import dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_aws import ChatBedrock
import boto3
from botocore.exceptions import ClientError

dotenv.load_dotenv()

def validate_aws_credentials():
    try:
        region = os.getenv('AWS_DEFAULT_REGION') or os.getenv('AWS_REGION')
        if not region:
            print("Error: AWS region not configured.")
            print("Please set AWS_DEFAULT_REGION or AWS_REGION environment variable.")
            print("Example: export AWS_DEFAULT_REGION=us-east-1")
            return False
        
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if not credentials:
            print("Error: AWS credentials not found.")
            print("Please configure your AWS credentials using one of these methods:")
            print("1. AWS CLI: aws configure")
            print("2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            print("3. IAM role (if running on EC2)")
            print("4. AWS credentials file (~/.aws/credentials)")
            return False
        
        try:
            sts_client = session.client('sts')
            sts_client.get_caller_identity()
            print(f"AWS credentials validated for region: {region}")
            return True
        except ClientError as e:
            print(f"Error: Invalid AWS credentials: {e}")
            return False
            
    except Exception as e:
        print(f"Error validating AWS credentials: {e}")
        return False

async def create_bedrock_llm():
    try:
        llm = ChatBedrock(
            model_id="amazon.nova-pro-v1:0",
            model_kwargs={"temperature": 0}
        )
        return llm
    except Exception as e:
        print(f"Error creating Bedrock LLM: {e}")
        raise

async def main():
    if not validate_aws_credentials():
        print("\nAWS configuration validation failed. Please fix the issues above and try again.")
        sys.exit(1)
    
    server_script_path = str(Path(__file__).parent.parent / "mcp_server" / "weather_mcp_server_stdio.py")
    
    if not Path(server_script_path).exists():
        print(f"Error: Weather MCP server script not found at {server_script_path}")
        sys.exit(1)
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", server_script_path],
    )
    
    print("Starting LangChain client with Amazon Bedrock for OpenWeather MCP...")
    print("=" * 60)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                try:
                    await session.initialize()
                    print("Connected to OpenWeather MCP server")
                    
                    try:
                        tools = await load_mcp_tools(session)
                        print(f"Loaded {len(tools)} tools:")
                        for tool in tools:
                            print(f"  - {tool.name}: {tool.description}")
                    except Exception as e:
                        print(f"Error loading MCP tools: {e}")
                        return
                    
                    try:
                        llm = await create_bedrock_llm()
                        print("Bedrock LLM created successfully")
                    except Exception as e:
                        print(f"Failed to create Bedrock LLM: {e}")
                        return
                    
                    try:
                        agent = create_react_agent(llm, tools)
                        print("LangChain agent created successfully")
                    except Exception as e:
                        print(f"Error creating agent: {e}")
                        return
                    
                    print("\nLangChain agent with Amazon Bedrock created successfully!")
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
                            
                            try:
                                response = await agent.ainvoke({
                                    "messages": [{"role": "user", "content": user_input}]
                                })
                                
                                last_message = response["messages"][-1]
                                print(f"\nResponse: {last_message.content}")
                            except Exception as e:
                                print(f"\nError processing query: {e}")
                                print("Please try again with a different question.")
                            
                        except KeyboardInterrupt:
                            print("\nShutting down client...")
                            break
                        except EOFError:
                            print("\nShutting down client...")
                            break
                        except Exception as e:
                            print(f"\nUnexpected error: {e}")
                            
                except Exception as e:
                    print(f"Error initializing MCP session: {e}")
                    return
                    
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        print("Please make sure:")
        print("1. The weather_mcp_server_stdio.py script exists")
        print("2. All required dependencies are installed")
        print("3. The OpenWeather API key is configured")
        return


def run_examples():
    
    async def run_example_queries():
        if not validate_aws_credentials():
            print("\nAWS configuration validation failed. Please fix the issues above and try again.")
            return
            
        server_script_path = str(Path(__file__).parent.parent / "mcp_server" / "weather_mcp_server_stdio.py")
        
        if not Path(server_script_path).exists():
            print(f"Error: Weather MCP server script not found at {server_script_path}")
            return
        
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", server_script_path],
        )
        
        print("Running examples with LangChain Bedrock client...")
        print("=" * 60)
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    try:
                        await session.initialize()
                        print("Connected to OpenWeather MCP server")
                        
                        try:
                            tools = await load_mcp_tools(session)
                            print(f"Loaded {len(tools)} tools")
                        except Exception as e:
                            print(f"Error loading MCP tools: {e}")
                            return
                        
                        try:
                            llm = await create_bedrock_llm()
                            print("Bedrock LLM created successfully")
                        except Exception as e:
                            print(f"Failed to create Bedrock LLM: {e}")
                            return
                            
                        try:
                            agent = create_react_agent(llm, tools)
                            print("LangChain agent created successfully")
                        except Exception as e:
                            print(f"Error creating agent: {e}")
                            return
                        
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
                        
                        print(f"\nRunning {len(examples)} example queries...")
                        print("-" * 60)
                        
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
                                print(f"Error processing example {i}: {e}")
                            
                            print()
                            
                    except Exception as e:
                        print(f"Error initializing MCP session: {e}")
                        return
                        
        except Exception as e:
            print(f"Error connecting to MCP server: {e}")
            return
    
    asyncio.run(run_example_queries())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        run_examples()
    else:
        asyncio.run(main())