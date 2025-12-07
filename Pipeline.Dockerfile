# Default Python trixie slim image with uv built in
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Set workdir to /app
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies from pyproject.toml
RUN uv sync

# Download libgomp1 for lightgbm
RUN apt-get update && apt-get install -y libgomp1

# Run Pipeline
ENTRYPOINT ["uv", "run", "kedro", "run"]
