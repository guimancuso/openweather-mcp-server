# OpenWeather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the OpenWeather API. This project includes both HTTP and stdio transport implementations, along with LangChain client integrations for Anthropic Claude and Amazon Bedrock.

## Features

- Current weather temperature and conditions
- 5-day weather forecast with 3-hour intervals
- Support for multiple languages (Portuguese, English, Spanish, Italian)
- HTTP and stdio transport modes
- LangChain integration with Anthropic Claude
- LangChain integration with Amazon Bedrock
- Comprehensive error handling and validation

## Prerequisites

- Python 3.11 or higher
- UV package manager
- OpenWeather API key
- Anthropic API key (for Anthropic client)
- AWS credentials (for Bedrock client)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/guimancuso/openweather-mcp-server.git
cd openweather-mcp-server
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your API keys:
```bash
# Required for all clients
OPENWEATHER_KEY=your_openweather_api_key_here

# Required for Anthropic client
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Required for Bedrock client
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
```

## API Key Setup

### OpenWeather API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add the key to your `.env` file

### Anthropic API (Optional)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file

### AWS Bedrock (Optional)
1. Set up AWS credentials using one of these methods:
   - AWS CLI: `aws configure`
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - IAM role (if running on EC2)
   - AWS credentials file (`~/.aws/credentials`)
2. Set the AWS region in your `.env` file

## Usage

### MCP Server (HTTP Mode)
```bash
uv run python mcp_server/weather_mcp_server_http.py
```
The server will start on `http://0.0.0.0:8000`

### MCP Server (stdio Mode)
```bash
uv run python mcp_server/weather_mcp_server_stdio.py
```

### Anthropic Client
```bash
# Interactive mode
uv run python clients/weather_client_anthropic.py

# Run examples
uv run python clients/weather_client_anthropic.py --examples
```

### Bedrock Client
```bash
# Interactive mode
uv run python clients/weather_client_bedrock.py

# Run examples
uv run python clients/weather_client_bedrock.py --examples
```

### Testing
```bash
# Test Anthropic client
uv run python clients_tests/weather_client_test_anthropic.py

# Test Bedrock client
uv run python clients_tests/weather_client_test_bedrock.py
```

## Available Tools

### get_current_temperature(city: str)
Get current weather temperature and conditions for a specific city.

**Parameters:**
- `city`: City name (e.g., "London", "New York", "São Paulo")

**Returns:** JSON object with current weather data

### get_weather_forecast(city: str)
Get 5-day weather forecast with 3-hour intervals for a specific city.

**Parameters:**
- `city`: City name (e.g., "London", "New York", "São Paulo")

**Returns:** JSON object with forecast data

## Example Queries

The system supports queries in multiple languages:

- "What is the current temperature in Prague?"
- "Give me the weather forecast for London in the coming days"
- "¿Cuál es la temperatura actual en Madrid?"
- "¿Cómo estará el clima en Barcelona mañana?"
- "Qual è la temperatura corrente a Roma?"
- "Che tempo farà a Milano nei prossimi giorni?"
- "Qual é a temperatura atual em São Paulo?"
- "Como estará o tempo no Rio de Janeiro amanhã?"

## Project Structure

```
openweather-mcp-server/
├── clients/                          # LangChain client implementations
│   ├── weather_client_anthropic.py  # Anthropic Claude client
│   └── weather_client_bedrock.py    # Amazon Bedrock client
├── clients_tests/                    # Test files for clients
│   ├── weather_client_test_anthropic.py
│   └── weather_client_test_bedrock.py
├── mcp_server/                       # MCP server implementations
│   ├── weather_mcp_server_http.py   # HTTP transport server
│   └── weather_mcp_server_stdio.py  # stdio transport server
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── pyproject.toml                   # Project dependencies
├── README.md                        # This file
└── uv.lock                          # Dependency lock file
```

## Dependencies

- `fastmcp`: MCP server framework
- `requests`: HTTP client for API calls
- `dotenv`: Environment variable management
- `langchain-anthropic`: Anthropic Claude integration
- `langchain-aws`: AWS Bedrock integration
- `langchain-mcp-adapters`: MCP tool adapters
- `langgraph`: Agent framework

## Error Handling

The application includes comprehensive error handling for:
- Missing API keys
- Invalid AWS credentials
- Network connectivity issues
- Invalid city names
- API rate limiting

## Security

- All API keys are loaded from environment variables
- No hardcoded secrets in the codebase
- Proper error handling that doesn't leak sensitive information
- Input validation through the OpenWeather API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the error messages in the console
2. Verify your API keys are correctly set
3. Ensure all dependencies are installed
4. Check the OpenWeather API documentation for city name formats