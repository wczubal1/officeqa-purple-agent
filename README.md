# Tau2 Purple Agent

A purple agent for the tau2-bench customer service benchmark on AgentBeats.

## Overview

This agent participates in the [tau2-bench](https://github.com/sierra-research/tau2-bench) benchmark, which evaluates customer service agents in dual-control environments. The agent must handle realistic customer service tasks including troubleshooting, billing inquiries, and account management while coordinating with a simulated user.

## Setup

### Prerequisites
- Python 3.11+
- Docker (for containerization)
- OpenAI API key (or other LLM provider)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```bash
# Add your OPENAI_API_KEY or other LLM provider keys
echo "OPENAI_API_KEY=your-key-here" > .env
```

## Running Locally

To run the agent server:

```bash
python -m src.agent.server --host 127.0.0.1 --port 9019 --agent-llm openai/gpt-4.1
```

## Running with AgentBeats

To run assessments using the agentbeats-run command, see the [agentbeats-tutorial](https://github.com/RDI-Foundation/agentbeats-tutorial) for scenario configuration.

## Docker Build

Build the Docker image:

```bash
docker build -t officeqa-purple-agent:latest .
```

Run in Docker:

```bash
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY officeqa-purple-agent:latest
```

## Integration with AgentBeats

### 1. Register on AgentBeats

1. Go to [agentbeats.dev/register-agent](https://agentbeats.dev/register-agent)
2. Select "Purple" agent type
3. Fill in:
   - Agent name
   - Docker image reference (e.g., `ghcr.io/username/officeqa-purple-agent:latest`)
   - Repository URL
4. Copy your **Agent ID** for later use

### 2. Submit Assessments

#### Quick Submit (Recommended)
1. Go to the OfficeQA green agent page on AgentBeats
2. Click "Quick Submit"
3. Select your purple agent from the dropdown
4. Add your OpenAI API key as a secret
5. Configure any parameters (if needed)
6. Submit to create a PR

#### Manual Submit
1. Clone the leaderboard repo: https://github.com/RDI-Foundation/officeqa-agentbeats-leaderboard
2. Edit `scenario.toml` with your agent IDs and configuration
3. Push to trigger the GitHub Actions workflow
4. Merge the PR once results are available

## Project Structure

```
officeqa-purple-agent/
├── src/
│   └── agent/
│       ├── main.py           # Entry point
│       ├── officeqa_agent.py  # Core agent logic
│       └── llm_client.py      # OpenAI client wrapper
├── tests/
│   └── test_agent.py
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
└── .env.example
```

## Resources

- [AgentBeats Tutorial](https://docs.agentbeats.dev/tutorial/)
- [OfficeQA Benchmark](https://agentbeats.dev/agentbeater/officeqa)
- [Agent Template](https://github.com/RDI-Foundation/agent-template)
- [A2A Protocol](https://docs.agentbeats.dev/)

## License

MIT
