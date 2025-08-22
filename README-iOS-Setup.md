# 🍎 iOS App Setup - Quick Start

## 🚀 What You Need

To make your Cursor CLI work in an iOS app, you need:

1. **API Server** - REST endpoints for iOS communication
2. **Authentication** - Secure API key management
3. **Real-time Communication** - Chat with the CLI
4. **Mobile-Optimized Interface** - Touch-friendly UI

## ⚡ Quick Setup

### 1. Rebuild Docker Container
```bash
# Stop current services
./cursor-docker.sh stop

# Rebuild with new API server
./cursor-docker.sh build

# Start services
./cursor-docker.sh start
```

### 2. Add DNS Records
In your Cloudflare dashboard, add:
- **Hostname**: `api.valensjewelry.com`
- **Service**: `http://192.168.1.9:5001`

### 3. Test API Endpoints
```bash
# Health check
curl https://api.valensjewelry.com/api/health

# Test login (replace with your API key)
curl -X POST https://api.valensjewelry.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key":"your_cursor_api_key"}'
```

## 📱 iOS App Requirements

### Minimum iOS Version
- **iOS 15.0+** (for async/await support)
- **SwiftUI** for modern UI
- **Combine** for reactive programming

### Required Frameworks
```swift
import Foundation
import SwiftUI
import Combine
import Security  // For Keychain
```

### Network Configuration
Add to your `Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <key>NSExceptionDomains</key>
    <dict>
        <key>api.valensjewelry.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <false/>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.2</string>
        </dict>
    </dict>
</dict>
```

## 🔑 API Key Setup

### 1. Get Your Cursor API Key
- Go to [cursor.com](https://cursor.com)
- Sign in to your account
- Navigate to Settings → API Keys
- Create a new API key

### 2. Store Securely in iOS
```swift
// Use the KeychainManager from IOS-API-DOCS.md
KeychainManager.saveAPIKey("your_api_key_here")
```

## 🧪 Testing Your Setup

### 1. Test Local API
```bash
# Check if API server is running
curl http://localhost:5001/api/health
```

### 2. Test Public API
```bash
# Test from external network
curl https://api.valensjewelry.com/api/health
```

### 3. Test Authentication
```bash
curl -X POST https://api.valensjewelry.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key":"your_api_key"}'
```

## 🚨 Common Issues

### 1. API Server Not Starting
```bash
# Check container logs
./cursor-docker.sh logs

# Check if port 5000 is exposed
docker ps | grep 5000
```

### 2. CORS Errors in iOS
- Ensure CORS is enabled in `api-server.py`
- Check if the API server is running on port 5000

### 3. Authentication Fails
- Verify your API key is correct
- Check if the session is being created properly
- Look for errors in the API server logs

## 📋 Next Steps

1. **Implement the iOS app** using the code from `IOS-API-DOCS.md`
2. **Test authentication** with your API key
3. **Test CLI communication** by sending messages
4. **Add error handling** and user feedback
5. **Implement offline support** and retry logic

## 🔗 Useful Links

- **Full API Documentation**: `IOS-API-DOCS.md`
- **Cloudflare Tunnel Setup**: `CLOUDFLARE-TUNNEL-SETUP.md`
- **Docker Management**: `cursor-docker.sh`
- **Repository**: [github.com/marcoIbrahim0/cypherxV3.0](https://github.com/marcoIbrahim0/cypherxV3.0)

---

**Your Cursor CLI is now ready for iOS! 🚀**
