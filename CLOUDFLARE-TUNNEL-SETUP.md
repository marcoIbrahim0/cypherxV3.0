# Cloudflare Tunnel Setup for Cursor Headless CLI

This guide will help you set up a Cloudflare tunnel to expose your Cursor headless CLI with a public IP address, making it accessible from anywhere on the internet.

## 🎯 What You'll Get

- **Public URL**: Access your Cursor CLI from anywhere
- **Secure Connection**: HTTPS with Cloudflare's SSL certificates
- **No Port Forwarding**: Works behind NAT/firewalls
- **Professional Domain**: Use your own domain or Cloudflare's free subdomain
- **Web Interface**: Beautiful status dashboard

## 📋 Prerequisites

1. **Cloudflare Account**: Free account at [cloudflare.com](https://cloudflare.com)
2. **Domain**: Your own domain or Cloudflare's free subdomain
3. **Docker**: Running on your machine
4. **Git**: To clone the repository

## 🚀 Quick Setup

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/marcoIbrahim0/cypherxV3.0.git
cd cypherxV3.0

# Make scripts executable
chmod +x cursor-docker.sh
chmod +x setup-cloudflare-tunnel.sh
```

### Step 2: Setup Cloudflare Tunnel

```bash
# Run the automated setup
./cursor-docker.sh tunnel-setup
```

The script will:
- Install cloudflared if needed
- Log you into Cloudflare
- Create a tunnel
- Set up DNS records
- Configure everything automatically

### Step 3: Start Services

```bash
# Build and start everything
./cursor-docker.sh build
./cursor-docker.sh start
```

### Step 4: Access Your Public Cursor CLI

Visit your public URL (e.g., `https://cursor-cli.yourdomain.com`) to see the web interface!

## 🔧 Manual Setup (Alternative)

If you prefer to set up manually or need more control:

### 1. Install cloudflared

**macOS:**
```bash
brew install cloudflared
```

**Linux:**
```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### 2. Login to Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser to authenticate with Cloudflare.

### 3. Create Tunnel

```bash
cloudflared tunnel create cypherx-cursor-cli
```

### 4. Configure DNS

```bash
# Replace with your actual domain
cloudflared tunnel route dns cypherx-cursor-cli cursor-cli.yourdomain.com
```

### 5. Get Credentials

```bash
cloudflared tunnel token <TUNNEL_ID> > cloudflared-credentials.json
```

### 6. Update Configuration

Edit `cloudflared.yml` and replace `cursor-cli.your-domain.com` with your actual hostname.

## 🌐 Domain Options

### Option 1: Your Own Domain
- **Pros**: Professional, memorable, branded
- **Cons**: Requires domain ownership
- **Example**: `cursor-cli.yourcompany.com`

### Option 2: Cloudflare Free Subdomain
- **Pros**: Free, no domain needed
- **Cons**: Less professional
- **Example**: `cursor-cli.yourname.trycloudflare.com`

### Option 3: Custom Subdomain
- **Pros**: Professional, memorable
- **Cons**: Requires domain setup
- **Example**: `ai.yourdomain.com`

## 🔒 Security Features

- **HTTPS**: Automatic SSL certificates
- **Authentication**: Cloudflare Access integration available
- **Rate Limiting**: Built-in DDoS protection
- **Geolocation**: Control access by country
- **IP Filtering**: Whitelist specific IPs

## 📊 Monitoring & Management

### Check Tunnel Status

```bash
# View tunnel logs
./cursor-docker.sh tunnel

# Check all services
./cursor-docker.sh status

# View container logs
./cursor-docker.sh logs
```

### Cloudflare Dashboard

Visit [dash.cloudflare.com](https://dash.cloudflare.com) to:
- Monitor tunnel health
- View analytics
- Configure security rules
- Manage DNS records

## 🚨 Troubleshooting

### Common Issues

#### 1. Tunnel Won't Start
```bash
# Check credentials
ls -la cloudflared-credentials.json

# Verify configuration
cat cloudflared.yml

# Check logs
./cursor-docker.sh tunnel
```

#### 2. DNS Not Resolving
- Wait 5-10 minutes for DNS propagation
- Check Cloudflare dashboard for DNS records
- Verify tunnel is running

#### 3. Connection Refused
```bash
# Check if containers are running
./cursor-docker.sh status

# Restart services
./cursor-docker.sh restart
```

#### 4. Permission Issues
```bash
# Fix file permissions
chmod 600 cloudflared-credentials.json
chmod 644 cloudflared.yml
```

### Debug Commands

```bash
# Test tunnel connectivity
cloudflared tunnel info cypherx-cursor-cli

# Check DNS resolution
nslookup cursor-cli.yourdomain.com

# Test HTTP connection
curl -I https://cursor-cli.yourdomain.com
```

## 🔄 Updates & Maintenance

### Update Cloudflare Tunnel

```bash
# Pull latest image
docker pull cloudflare/cloudflared:latest

# Restart services
./cursor-docker.sh restart
```

### Update Cursor CLI

```bash
# Rebuild with latest Cursor CLI
./cursor-docker.sh build
./cursor-docker.sh restart
```

### Backup Configuration

```bash
# Backup important files
cp cloudflared.yml cloudflared.yml.backup
cp cloudflared-credentials.json cloudflared-credentials.json.backup
```

## 🌟 Advanced Features

### Custom Domains

Add multiple hostnames to your tunnel:

```yaml
ingress:
  - hostname: cursor-cli.yourdomain.com
    service: http://cursor-headless-cli:3000
  - hostname: ai.yourdomain.com
    service: http://cursor-headless-cli:3000
  - hostname: dev.yourdomain.com
    service: http://cursor-headless-cli:3000
```

### Load Balancing

Route traffic to multiple instances:

```yaml
ingress:
  - hostname: cursor-cli.yourdomain.com
    service: http://cursor-headless-cli:3000
    originRequest:
      loadBalancer:
        pool: cursor-cli-pool
```

### Custom Headers

Add security headers:

```yaml
ingress:
  - hostname: cursor-cli.yourdomain.com
    service: http://cursor-headless-cli:3000
    originRequest:
      headers:
        - name: X-Custom-Header
          value: "Secure"
```

## 📚 Additional Resources

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cursor CLI Documentation](https://cursor.com/docs)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [GitHub Repository](https://github.com/marcoIbrahim0/cypherxV3.0)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Cloudflare tunnel logs
3. Check Docker container status
4. Open an issue on GitHub
5. Join the Cursor community

---

**Happy coding with your public Cursor CLI! 🚀**
