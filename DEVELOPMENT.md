# Development Guide for OfficeQA Purple Agent

## Quick Start

1. **Set up environment:**
   ```bash
   make install
   source venv/bin/activate
   ```

2. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env with your OPENAI_API_KEY
   ```

3. **Test the agent:**
   ```bash
   make example
   ```

## Architecture

### Core Components

- **LLMClient** (`src/agent/llm_client.py`): Handles all OpenAI API interactions
- **OfficeQAAgent** (`src/agent/officeqa_agent.py`): Core agent logic for processing OfficeQA tasks
- **AgentServer** (`src/agent/main.py`): Assessment request handler following A2A protocol

### Task Types

The agent handles multiple task types:

- **QA (Question Answering)**: General comprehension questions
- **Extraction**: Pulling specific values from documents
- **Calculation**: Multi-step quantitative reasoning

## Development Workflow

### 1. Add New Features

Edit the agent logic in `src/agent/officeqa_agent.py`:

```python
def _handle_custom_task(self, question: str, context: str) -> str:
    """Handle custom task type."""
    # Add your logic here
    pass
```

### 2. Test Locally

```bash
make test           # Run pytest
make example        # Run example assessment
make lint          # Check code quality
make format        # Auto-format code
```

### 3. Build Docker Image

```bash
make docker-build
make docker-run
```

## Integration with AgentBeats

### Register Purple Agent

1. Go to [agentbeats.dev/register-agent](https://agentbeats.dev/register-agent)
2. Select "Purple" agent type
3. Fill in:
   - Agent name: e.g., "your-username/officeqa-purple-agent"
   - Docker image: Your published image reference
   - Repository: Link to your GitHub repo
4. Copy the **Agent ID** provided

### Submit Assessment

#### Option 1: Quick Submit (Recommended)
1. Visit OfficeQA page: https://agentbeats.dev/agentbeater/officeqa
2. Click "Quick Submit"
3. Select your purple agent
4. Provide OpenAI API key
5. Submit to create a PR

#### Option 2: Manual Submit
1. Clone leaderboard repo
2. Edit `scenario.toml` with agent IDs
3. Push to trigger GitHub Actions
4. Results appear on leaderboard after merge

## Environment Variables

Key variables in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (default: gpt-4)
- `AGENT_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Troubleshooting

### API Key Issues
```bash
# Verify your API key is set
echo $OPENAI_API_KEY

# Or check .env file
cat .env
```

### Test Failures
```bash
# Run with verbose output
pytest tests/ -v -s

# Check logs
tail -f agent.log
```

### Docker Issues
```bash
# Build with no cache
docker build --no-cache -t officeqa-purple-agent:latest .

# Check container logs
docker logs officeqa-purple-agent
```

## Next Steps

1. **Improve Task Handling**: Enhance the `_handle_*` methods with better prompts
2. **Add Tool Use**: Integrate document retrieval tools
3. **Improve Confidence**: Implement uncertainty estimation
4. **Add Caching**: Reduce API calls with response caching
5. **Performance**: Optimize for faster inference

## Resources

- [AgentBeats Tutorial](https://docs.agentbeats.dev/tutorial/)
- [OfficeQA Benchmark](https://agentbeats.dev/agentbeater/officeqa)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Agent Template](https://github.com/RDI-Foundation/agent-template)
