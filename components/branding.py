import streamlit as st
import time
import base64
from typing import Optional

class FCGBranding:
    """Four Corners Group branding components"""
    
    @staticmethod
    def get_fcg_colors():
        """Get FCG brand colors"""
        return {
            'primary': '#2E7D32',      # Deep Green
            'secondary': '#66BB6A',     # Light Green
            'accent': '#FFD700',        # Gold
            'dark': '#1B5E20',          # Dark Green
            'light': '#E8F5E8',        # Very Light Green
            'text': '#2C3E50',          # Dark Gray
            'white': '#FFFFFF'
        }
    
    @staticmethod
    def inject_fcg_css():
        """Inject FCG custom CSS"""
        colors = FCGBranding.get_fcg_colors()
        
        st.markdown(f"""
        <style>
        /* FCG Color Scheme */
        :root {{
            --fcg-primary: {colors['primary']};
            --fcg-secondary: {colors['secondary']};
            --fcg-accent: {colors['accent']};
            --fcg-dark: {colors['dark']};
            --fcg-light: {colors['light']};
            --fcg-text: {colors['text']};
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Custom styling for FCG */
        .fcg-header {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .fcg-logo {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {colors['white']};
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        
        .fcg-subtitle {{
            font-size: 1.2rem;
            color: {colors['light']};
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .fcg-tagline {{
            font-size: 0.9rem;
            color: {colors['light']};
            text-align: center;
            font-style: italic;
        }}
        
        .login-container {{
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: transparent;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            border: 1px solid {colors['light']};
        }}
        
        .login-header {{
            text-align: center;
            margin-top: -71px;
            margin-left: 30px;
            color: {colors['text']};    

        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: {colors['white']};
            border: none;
            border-radius: 5px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, {colors['dark']} 0%, {colors['primary']} 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        .loader-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 50vh;
        }}
        
        .fcg-loader {{
            width: 60px;
            height: 60px;
            border: 4px solid {colors['light']};
            border-top: 4px solid {colors['primary']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .status-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }}
        
        .status-online {{
            background: {colors['secondary']};
            color: {colors['white']};
        }}
        
        .status-admin {{
            background: {colors['accent']};
            color: {colors['dark']};
        }}
        
        .welcome-message {{
            background: {colors['dark']};
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid {colors['primary']};
            margin: 1rem 0;
            color: black;
        }}
        
        .footer-info {{
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            background: {colors['light']};
            border-radius: 5px;
            font-size: 0.8rem;
            color: {colors['text']};
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_fcg_header():
        """Display FCG branded header"""
        st.markdown("""
        <div style="display:none" class="fcg-header">
            
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_fcg_loader(message: str = "Loading..."):
        """Display FCG branded loader"""
        st.markdown(f"""
        <div class="loader-container">
            <div class="fcg-loader"></div>
            <p style="color: var(--fcg-text); font-weight: 600;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_welcome_message(user_data: dict):
        """Display welcome message for logged-in user"""
        role_badge = f'<span class="status-badge status-{"admin" if user_data["role"] == "admin" else "online"}">{user_data["role"].replace("_", " ").title()}</span>'
        
        st.markdown(f"""
        <div class="welcome-message">
            <h4>Welcome back, {user_data['full_name']}! {role_badge}</h4>
            <p><strong>Email:</strong> {user_data['email']}</p>
            <p><strong>Last Login:</strong> {user_data.get('last_login', 'First time login')}</p>
        </div>
        """, unsafe_allow_html=True)
