# Use the same Python base image for consistency
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the Streamlit app code
COPY ./ /app/

# Tell Docker to expose the port Streamlit will run on
EXPOSE 8501

# The command to run the Streamlit app.
# The --server.address=0.0.0.0 flag is crucial for Docker.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]