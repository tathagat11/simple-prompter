FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir poetry

# Disable Poetry's virtual environment creation
RUN poetry config virtualenvs.create false

# Set working directory
WORKDIR /code

COPY ./data /code/data

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY ./app ./app

# Expose the port (optional, for documentation purposes)
EXPOSE 8000

# Set environment variable for port
ENV PORT=8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]