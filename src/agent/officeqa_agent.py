"""Core OfficeQA purple agent implementation."""

import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """Result of a single task evaluation."""

    task_id: str
    answer: str
    confidence: float
    reasoning: str


class OfficeQAAgent:
    """Purple agent for the OfficeQA benchmark."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize the OfficeQA agent.

        Args:
            llm_client: Optional LLMClient instance. If not provided, creates a new one.
        """
        self.llm_client = llm_client or LLMClient()
        self.results: List[TaskResult] = []

    def process_task(
        self,
        task_id: str,
        question: str,
        documents: List[str],
        task_type: str = "qa",
    ) -> TaskResult:
        """
        Process a single OfficeQA task.

        Args:
            task_id: Unique task identifier
            question: The question to answer
            documents: List of relevant document texts
            task_type: Type of task (qa, extraction, calculation, etc.)

        Returns:
            TaskResult containing the answer and metadata
        """
        logger.info(f"Processing task {task_id}: {question[:50]}...")

        try:
            # Combine documents into context
            context = "\n---\n".join(documents)

            # Generate answer based on task type
            if task_type == "extraction":
                answer = self._handle_extraction(question, context)
            elif task_type == "calculation":
                answer = self._handle_calculation(question, context)
            else:  # default qa
                answer = self._handle_qa(question, context)

            # For now, estimate confidence (can be improved with fine-tuning)
            confidence = self._estimate_confidence(answer)

            result = TaskResult(
                task_id=task_id,
                answer=answer,
                confidence=confidence,
                reasoning=f"Processed {len(documents)} document(s) for {task_type} task",
            )

            self.results.append(result)
            logger.info(f"Task {task_id} completed with confidence: {confidence:.2f}")

            return result

        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            return TaskResult(
                task_id=task_id,
                answer="Unable to process",
                confidence=0.0,
                reasoning=f"Error: {str(e)}",
            )

    def _handle_qa(self, question: str, context: str) -> str:
        """Handle general Q&A tasks."""
        if not context.strip():
            prompt = f"""Answer the following OfficeQA question as accurately as possible.

Return only the final answer with no explanation.

Question: {question}

Answer:"""
            return self.llm_client.answer_prompt(prompt)
        return self.llm_client.extract_answer(question, context)

    def _handle_extraction(self, question: str, context: str) -> str:
        """Handle data extraction tasks."""
        prompt = f"""Extract the specific information requested from the following context.

Context:
{context}

Request: {question}

Extracted Information:"""

        return self.llm_client.query(prompt, max_tokens=300)

    def _handle_calculation(self, question: str, context: str) -> str:
        """Handle quantitative calculation tasks."""
        prompt = f"""Based on the data in the following context, perform the necessary calculations to answer the question.

Context:
{context}

Question: {question}

Calculation Result:"""

        return self.llm_client.query(prompt, max_tokens=500)

    def _estimate_confidence(self, answer: str) -> float:
        """
        Estimate confidence in the answer.

        This is a placeholder implementation. In production, this could use
        uncertainty estimation techniques or fine-tuned models.

        Args:
            answer: The generated answer

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Simple heuristic: answers with more detail are likely more confident
        word_count = len(answer.split())
        # Normalize to 0.0-1.0 range
        confidence = min(0.5 + (word_count / 100) * 0.5, 1.0)
        return confidence

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get all task results.

        Returns:
            List of results as dictionaries
        """
        return [asdict(result) for result in self.results]

    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results = []
