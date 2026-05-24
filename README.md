# OfficeQA Purple Agent

A purple agent (competitor) for the OfficeQA benchmark on AgentBeats.

## Overview

This agent evaluates end-to-end grounded reasoning over U.S. Treasury Bulletins. It retrieves relevant documents, extracts values from tables and figures, and performs multi-step quantitative computations to answer questions across 246 human-annotated tasks.

## Setup

### Prerequisites
- Python 3.10+
- Docker (for containerization)
- OpenAI API key

### Installation

1. Clone this repository:
```bash
git clone <repo-url>
cd officeqa-purple-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Running Locally

To test the agent locally:

```bash
python -m src.agent.main
```

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
