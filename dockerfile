FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Copy all files
COPY . .

# Install dependencies from pyproject.toml
RUN uv sync

# Run Pipeline
ENTRYPOINT ["uv", "run", "kedro", "run"]