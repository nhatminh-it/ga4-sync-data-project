# Use Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Chalice local server for testing
CMD ["chalice", "local", "--host", "0.0.0.0"]
