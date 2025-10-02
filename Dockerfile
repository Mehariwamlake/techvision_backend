# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /techvision_backend

# Install dependencies
COPY requirements.txt /techvision_backend/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /techvision_backend/

# Collect static files (optional for admin panel)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
