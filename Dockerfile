# syntax=docker/dockerfile:1.6

# -------------------------------------------------------------------
# Flask DevOps app — production-style image
# - small base (slim)
# - dependency layer cached separately from app code
# - runs as non-root
# - gunicorn (production WSGI server), not flask dev server
# - includes HEALTHCHECK
# -------------------------------------------------------------------

FROM python:3.12-slim AS runtime

# Environment for Python in containers:
#   PYTHONDONTWRITEBYTECODE  — don't write .pyc files
#   PYTHONUNBUFFERED         — flush stdout/stderr immediately (so logs appear live)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5000 \
    APP_VERSION=1.0.0

WORKDIR /app

# --- Layer 1: dependencies -----------------------------------------
# Copy ONLY requirements.txt first. As long as this file doesn't change,
# Docker reuses this layer on rebuild — even if app.py changes.
COPY requirements.txt ./

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# --- Layer 2: application code -------------------------------------
COPY app.py ./

# --- Non-root user --------------------------------------------------
# Create an unprivileged user and switch to it. If the container is
# compromised, the attacker doesn't get root.
RUN groupadd --system app \
 && useradd --system --gid app --no-create-home --shell /usr/sbin/nologin app \
 && chown -R app:app /app

USER app

EXPOSE 5000

# --- Health check ---------------------------------------------------
# Docker will run this every 30s. If it fails 3 times in a row,
# the container is marked unhealthy. Uses Python (no curl in slim image).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:5000/health').status == 200 else 1)"

# --- Start command --------------------------------------------------
# gunicorn with 2 worker processes; logs to stdout/stderr so Docker captures them.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", \
     "--access-logfile", "-", "--error-logfile", "-", \
     "app:app"]
