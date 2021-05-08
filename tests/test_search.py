from fastapi.testclient import TestClient
from ..app import app


def test_get_vocabulary():
    with TestClient(app) as testClient:
        response = testClient.get("/search/vocabulary")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert all(
            term
            not in [
                "in",
                "and",
                "or",
                "an",
                "a",
                "the",
                "that",
                "what",
            ]
            for term in response.json()
        )
