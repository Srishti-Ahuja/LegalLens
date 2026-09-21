FROM python:3.12-slim

# Install system dependencies (PostgreSQL client, build tools, poppler for PDF)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project source code (everything in backend/)
COPY . .

# Expose port (Render expects the service to listen on $PORT, but we bind to 0.0.0.0:8000)
EXPOSE 8000

# Run migrations and start the server with gunicorn
CMD gunicorn legal_project.wsgi:application --bind 0.0.0.0:${PORT} --workers 2
