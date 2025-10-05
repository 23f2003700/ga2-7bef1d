FROM python:3.11-slim

# Create the same UID (1000) that Spaces uses when running your container
RUN useradd -m -u 1000 user

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory and install Python dependencies before copying source
WORKDIR /home/user/app
COPY --chown=user requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=user . .

# Switch to non-root user for security
USER user

# Set environment variables
ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH
ENV APP_PORT=7358

# Expose the required port
EXPOSE 7358

# Health check for container monitoring
HEALTHCHEK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7358/health || exit 1

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7358"]