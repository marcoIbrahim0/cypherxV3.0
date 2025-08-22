# Cursor Headless CLI Installation & Usage Guide

This guide provides step-by-step instructions for installing and using the Cursor headless CLI, both locally and in Docker containers.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Installation](#local-installation)
3. [Docker Installation](#docker-installation)
4. [Authentication with API Key](#authentication-with-api-key)
5. [Basic Usage](#basic-usage)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- **Operating System**: macOS, Linux, or Windows (WSL)
- **Shell**: bash, zsh, or fish
- **Docker**: Required only for containerized installation
- **Internet Connection**: For downloading and authentication

## Local Installation

### Step 1: Install Cursor CLI

```bash
# Download and install Cursor CLI
curl https://cursor.com/install -fsS | bash
```

### Step 2: Add to PATH

**For bash:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**For zsh:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**For fish:**
```bash
mkdir -p $HOME/.config/fish
echo 'fish_add_path $HOME/.local/bin' >> $HOME/.config/fish/config.fish
source $HOME/.config/fish/config.fish
```

### Step 3: Verify Installation

```bash
cursor-agent --help
```

## Docker Installation

### Step 1: Clone or Download Files

Ensure you have these files in your project directory:
- `Dockerfile`
- `docker-compose.yml`
- `cursor-docker.sh` (management script)

### Step 2: Build Docker Image

```bash
# Make the script executable
chmod +x cursor-docker.sh

# Build the image
./cursor-docker.sh build
```

### Step 3: Start Container

```bash
./cursor-docker.sh start
```

### Step 4: Access Container

```bash
./cursor-docker.sh shell
```

## Authentication with API Key

### Step 1: Get Your API Key

1. Go to [cursor.com](https://cursor.com)
2. Sign in to your account
3. Navigate to **Settings** → **API Keys**
4. Click **Generate New API Key**
5. Copy the generated key (keep it secure!)

### Step 2: Use API Key

#### **Local Installation:**
```bash
# Method 1: Environment variable
export CURSOR_API_KEY="your-api-key-here"
cursor-agent

# Method 2: Command line flag
cursor-agent --api-key "your-api-key-here"
```

#### **Docker Installation:**
```bash
# From host machine
export CURSOR_API_KEY="your-api-key-here"
./cursor-docker.sh restart

# Or set in docker-compose.yml
environment:
  - CURSOR_API_KEY=your-api-key-here
```

### Step 3: Verify Authentication

```bash
# Check authentication status
cursor-agent status
```

## Basic Usage

### Starting the CLI

```bash
# Basic start
cursor-agent

# With specific model
cursor-agent --model gpt-4o

# Non-interactive mode (for scripts)
cursor-agent --print "Write a Python function"
```

### Available Models

- **GPT Models**: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- **Claude Models**: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Gemini Models**: `gemini-pro`, `gemini-pro-1.5`

### Switching Models

```bash
# Start with specific model
cursor-agent --model claude-3-sonnet

# Use different model for specific command
cursor-agent --model gpt-4o --print "Explain Docker"
```

## Advanced Features

### Command Line Options

```bash
# View all options
cursor-agent --help

# Common flags
cursor-agent --model gpt-4o          # Specify model
cursor-agent --print                 # Non-interactive mode
cursor-agent --background            # Start in background
cursor-agent --force                 # Allow all commands
cursor-agent --with-diffs            # Include git changes
```

### Working with Files

```bash
# Analyze specific file
cursor-agent --print "Review this code" < filename.py

# Include git changes
cursor-agent --with-diffs --print "What changed?"
```

### Background Mode

```bash
# Start in background
cursor-agent --background

# Resume latest chat
cursor-agent resume
```

## Docker Management Commands

```bash
# Build image
./cursor-docker.sh build

# Start container
./cursor-docker.sh start

# Stop container
./cursor-docker.sh stop

# View logs
./cursor-docker.sh logs

# Access shell
./cursor-docker.sh shell

# Check status
./cursor-docker.sh status

# Clean up
./cursor-docker.sh clean
```

## Troubleshooting

### Common Issues

#### **1. "command not found: cursor-agent"**
```bash
# Check if PATH is set correctly
echo $PATH | grep .local/bin

# Reinstall if needed
curl https://cursor.com/install -fsS | bash
```

#### **2. "Permission denied"**
```bash
# Fix permissions
chmod +x ~/.local/bin/cursor-agent

# Or reinstall as current user
curl https://cursor.com/install -fsS | bash
```

#### **3. "Authentication failed"**
```bash
# Check API key
echo $CURSOR_API_KEY

# Re-authenticate
cursor-agent logout
export CURSOR_API_KEY="your-api-key-here"
cursor-agent
```

#### **4. Docker container restarting**
```bash
# Check logs
./cursor-docker.sh logs

# Rebuild if needed
./cursor-docker.sh clean
./cursor-docker.sh build
```

### Getting Help

```bash
# Command help
cursor-agent --help

# Check version
cursor-agent --version

# Check status
cursor-agent status
```

## Security Best Practices

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **Docker Security**
   - Run as non-root user (already configured)
   - Use read-only mounts where possible
   - Keep images updated

3. **Network Security**
   - Use private networks in Docker
   - Limit port exposure
   - Monitor container logs

## Examples

### Example 1: Code Review
```bash
cursor-agent --model gpt-4o --print "Review this Python code for best practices" < main.py
```

### Example 2: Bug Fixing
```bash
cursor-agent --model claude-3-sonnet --print "Help me fix this error" < error_log.txt
```

### Example 3: Documentation
```bash
cursor-agent --model gemini-pro --print "Generate documentation for this function" < function.py
```

## Support

- **Official Documentation**: [cursor.com/docs](https://cursor.com/docs)
- **GitHub Issues**: [github.com/cursor-ai/cursor](https://github.com/cursor-ai/cursor)
- **Community**: [discord.gg/cursor](https://discord.gg/cursor)

## License

This installation guide is provided as-is. Cursor CLI is subject to its own license terms.

---

**Happy coding with Cursor! 🚀**
