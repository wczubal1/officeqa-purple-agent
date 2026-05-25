"""HTTP A2A server entrypoint for the OfficeQA purple agent."""

import argparse
import json
import logging
import os
from typing import Any

import uvicorn
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message
from dotenv import load_dotenv

from .llm_client import LLMClient
from .officeqa_agent import OfficeQAAgent

load_dotenv()

logging.basicConfig(
    level=os.getenv("AGENT_LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


FINAL_ANSWER_OPEN = "<FINAL_ANSWER>"
FINAL_ANSWER_CLOSE = "</FINAL_ANSWER>"


def _preview(text: str, limit: int = 500) -> str:
    """Return a single-line preview for logs."""
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[:limit] + "...[truncated]"


def _wrap_final_answer(text: str) -> str:
    """Wrap outward responses in the format expected by the scorer."""
    answer = text.strip()
    if not answer:
        answer = "Unable to process"
    if answer.startswith(FINAL_ANSWER_OPEN) and answer.endswith(FINAL_ANSWER_CLOSE):
        return answer
    return f"{FINAL_ANSWER_OPEN}{answer}{FINAL_ANSWER_CLOSE}"


class OfficeQAExecutor(AgentExecutor):
    """A2A executor that turns incoming text into OfficeQA responses."""

    def __init__(self) -> None:
        self.agent = OfficeQAAgent(LLMClient())

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_input = context.get_user_input()
        if not user_input.strip():
            raise ValueError("Empty request")

        logger.info("Received request preview: %s", _preview(user_input))
        response_text = _wrap_final_answer(self._handle_message(user_input))
        logger.info("Returning response preview: %s", _preview(response_text))
        await event_queue.enqueue_event(
            new_agent_text_message(
                response_text,
                context_id=context.context_id,
                task_id=context.task_id,
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel is not supported")

    def _handle_message(self, raw_text: str) -> str:
        raw_text = raw_text.strip()
        if not raw_text:
            raise ValueError("Empty request")

        try:
            request = json.loads(raw_text)
        except json.JSONDecodeError:
            return self.agent.process_task(
                task_id="message",
                question=raw_text,
                documents=[],
                task_type="qa",
            ).answer

        if isinstance(request, dict) and "tasks" in request:
            results = self._handle_assessment_request(request).get("results", [])
            if len(results) == 1:
                return str(results[0].get("answer", ""))
            return json.dumps(results)

        return self.agent.process_task(
            task_id=request.get("id", "message") if isinstance(request, dict) else "message",
            question=request.get("question", raw_text) if isinstance(request, dict) else raw_text,
            documents=request.get("documents", []) if isinstance(request, dict) else [],
            task_type=request.get("type", "qa") if isinstance(request, dict) else "qa",
        ).answer

    def _handle_assessment_request(self, request: dict[str, Any]) -> dict[str, Any]:
        tasks = request.get("tasks", [])
        self.agent.clear_results()

        for task in tasks:
            self.agent.process_task(
                task_id=task.get("id", "unknown"),
                question=task.get("question", ""),
                documents=task.get("documents", []),
                task_type=task.get("type", "qa"),
            )

        return {
            "status": "success",
            "participant_id": os.getenv("PARTICIPANT_ID", "officeqa-purple-agent"),
            "results": self.agent.get_results(),
        }


def build_agent_card(card_url: str) -> AgentCard:
    skill = AgentSkill(
        id="officeqa",
        name="OfficeQA",
        description="Answers OfficeQA tasks using document-grounded reasoning.",
        tags=["officeqa", "finance", "qa"],
        examples=[],
    )
    return AgentCard(
        name="OfficeQA Purple Agent",
        description="Purple agent for the OfficeQA benchmark.",
        url=card_url,
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )


def run_example() -> None:
    executor = OfficeQAExecutor()
    example_request = {
        "tasks": [
            {
                "id": "example_1",
                "question": "What is the total amount mentioned in the Treasury bulletin?",
                "documents": [
                    "The U.S. Treasury reported a total of $1.2 trillion in outstanding debt as of Q1 2024."
                ],
                "type": "extraction",
            }
        ]
    }
    print(json.dumps(executor._handle_assessment_request(example_request), indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the OfficeQA A2A server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server")
    parser.add_argument("--port", default=9009, type=int, help="Port to bind the server")
    parser.add_argument("--card-url", help="URL to advertise in the agent card")
    parser.add_argument("--example", action="store_true", help="Run a local example and exit")
    args = parser.parse_args()

    if args.example or os.getenv("RUN_EXAMPLE") == "true":
        run_example()
        return

    card_url = args.card_url or f"http://{args.host}:{args.port}/"
    request_handler = DefaultRequestHandler(
        agent_executor=OfficeQAExecutor(),
        task_store=InMemoryTaskStore(),
    )
    app = A2AStarletteApplication(
        agent_card=build_agent_card(card_url),
        http_handler=request_handler,
    )
    uvicorn.run(app.build(), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
