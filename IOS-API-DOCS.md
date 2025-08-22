# 🍎 iOS App Integration Guide

## Overview
This guide explains how to integrate your iOS app with the Cursor Headless CLI through the REST API.

## 🔑 API Endpoints

### Base URL
```
https://your-domain.com:5000/api
```

### Authentication
All API calls require a valid session. Start by calling the login endpoint.

#### POST `/api/auth/login`
**Request Body:**
```json
{
  "api_key": "your_cursor_api_key_here"
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "authenticated",
  "message": "Login successful"
}
```

**iOS Swift Example:**
```swift
func login(apiKey: String) async throws -> LoginResponse {
    let url = URL(string: "https://your-domain.com:5000/api/auth/login")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = ["api_key": apiKey]
    request.httpBody = try JSONSerialization.data(withJSONObject: body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(LoginResponse.self, from: data)
}
```

### CLI Management

#### POST `/api/cli/start`
Start the Cursor CLI for your session.

**Response:**
```json
{
  "message": "CLI started successfully",
  "status": "running",
  "session_id": "uuid-here"
}
```

#### GET `/api/cli/status`
Get the current status of your CLI session.

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "running",
  "created_at": "2024-01-01T12:00:00",
  "last_activity": "2024-01-01T12:05:00",
  "uptime": 300.0
}
```

#### POST `/api/cli/stop`
Stop the Cursor CLI for your session.

**Response:**
```json
{
  "message": "CLI stopped successfully",
  "status": "stopped"
}
```

### Chat with CLI

#### POST `/api/cli/chat`
Send a message to the Cursor CLI.

**Request Body:**
```json
{
  "message": "Write a Python function to calculate fibonacci numbers"
}
```

**Response:**
```json
{
  "message": "Message received",
  "response": "CLI received: Write a Python function to calculate fibonacci numbers",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Session Management

#### POST `/api/logout`
Logout and clean up your session.

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

## 📱 iOS App Implementation

### 1. Create API Client

```swift
class CursorAPIClient {
    private let baseURL = "https://your-domain.com:5000/api"
    private var sessionID: String?
    
    func login(apiKey: String) async throws -> LoginResponse {
        // Implementation above
    }
    
    func startCLI() async throws -> CLIResponse {
        guard let sessionID = sessionID else {
            throw APIError.notAuthenticated
        }
        
        let url = URL(string: "\(baseURL)/cli/start")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(CLIResponse.self, from: data)
    }
    
    func sendMessage(_ message: String) async throws -> ChatResponse {
        guard let sessionID = sessionID else {
            throw APIError.notAuthenticated
        }
        
        let url = URL(string: "\(baseURL)/cli/chat")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["message": message]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(ChatResponse.self, from: data)
    }
}
```

### 2. Create Data Models

```swift
struct LoginResponse: Codable {
    let sessionID: String
    let status: String
    let message: String
    
    enum CodingKeys: String, CodingKey {
        case sessionID = "session_id"
        case status, message
    }
}

struct CLIResponse: Codable {
    let message: String
    let status: String
    let sessionID: String
    
    enum CodingKeys: String, CodingKey {
        case message, status
        case sessionID = "session_id"
    }
}

struct ChatResponse: Codable {
    let message: String
    let response: String
    let timestamp: String
}

enum APIError: Error {
    case notAuthenticated
    case invalidResponse
    case networkError
}
```

### 3. Create Main View

```swift
struct ContentView: View {
    @StateObject private var viewModel = CursorViewModel()
    @State private var messageText = ""
    
    var body: some View {
        NavigationView {
            VStack {
                // Status Section
                StatusView(status: viewModel.cliStatus)
                
                // Chat Section
                ScrollView {
                    LazyVStack {
                        ForEach(viewModel.messages, id: \.id) { message in
                            MessageView(message: message)
                        }
                    }
                }
                
                // Input Section
                HStack {
                    TextField("Ask Cursor AI...", text: $messageText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button("Send") {
                        Task {
                            await viewModel.sendMessage(messageText)
                            messageText = ""
                        }
                    }
                    .disabled(messageText.isEmpty || !viewModel.isAuthenticated)
                }
                .padding()
            }
            .navigationTitle("Cursor CLI")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Login") {
                        viewModel.showLogin = true
                    }
                }
            }
            .sheet(isPresented: $viewModel.showLogin) {
                LoginView(viewModel: viewModel)
            }
        }
    }
}
```

### 4. Create ViewModel

```swift
class CursorViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var cliStatus = "disconnected"
    @Published var messages: [ChatMessage] = []
    @Published var showLogin = false
    
    private let apiClient = CursorAPIClient()
    
    func login(apiKey: String) async {
        do {
            let response = try await apiClient.login(apiKey: apiKey)
            await MainActor.run {
                self.isAuthenticated = true
                self.showLogin = false
            }
            
            // Start CLI after login
            try await startCLI()
        } catch {
            print("Login failed: \(error)")
        }
    }
    
    func startCLI() async throws {
        let response = try await apiClient.startCLI()
        await MainActor.run {
            self.cliStatus = response.status
        }
    }
    
    func sendMessage(_ text: String) async {
        let message = ChatMessage(id: UUID(), text: text, isUser: true, timestamp: Date())
        await MainActor.run {
            self.messages.append(message)
        }
        
        do {
            let response = try await apiClient.sendMessage(text)
            let aiMessage = ChatMessage(
                id: UUID(),
                text: response.response,
                isUser: false,
                timestamp: Date()
            )
            await MainActor.run {
                self.messages.append(aiMessage)
            }
        } catch {
            print("Failed to send message: \(error)")
        }
    }
}

struct ChatMessage: Identifiable {
    let id: UUID
    let text: String
    let isUser: Bool
    let timestamp: Date
}
```

## 🔒 Security Considerations

### 1. API Key Storage
- **Never** store API keys in plain text
- Use iOS Keychain for secure storage
- Consider using biometric authentication

```swift
import Security

class KeychainManager {
    static func saveAPIKey(_ apiKey: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "CursorAPIKey",
            kSecValueData as String: apiKey.data(using: .utf8)!
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    static func getAPIKey() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "CursorAPIKey",
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        if status == errSecSuccess,
           let data = result as? Data,
           let apiKey = String(data: data, encoding: .utf8) {
            return apiKey
        }
        return nil
    }
}
```

### 2. Network Security
- Use HTTPS only
- Implement certificate pinning if needed
- Handle network errors gracefully

### 3. Session Management
- Implement automatic session refresh
- Handle expired sessions
- Clear sensitive data on app background

## 🚀 Testing

### 1. Test API Endpoints
```bash
# Test health endpoint
curl https://your-domain.com:5000/api/health

# Test login
curl -X POST https://your-domain.com:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key":"your_api_key"}'
```

### 2. Test iOS App
- Test on different iOS versions
- Test with poor network conditions
- Test background/foreground transitions
- Test memory pressure scenarios

## 📋 Checklist

- [ ] API server running on port 5000
- [ ] HTTPS enabled with valid certificate
- [ ] iOS app can authenticate
- [ ] CLI can be started/stopped
- [ ] Messages can be sent/received
- [ ] Error handling implemented
- [ ] Security measures in place
- [ ] Testing completed

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure CORS is properly configured in the API server
2. **Session Expired**: Implement automatic re-authentication
3. **Network Timeouts**: Add retry logic with exponential backoff
4. **Memory Issues**: Monitor memory usage and implement cleanup

### Debug Tips

- Use Charles Proxy or Proxyman to inspect network traffic
- Enable verbose logging in the API server
- Test with Postman before implementing in iOS
- Monitor server logs for errors

---

**Happy coding with your iOS app! 🚀**
