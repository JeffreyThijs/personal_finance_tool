import os
from app.settings import get_settings
from fastapi.testclient import TestClient


def test_app(client: TestClient):
    assert isinstance(client, TestClient)

    response = client.get("/")
    assert response.status_code == 200
    
    
