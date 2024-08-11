FROM python:3.11.9-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY backend/requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

FROM python:3.11.9-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY backend/ backend/
CMD [".venv/bin/python3", "-m", "app"]
