# Use the same Python base image for consistency
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /frontend

# Install dependencies w/ uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY ./frontend /frontend/  

# Tell Docker to expose the port Streamlit will run on
EXPOSE 8501

# The command to run the Streamlit app.
# The --server.address=0.0.0.0 flag is crucial for Docker.
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]