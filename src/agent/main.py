"""Main entry point for the OfficeQA purple agent."""

import os
import json
import logging
import sys
from typing import Optional
from dotenv import load_dotenv

from .llm_client import LLMClient
from .officeqa_agent import OfficeQAAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("AGENT_LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class AgentServer:
    """Server for the OfficeQA purple agent following A2A protocol."""

    def __init__(self):
        """Initialize the agent server."""
        self.llm_client = LLMClient()
        self.agent = OfficeQAAgent(self.llm_client)
        logger.info("OfficeQA Purple Agent initialized")

    def handle_assessment_request(self, request: dict) -> dict:
        """
        Handle an assessment request from the green agent.

        Args:
            request: Assessment request in A2A format

        Returns:
            Assessment result in A2A format
        """
        logger.info("Received assessment request")

        try:
            # Extract tasks from request
            tasks = request.get("tasks", [])

            results = []
            for task in tasks:
                task_result = self.agent.process_task(
                    task_id=task.get("id", "unknown"),
                    question=task.get("question", ""),
                    documents=task.get("documents", []),
                    task_type=task.get("type", "qa"),
                )
                results.append(task_result)

            response = {
                "status": "success",
                "participant_id": os.getenv("PARTICIPANT_ID", "officeqa-purple-agent"),
                "results": self.agent.get_results(),
            }

            logger.info(f"Assessment complete. Processed {len(results)} tasks.")
            return response

        except Exception as e:
            logger.error(f"Error handling assessment request: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    def run_example(self) -> None:
        """Run an example assessment for testing."""
        logger.info("Running example assessment...")

        example_request = {
            "tasks": [
                {
                    "id": "example_1",
                    "question": "What is the total amount mentioned in the Treasury bulletin?",
                    "documents": [
                        "The U.S. Treasury reported a total of $1.2 trillion in outstanding debt as of Q1 2024."
                    ],
                    "type": "extraction",
                },
                {
                    "id": "example_2",
                    "question": "Calculate the average of the following values: 100, 200, 300",
                    "documents": ["Values: 100, 200, 300"],
                    "type": "calculation",
                },
            ]
        }

        response = self.handle_assessment_request(example_request)
        print("\nExample Input Questions:")
        for task in example_request["tasks"]:
            print(f"  Task {task['id']}: {task['question']}")
        print("\nExample Assessment Response:")
        print(json.dumps(response, indent=2))


def main():
    """Main entry point."""
    logger.info("Starting OfficeQA Purple Agent")

    server = AgentServer()

    # Check if running in example mode
    if "--example" in sys.argv or os.getenv("RUN_EXAMPLE") == "true":
        server.run_example()
    else:
        # A2A protocol mode: read from stdin, write to stdout
        logger.info("Agent ready to receive assessment requests")
        logger.info("Run with --example flag to test")
        
        # Listen for A2A protocol requests on stdin
        try:
            for line in sys.stdin:
                if line.strip():
                    try:
                        request = json.loads(line)
                        response = server.handle_assessment_request(request)
                        print(json.dumps(response))
                        sys.stdout.flush()
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON: {e}")
                        error_response = {
                            "status": "error",
                            "error": f"Invalid JSON input: {e}"
                        }
                        print(json.dumps(error_response))
                        sys.stdout.flush()
        except KeyboardInterrupt:
            logger.info("Agent shutdown requested")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
