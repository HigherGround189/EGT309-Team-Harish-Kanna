# Default Python trixie slim image with uv built in
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Set workdir to /app
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies from pyproject.toml
RUN uv sync

# Expose port used by Jupyter
EXPOSE 8888

# Start Development server
ENTRYPOINT ["uv", "run", "kedro", "jupyter", "notebook"]
CMD ["--allow-root", "--NotebookApp.token=", "--NotebookApp.password=", "--ip=0.0.0.0"]