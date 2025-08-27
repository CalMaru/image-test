FROM python:3.12.10

ENV HOME /app
RUN mkdir -p ${HOME}
WORKDIR ${HOME}

RUN apt-get update -y && apt-get install -y poppler-utils\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/

COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv .venv && \
    uv sync --no-install-project --no-editable

COPY . .
