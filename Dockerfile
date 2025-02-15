FROM python:3.11-slim

# Install Poetry
RUN pip install --no-cache-dir poetry

# Disable Poetry virtual environments
RUN poetry config virtualenvs.create false

# Set working directory
WORKDIR /code

# Copy only dependency-related files first (better layer caching)
COPY ./pyproject.toml ./README.md ./poetry.lock* ./

# Install dependencies without installing the package itself
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY ./packages ./packages  # Ensure correct directory name
COPY ./app ./app

# Expose port for the application
EXPOSE 8080

# Run the application using Uvicorn
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]
