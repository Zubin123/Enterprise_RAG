FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project
COPY . .

# Install dependencies
RUN uv pip install -r requirements.txt

# Expose Render port
EXPOSE 8000

# Start server
CMD ["python", "-m", "app.main"]
