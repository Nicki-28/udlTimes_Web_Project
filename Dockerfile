# Use Python 3.13 as the base image (slim = smaller size, no extra tools)
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first (this helps Docker cache layers, 
# dependencies won't be reinstalled unless these files change)
COPY pyproject.toml uv.lock ./

# Install the exact packages pinned in uv.lock
# --frozen: don't update the lockfile, just install what's in it
# --no-dev: skip development-only dependencies
RUN uv sync --frozen --extra test
RUN apt-get update && apt-get install -y chromium chromium-driver && rm -rf /var/lib/apt/lists/*
# Copy the entire project into the container
COPY . .

# Tell Docker this container will listen on port 8000
EXPOSE 8000

# Command that runs when the container starts:
# 1. Apply database migrations (create/update tables)
# 2. Start Django's development server on all interfaces (0.0.0.0)
CMD uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000

# 127.0.0.1 = only reachable from inside the container (default, won't work with Docker)
# 0.0.0.0 = listen on all interfaces, so the host machine can reach the container