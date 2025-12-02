# Default Python trixie slim image with uv built in
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Set workdir to app
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies from pyproject.toml
RUN uv sync

# Run Pipeline
ENTRYPOINT ["uv", "run", "kedro", "run"]
