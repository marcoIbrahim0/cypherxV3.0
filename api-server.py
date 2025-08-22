#!/usr/bin/env python3
"""
Cursor CLI API Server for iOS App
Provides REST endpoints to interact with the Cursor headless CLI
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import subprocess
import json
import os
import threading
import time
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SESSION_TYPE'] = 'filesystem'

# Enable CORS for iOS app
CORS(app, supports_credentials=True)

# Store active CLI sessions
active_sessions = {}

class CursorCLISession:
    def __init__(self, session_id, api_key):
        self.session_id = session_id
        self.api_key = api_key
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.process = None
        self.status = "created"
        self.current_model = "gpt-4"  # Default model
        self.available_models = [
            "gpt-4",
            "gpt-4-turbo", 
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-3.5-turbo",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
            "gemini-pro",
            "gemini-flash"
        ]
        
    def start_cli(self):
        """Start the Cursor CLI process"""
        try:
            env = os.environ.copy()
            env['CURSOR_API_KEY'] = self.api_key
            
            # Start cursor-agent in background
            self.process = subprocess.Popen(
                ['cursor-agent'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.status = "running"
            self.last_activity = datetime.now()
            logger.info(f"Started CLI session {self.session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to start CLI: {e}")
            self.status = "error"
            return False
    
    def stop_cli(self):
        """Stop the Cursor CLI process"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.status = "stopped"
            self.last_activity = datetime.now()
            logger.info(f"Stopped CLI session {self.session_id}")
    
    def change_model(self, new_model):
        """Change the AI model for this session"""
        if new_model not in self.available_models:
            return False, f"Model '{new_model}' not available. Available models: {', '.join(self.available_models)}"
        
        self.current_model = new_model
        self.last_activity = datetime.now()
        logger.info(f"Changed model to {new_model} for session {self.session_id}")
        return True, f"Model changed to {new_model}"
    
    def get_model_info(self):
        """Get current model and available models"""
        return {
            'current_model': self.current_model,
            'available_models': self.available_models
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(active_sessions)
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate with API key and create session"""
    data = request.get_json()
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 400
    
    # Validate API key format (basic check)
    if len(api_key) < 20:
        return jsonify({'error': 'Invalid API key format'}), 400
    
    # Create session
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    
    # Store session
    active_sessions[session_id] = CursorCLISession(session_id, api_key)
    
    return jsonify({
        'session_id': session_id,
        'status': 'authenticated',
        'message': 'Login successful'
    })

@app.route('/api/cli/start', methods=['POST'])
def start_cli():
    """Start the Cursor CLI for the current session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cli_session = active_sessions[session_id]
    
    if cli_session.status == "running":
        return jsonify({'message': 'CLI already running', 'status': 'running'})
    
    success = cli_session.start_cli()
    if success:
        return jsonify({
            'message': 'CLI started successfully',
            'status': 'running',
            'session_id': session_id
        })
    else:
        return jsonify({'error': 'Failed to start CLI'}), 500

@app.route('/api/cli/status', methods=['GET'])
def cli_status():
    """Get CLI status for current session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cli_session = active_sessions[session_id]
    
    return jsonify({
        'session_id': session_id,
        'status': cli_session.status,
        'created_at': cli_session.created_at.isoformat(),
        'last_activity': cli_session.last_activity.isoformat(),
        'uptime': (datetime.now() - cli_session.created_at).total_seconds() if cli_session.created_at else 0,
        'current_model': cli_session.current_model
    })

@app.route('/api/cli/stop', methods=['POST'])
def stop_cli():
    """Stop the Cursor CLI for current session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cli_session = active_sessions[session_id]
    cli_session.stop_cli()
    
    return jsonify({
        'message': 'CLI stopped successfully',
        'status': 'stopped'
    })

@app.route('/api/cli/chat', methods=['POST'])
def chat_with_cli():
    """Send a message to the Cursor CLI"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    cli_session = active_sessions[session_id]
    
    if cli_session.status != "running":
        return jsonify({'error': 'CLI not running'}), 400
    
    # Update activity
    cli_session.last_activity = datetime.now()
    
    # For now, return a mock response
    # In a real implementation, you'd communicate with the CLI process
    return jsonify({
        'message': 'Message received',
        'response': f'CLI received: {message}',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions (admin only)"""
    return jsonify({
        'sessions': [
            {
                'session_id': s.session_id,
                'status': s.status,
                'created_at': s.created_at.isoformat(),
                'last_activity': s.last_activity.isoformat(),
                'current_model': s.current_model
            }
            for s in active_sessions.values()
        ]
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models and current model for the session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cli_session = active_sessions[session_id]
    return jsonify(cli_session.get_model_info())

@app.route('/api/models/change', methods=['POST'])
def change_model():
    """Change the AI model for the current session"""
    session_id = session.get('session_id')
    if not session_id or session_id not in active_sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    new_model = data.get('model')
    
    if not new_model:
        return jsonify({'error': 'Model parameter required'}), 400
    
    cli_session = active_sessions[session_id]
    success, message = cli_session.change_model(new_model)
    
    if success:
        return jsonify({
            'message': message,
            'current_model': cli_session.current_model,
            'available_models': cli_session.available_models
        })
    else:
        return jsonify({'error': message}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout and clean up session"""
    session_id = session.get('session_id')
    if session_id and session_id in active_sessions:
        cli_session = active_sessions[session_id]
        cli_session.stop_cli()
        del active_sessions[session_id]
    
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# Cleanup old sessions periodically
def cleanup_sessions():
    """Clean up inactive sessions"""
    while True:
        time.sleep(300)  # Check every 5 minutes
        current_time = datetime.now()
        
        sessions_to_remove = []
        for session_id, cli_session in active_sessions.items():
            # Remove sessions older than 1 hour
            if (current_time - cli_session.last_activity).total_seconds() > 3600:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            cli_session = active_sessions[session_id]
            cli_session.stop_cli()
            del active_sessions[session_id]
            logger.info(f"Cleaned up inactive session {session_id}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
