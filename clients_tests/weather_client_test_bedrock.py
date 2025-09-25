import asyncio
import dotenv
import os
import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

sys.path.append(str(Path(__file__).parent.parent))
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

if not validate_aws_credentials():
    print("AWS credentials/region not configured properly")
    print("To use the full Bedrock client, please configure AWS credentials and region")
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
    print("AWS credentials and region configured properly")
    print("Running full LangChain Bedrock client...")
    
    from clients.weather_client_bedrock import run_examples
    run_examples()