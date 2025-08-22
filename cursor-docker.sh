#!/bin/bash

# Cursor Headless CLI Docker Management Script

case "$1" in
    "build")
        echo "Building Cursor headless CLI Docker image..."
        docker compose build
        ;;
    "start")
        echo "Starting Cursor headless CLI container..."
        docker compose up -d
        ;;
    "stop")
        echo "Stopping Cursor headless CLI container..."
        docker compose down
        ;;
    "restart")
        echo "Restarting Cursor headless CLI container..."
        docker compose restart
        ;;
    "logs")
        echo "Showing container logs..."
        docker compose logs -f cursor-headless
        ;;
    "shell")
        echo "Opening shell in Cursor headless CLI container..."
        docker compose exec cursor-headless bash
        ;;
    "status")
        echo "Container status:"
        docker compose ps
        ;;
    "tunnel")
        echo "Cloudflare tunnel status:"
        docker compose logs cloudflared --tail=20
        ;;
    "tunnel-setup")
        echo "Setting up Cloudflare tunnel..."
        chmod +x setup-cloudflare-tunnel.sh
        ./setup-cloudflare-tunnel.sh
        ;;
    "clean")
        echo "Cleaning up containers and volumes..."
        docker compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: $0 {build|start|stop|restart|logs|shell|status|tunnel|tunnel-setup|clean}"
        echo ""
        echo "Commands:"
        echo "  build         - Build the Docker image"
        echo "  start         - Start the container"
        echo "  stop          - Stop the container"
        echo "  restart       - Restart the container"
        echo "  logs          - Show container logs"
        echo "  shell         - Open shell in container"
        echo "  status        - Show container status"
        echo "  tunnel        - Show Cloudflare tunnel logs"
        echo "  tunnel-setup  - Set up Cloudflare tunnel"
        echo "  clean         - Clean up containers and volumes"
        exit 1
        ;;
esac
