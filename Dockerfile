FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-noto-core \
    fonts-noto-extra \
    fonts-noto-ui-core \
    fonts-noto-ui-extra \
    fonts-noto-mono \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r dilauser && useradd -r -g dilauser dilauser

# Create directories
RUN mkdir -p /app/output /app/logs /app/app/templates && \
    chown -R dilauser:dilauser /app

# Copy requirements and install dependencies
COPY --chown=dilauser:dilauser requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY --chown=dilauser:dilauser docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Copy application code
COPY --chown=dilauser:dilauser . /app/

# Create necessary directories
RUN mkdir -p /app/app/static/fonts/google_fonts /app/app/static/fonts/local_fonts /app/fonts /app/images && \
    chown -R dilauser:dilauser /app/app/static/fonts /app/fonts /app/images

# Ensure output directories exist and are writable
RUN mkdir -p /app/output/images /app/output/temp && \
    chown -R dilauser:dilauser /app/output

# Switch to non-root user
USER dilauser

# Expose port
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["prod"] 