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

### Step 3: Configure Service URLs (IMPORTANT!)

**⚠️ Critical Step**: After setting up the tunnel, you MUST update the service URLs in your Cloudflare dashboard:

1. **Go to**: [dash.cloudflare.com](https://dash.cloudflare.com) → Zero Trust → Tunnels → [Your Tunnel Name]
2. **Click**: "Public hostnames" tab
3. **For each hostname**, set the URL to: `http://YOUR_MACHINE_IP:3000`

**Example**:
- **Hostname**: `cursor-cli.yourdomain.com`
- **URL**: `http://192.168.1.9:3000` (replace with your actual IP)

**❌ Don't use**: `localhost:3000` or `cursor-headless-cli:3000`  
**✅ Use**: `http://YOUR_MACHINE_IP:3000`

### Step 3: Start Services

```bash
# Build and start everything
./cursor-docker.sh build
./cursor-docker.sh start
```

### Step 4: Access Your Public Cursor CLI

Visit your public URL (e.g., `https://cursor-cli.yourdomain.com`) to see the web interface!

## 🧪 Testing & Verification

### Test Local Service First
```bash
# Check if local service is running
curl -I http://localhost:3000

# Check if tunnel is running
./cursor-docker.sh tunnel

# Check container status
./cursor-docker.sh status
```

### Test Public Access
1. **Wait 1-2 minutes** after updating Cloudflare dashboard
2. **Test your public URL**: `https://cursor-cli.yourdomain.com`
3. **Expected result**: Beautiful Cursor CLI web interface

### Common Test Results
- **Error 1016**: Service URL not configured correctly
- **Error 502**: Using wrong service URL (localhost instead of IP)
- **Success**: Beautiful web interface loads

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

### 7. Configure Service URLs (CRITICAL!)

**⚠️ IMPORTANT**: You must configure the service URLs in your Cloudflare dashboard:

1. **Go to**: [dash.cloudflare.com](https://dash.cloudflare.com) → Zero Trust → Tunnels → [Your Tunnel Name]
2. **Click**: "Public hostnames" tab
3. **For each hostname**, configure:
   - **Hostname**: `cursor-cli.yourdomain.com`
   - **Path**: `/`
   - **Type**: `HTTP`
   - **URL**: `http://YOUR_MACHINE_IP:3000`

**Get Your Machine IP**:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

**Example Configuration**:
- **Hostname**: `cursor-cli.valensjewelry.com`
- **URL**: `http://192.168.1.9:3000`

**❌ Common Mistakes**:
- Using `localhost:3000` (won't work from tunnel)
- Using `cursor-headless-cli:3000` (Docker service names don't resolve)
- Using `127.0.0.1:3000` (same as localhost issue)

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

#### 2. Error 1016: Origin DNS Error
**Problem**: Cloudflare can't resolve the service URL  
**Solution**: Update the service URL in Cloudflare dashboard to use your machine's IP address

```bash
# Get your machine's IP address
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1

# Use this IP in Cloudflare dashboard
# Example: http://192.168.1.9:3000
```

#### 3. Error 502: Bad Gateway
**Problem**: Tunnel connects but can't reach your local service  
**Solution**: 
- ❌ Don't use: `localhost:3000` or `cursor-headless-cli:3000`
- ✅ Use: `http://YOUR_MACHINE_IP:3000`

#### 4. Invalid JSON Credentials
**Problem**: `cloudflared-credentials.json` contains invalid JSON  
**Solution**: Regenerate the credentials file

```bash
# Remove old file and regenerate
rm cloudflared-credentials.json
cloudflared tunnel token --cred-file cloudflared-credentials.json YOUR_TUNNEL_ID
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

## 📋 Quick Reference

### Essential Commands
```bash
# Start services
./cursor-docker.sh start

# Check status
./cursor-docker.sh status

# View tunnel logs
./cursor-docker.sh tunnel

# Get machine IP
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

### Critical Configuration
- **Service URL**: Must use `http://YOUR_MACHINE_IP:3000`
- **Don't use**: `localhost:3000` or Docker service names
- **Tunnel**: Must be running and connected
- **DNS**: Must be configured in Cloudflare dashboard

### Success Checklist
- [ ] Tunnel is running (`./cursor-docker.sh tunnel`)
- [ ] Local service accessible (`curl localhost:3000`)
- [ ] Service URL configured with machine IP
- [ ] DNS record created in Cloudflare
- [ ] Public URL loads web interface

---

**Happy coding with your public Cursor CLI! 🚀**
