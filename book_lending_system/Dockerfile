# Base image
FROM python:3.13.3-slim-bookworm

# Set working directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.adapters.api.rest.fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
