#!/bin/bash

# Cloudflare Tunnel Setup Script for Cursor Headless CLI
# This script helps you set up a Cloudflare tunnel to expose your Cursor CLI publicly

set -e

echo "🚀 Setting up Cloudflare Tunnel for Cursor Headless CLI"
echo "======================================================"

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "📥 Installing cloudflared..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install cloudflared
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
    else
        echo "❌ Unsupported OS. Please install cloudflared manually from: https://github.com/cloudflare/cloudflared/releases"
        exit 1
    fi
fi

echo "✅ cloudflared is installed"

# Login to Cloudflare
echo "🔐 Logging into Cloudflare..."
cloudflared tunnel login

# Create tunnel
echo "🌐 Creating tunnel..."
TUNNEL_NAME="cypherx-cursor-cli"
cloudflared tunnel create $TUNNEL_NAME

# Get tunnel ID
TUNNEL_ID=$(cloudflared tunnel list --name $TUNNEL_NAME --format json | jq -r '.[0].id')
echo "📋 Tunnel ID: $TUNNEL_ID"

# Create DNS record
echo "📝 Creating DNS record..."
read -p "Enter your domain (e.g., example.com): " DOMAIN
read -p "Enter subdomain for Cursor CLI (e.g., cursor-cli): " SUBDOMAIN

FULL_HOSTNAME="$SUBDOMAIN.$DOMAIN"
echo "🌍 Full hostname will be: $FULL_HOSTNAME"

# Create DNS record
cloudflared tunnel route dns $TUNNEL_NAME $FULL_HOSTNAME

# Update configuration file
echo "📝 Updating configuration file..."
sed -i.bak "s/cursor-cli\.your-domain\.com/$FULL_HOSTNAME/g" cloudflared.yml

# Copy credentials
echo "🔑 Copying tunnel credentials..."
cloudflared tunnel token $TUNNEL_ID > cloudflared-credentials.json

echo ""
echo "✅ Cloudflare tunnel setup complete!"
echo ""
echo "📋 Summary:"
echo "   Tunnel Name: $TUNNEL_NAME"
echo "   Tunnel ID: $TUNNEL_ID"
echo "   Public URL: https://$FULL_HOSTNAME"
echo ""
echo "🚀 Next steps:"
echo "   1. Update your domain's DNS if needed"
echo "   2. Run: ./cursor-docker.sh start"
echo "   3. Access your Cursor CLI at: https://$FULL_HOSTNAME"
echo ""
echo "📚 For more info: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/"
