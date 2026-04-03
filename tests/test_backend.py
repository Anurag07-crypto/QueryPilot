import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


# Import app AFTER patching agent to avoid real initialization
with patch("work_space.agent.initialize_loader"):
    from server.backend import app

client = TestClient(app)

class TestChatEndPoint:
    """Tests for /chat FastAPI endpoint."""
    def test_chat_returns_200_on_success(self):
        """Valid query should return 200 with response key."""
        with patch("backend.my_agent", return_value="test answer"):
            response = client.post(
                "/chat",
                json={"query":"what is RAG"}
            )
        assert response.status_code == 200
        assert "response" in response.json()
    
    def test_chat_returns_correct_answer(self):
        """Response should contain the agent's answer."""
        with patch("backend.my_agent", return_value="RAG is retrieval augmented generation"):
            response = client.post(
                "/chat",
                json={"query": "what is RAG?"}
            )
        assert response.json()["response"] == "RAG is retrieval augmented generation"

    def test_chat_returns_500_on_runtime_error(self):
        """RuntimeError in agent should return 500."""
        with patch("backend.my_agent", side_effect=RuntimeError("model crashed")):
            response = client.post(
                "/chat",
                json={"query": "test"}
            )
        assert response.status_code == 500

    def test_chat_empty_query(self):
        """Empty query should still return 200 — agent handles it."""
        with patch("backend.my_agent", return_value="I need more context"):
            response = client.post(
                "/chat",
                json={"query": ""}
            )
        assert response.status_code == 200