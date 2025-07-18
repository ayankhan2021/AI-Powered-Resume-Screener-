import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import time

class AuthManager:
    """Professional authentication manager for Four Corners Group"""
    
    def __init__(self):
        self.users_file = "data/users.json"
        self.sessions_file = "data/sessions.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure authentication data files exist"""
        os.makedirs("data", exist_ok=True)
        
        # Create default users file if it doesn't exist
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("fcg@2024"),
                    "role": "admin",
                    "full_name": "FCG Administrator",
                    "email": "admin@fourcornersgroup.com",
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                },
                "hr_manager": {
                    "password": self.hash_password("hr@fcg123"),
                    "role": "hr_manager",
                    "full_name": "HR Manager",
                    "email": "hr@fourcornersgroup.com",
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                }
            }
            self.save_users(default_users)
        
        # Create sessions file if it doesn't exist
        if not os.path.exists(self.sessions_file):
            self.save_sessions({})
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users: Dict):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_sessions(self) -> Dict:
        """Load sessions from JSON file"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_sessions(self, sessions: Dict):
        """Save sessions to JSON file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user credentials"""
        users = self.load_users()
        
        if username in users:
            user = users[username]
            if user['password'] == self.hash_password(password):
                # Update last login
                user['last_login'] = datetime.now().isoformat()
                users[username] = user
                self.save_users(users)
                
                return {
                    'username': username,
                    'role': user['role'],
                    'full_name': user['full_name'],
                    'email': user['email'],
                    'last_login': user['last_login']
                }
        
        return None
    
    def create_session(self, user_data: Dict) -> str:
        """Create a new session for authenticated user"""
        session_id = hashlib.sha256(f"{user_data['username']}{datetime.now()}".encode()).hexdigest()
        
        sessions = self.load_sessions()
        sessions[session_id] = {
            'user_data': user_data,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=8)).isoformat()
        }
        self.save_sessions(sessions)
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """Validate session and return user data if valid"""
        sessions = self.load_sessions()
        
        if session_id in sessions:
            session = sessions[session_id]
            expires_at = datetime.fromisoformat(session['expires_at'])
            
            if datetime.now() < expires_at:
                return session['user_data']
            else:
                # Session expired, remove it
                del sessions[session_id]
                self.save_sessions(sessions)
        
        return None
    
    def logout_user(self, session_id: str):
        """Logout user by removing session"""
        sessions = self.load_sessions()
        if session_id in sessions:
            del sessions[session_id]
            self.save_sessions(sessions)
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        users = self.load_users()
        
        if username in users:
            user = users[username]
            if user['password'] == self.hash_password(old_password):
                user['password'] = self.hash_password(new_password)
                users[username] = user
                self.save_users(users)
                return True
        
        return False
    
    def add_user(self, username: str, password: str, role: str, full_name: str, email: str) -> bool:
        """Add new user (admin only)"""
        users = self.load_users()
        
        if username not in users:
            users[username] = {
                'password': self.hash_password(password),
                'role': role,
                'full_name': full_name,
                'email': email,
                'created_at': datetime.now().isoformat(),
                'last_login': None
            }
            self.save_users(users)
            return True
        
        return False