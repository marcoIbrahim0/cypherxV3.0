FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Create a non-root user for better security
RUN useradd -m -s /bin/bash cursor

# Install Cursor CLI as the cursor user
USER cursor
RUN curl https://cursor.com/install -fsS | bash

# Set PATH for the user
ENV PATH="/home/cursor/.local/bin:$PATH"

# Switch back to root to set permissions
USER root
RUN chown -R cursor:cursor /workspace

# Switch back to cursor user
USER cursor

# Copy web interface
COPY --chown=cursor:cursor web-interface.html /workspace/index.html

# Install a simple HTTP server
RUN pip3 install --user http-server

# Expose port for the agent (if needed)
EXPOSE 3000

# Default command to start the headless agent and serve web interface
CMD ["sh", "-c", "python3 -m http.server 3000 & cursor-agent"]
