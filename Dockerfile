FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/ ./src/


CMD ["uv","run","uvicorn","src.main:app","--host","0.0.0.0","--port","8000"]

