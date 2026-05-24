"""Tests for the OfficeQA agent."""

import pytest
from src.agent.llm_client import LLMClient
from src.agent.officeqa_agent import OfficeQAAgent


class TestLLMClient:
    """Test LLM client functionality."""

    def test_client_initialization(self):
        """Test that LLM client can be initialized."""
        # This will raise an error if API key is not set
        try:
            client = LLMClient()
            assert client.model == "gpt-4"
        except ValueError as e:
            pytest.skip(f"Skipping LLM test: {e}")

    def test_query_method_exists(self):
        """Test that query method exists."""
        try:
            client = LLMClient()
            assert hasattr(client, "query")
            assert callable(client.query)
        except ValueError:
            pytest.skip("Skipping LLM test: API key not configured")


class TestOfficeQAAgent:
    """Test OfficeQA agent functionality."""

    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""

        class MockLLMClient:
            def query(self, *args, **kwargs):
                return "Mock answer"

            def extract_answer(self, *args, **kwargs):
                return "Mock extracted answer"

            def perform_calculation(self, *args, **kwargs):
                return "Mock calculation: 600"

        return MockLLMClient()

    def test_agent_initialization(self, mock_llm_client):
        """Test agent initialization."""
        agent = OfficeQAAgent(mock_llm_client)
        assert agent.llm_client is mock_llm_client
        assert len(agent.results) == 0

    def test_process_task_qa(self, mock_llm_client):
        """Test processing a QA task."""
        agent = OfficeQAAgent(mock_llm_client)

        result = agent.process_task(
            task_id="test_1",
            question="What is the answer?",
            documents=["Document content"],
            task_type="qa",
        )

        assert result.task_id == "test_1"
        assert result.answer == "Mock answer"
        assert result.confidence > 0
        assert len(agent.results) == 1

    def test_process_task_extraction(self, mock_llm_client):
        """Test processing an extraction task."""
        agent = OfficeQAAgent(mock_llm_client)

        result = agent.process_task(
            task_id="test_2",
            question="Extract the value",
            documents=["Value: 100"],
            task_type="extraction",
        )

        assert result.task_id == "test_2"
        assert result.confidence > 0

    def test_get_results(self, mock_llm_client):
        """Test retrieving results."""
        agent = OfficeQAAgent(mock_llm_client)

        agent.process_task(
            task_id="test_1",
            question="Question 1",
            documents=["Doc"],
            task_type="qa",
        )

        results = agent.get_results()
        assert len(results) == 1
        assert results[0]["task_id"] == "test_1"

    def test_clear_results(self, mock_llm_client):
        """Test clearing results."""
        agent = OfficeQAAgent(mock_llm_client)

        agent.process_task(
            task_id="test_1",
            question="Question",
            documents=["Doc"],
        )

        assert len(agent.results) == 1
        agent.clear_results()
        assert len(agent.results) == 0
