# Flask DevOps Project

End-to-end DevOps project: Flask + Docker + Terraform + AWS EKS + Kubernetes + Helm + GitHub Actions + Prometheus + Grafana.

## Phase 1 - Application

- Flask app with 4 endpoints: `/`, `/health`, `/version`, `/metrics`
- Structured JSON logging
- Prometheus metrics via `prometheus_flask_exporter`
- 5 pytest tests, all passing

## Local development

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    pytest -v
    flask --app app run

## Project Status

- [x] Phase 1 - Application
- [x] Phase 2 - Git & GitHub
- [ ] Phase 3 - Docker
