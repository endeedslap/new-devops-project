import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    body = r.get_json()
    assert "message" in body
    assert "version" in body


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"


def test_version(client):
    r = client.get("/version")
    assert r.status_code == 200
    assert "version" in r.get_json()


def test_404(client):
    r = client.get("/does-not-exist")
    assert r.status_code == 404
    assert r.get_json()["error"] == "Not found"


def test_metrics_returns_prometheus_format(client):
    # Hit the app first so there's at least one request recorded
    client.get("/")
    r = client.get("/metrics")
    assert r.status_code == 200
    # Real exporter output includes request counters
    assert b"flask_http_request" in r.data or b"python_info" in r.data
