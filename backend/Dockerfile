# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
# This is done first to leverage Docker's layer caching
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container at /code
COPY ./ /code/

# Run the app. "main:app" assumes your file is main.py and your FastAPI instance is named "app".
# The host 0.0.0.0 makes the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]