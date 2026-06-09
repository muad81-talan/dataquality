import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def csv_bytes(content="col1,col2\n1,2\n3,4\n"):
    return content.encode()


def test_oversized_file_rejected():
    big = b"a" * (101 * 1024 * 1024)
    response = client.post("/upload", files={"file": ("big.csv", io.BytesIO(big), "text/csv")})
    assert response.status_code == 400


def test_non_csv_rejected():
    response = client.post("/upload", files={"file": ("data.txt", io.BytesIO(b"hello"), "text/plain")})
    assert response.status_code == 400


def test_valid_csv_returns_200():
    response = client.post("/upload", files={"file": ("data.csv", io.BytesIO(csv_bytes()), "text/csv")})
    assert response.status_code == 200
