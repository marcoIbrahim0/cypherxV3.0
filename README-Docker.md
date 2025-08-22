# Cursor Headless CLI in Docker

This setup provides a containerized version of the Cursor headless CLI for consistent, isolated AI coding assistance.

## Prerequisites

- Docker and Docker Compose installed
- Cursor API key (optional, but recommended)

## Quick Start

1. **Build the Docker image:**
   ```bash
   ./cursor-docker.sh build
   ```

2. **Start the container:**
   ```bash
   ./cursor-docker.sh start
   ```

3. **Access the CLI:**
   ```bash
   ./cursor-docker.sh shell
   ```

## Configuration

### Environment Variables

Set your Cursor API key (optional):
```bash
export CURSOR_API_KEY="your-api-key-here"
```

### Volume Mounts

The container automatically mounts:
- Current workspace directory (`./`) → `/workspace`
- Persistent cursor data → `/tmp/cursor-headless`
- Git configuration (read-only)
- SSH keys (read-only)

## Usage

### Management Commands

```bash
# Build the image
./cursor-docker.sh build

# Start the container
./cursor-docker.sh start

# Stop the container
./cursor-docker.sh stop

# Restart the container
./cursor-docker.sh restart

# View logs
./cursor-docker.sh logs

# Open shell in container
./cursor-docker.sh shell

# Check status
./cursor-docker.sh status

# Clean up everything
./cursor-docker.sh clean
```

### Direct Docker Commands

```bash
# Build
docker compose build

# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f cursor-headless

# Execute commands
docker compose exec cursor-headless cursor-agent --help
```

## Features

- **Isolated Environment**: Runs in its own container with all dependencies
- **Persistent Data**: Cursor data persists across container restarts
- **Git Integration**: Access to your git configuration and SSH keys
- **Security**: Runs as non-root user
- **Portability**: Works consistently across different environments

## Troubleshooting

### Container Won't Start
- Check if Docker is running
- Verify no port conflicts
- Check logs: `./cursor-docker.sh logs`

### Permission Issues
- Ensure SSH keys have correct permissions
- Check git configuration file permissions

### Performance Issues
- The container includes build tools for better code analysis
- Consider mounting only necessary directories for large projects

## Customization

### Modify Dockerfile
Edit `Dockerfile` to:
- Change base image
- Add additional packages
- Modify user configuration

### Modify docker-compose.yml
Edit `docker-compose.yml` to:
- Change port mappings
- Add environment variables
- Modify volume mounts

## Security Notes

- Container runs as non-root user
- SSH keys are mounted read-only
- Git config is mounted read-only
- Consider using Docker secrets for sensitive data in production

## Support

For issues with the Cursor CLI itself, refer to the official Cursor documentation.
For Docker-related issues, check Docker logs and ensure proper permissions.
