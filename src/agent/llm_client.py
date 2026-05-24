"""LLM client wrapper for OpenAI API."""

import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMClient:
    """Wrapper around OpenAI API for language model interactions."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
    ):
        """
        Initialize the LLM client.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            model: Model name to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable or api_key parameter required")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def query(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Send a query to the language model.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)

        Returns:
            The model's response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI assistant specialized in document analysis and quantitative reasoning.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise

    def extract_answer(self, question: str, context: str) -> str:
        """
        Extract an answer from context based on a question.

        Args:
            question: The question to answer
            context: The relevant context/document content

        Returns:
            The extracted answer
        """
        prompt = f"""Based on the following context, answer the question accurately and concisely.

Context:
{context}

Question: {question}

Answer:"""

        return self.query(prompt, max_tokens=500)

    def perform_calculation(self, instruction: str, data: str) -> str:
        """
        Perform calculations based on provided data.

        Args:
            instruction: The calculation instruction
            data: The data to use for calculation

        Returns:
            The calculation result
        """
        prompt = f"""Perform the following calculation based on the provided data.

Data:
{data}

Instruction: {instruction}

Result:"""

        return self.query(prompt, max_tokens=300)
