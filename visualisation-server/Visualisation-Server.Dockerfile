# Default Python alpine image with uv built in
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set workdir to /app
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies from pyproject.toml
RUN uv sync

# Expose port used by Flask
EXPOSE 5500

# Start viusalisation server
ENTRYPOINT [ "uv", "run", "main.py" ]