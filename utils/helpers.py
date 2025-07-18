import streamlit as st
import json
from typing import Dict, List, Any
import plotly.graph_objects as go
import pandas as pd
import os

class SessionManager:
    """Manage session state for the application"""
    
    @staticmethod
    def init_session_state():
        """Initialize session state variables"""
        if 'analyzed_resumes' not in st.session_state:
            st.session_state.analyzed_resumes = []
        
        if 'current_job_description' not in st.session_state:
            st.session_state.current_job_description = ""
        
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
    
    @staticmethod
    def add_analysis_to_history(analysis_result: Dict, filename: str):
        """Add analysis result to history"""
        history_item = {
            'filename': filename,
            'timestamp': str(pd.Timestamp.now()),
            'analysis': analysis_result
        }
        st.session_state.analysis_history.append(history_item)
        
        # Keep only last 10 analyses
        if len(st.session_state.analysis_history) > 10:
            st.session_state.analysis_history = st.session_state.analysis_history[-10:]

class FileValidator:
    """Validate uploaded files"""
    
    ALLOWED_EXTENSIONS = ['pdf', 'docx', 'txt']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_file(cls, uploaded_file) -> tuple[bool, str]:
        """Validate uploaded file"""
        if uploaded_file is None:
            return False, "No file uploaded"
        
        # Check file size
        if uploaded_file.size > cls.MAX_FILE_SIZE:
            return False, f"File size exceeds {cls.MAX_FILE_SIZE/(1024*1024):.1f}MB limit"
        
        # Check file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type. Allowed: {', '.join(cls.ALLOWED_EXTENSIONS)}"
        
        return True, "File is valid"

class ConfigManager:
    """Manage application configuration"""
    
    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        default_config = {
            'app_title': 'AI Resume Screener',
            'max_files_batch': 5,
            'score_thresholds': {
                'excellent': 85,
                'good': 70,
                'average': 50,
                'poor': 30
            }
        }
        
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
        except:
            pass
        
        return default_config

def format_score_color(score: float) -> str:
    """Return color based on score"""
    if score >= 85:
        return "green"
    elif score >= 70:
        return "orange"
    elif score >= 50:
        return "yellow"
    else:
        return "red"

def create_download_link(data: Dict, filename: str) -> str:
    """Create download link for analysis results"""
    json_data = json.dumps(data, indent=2)
    return f'<a href="data:application/json;base64,{json_data}" download="{filename}">Download Analysis Results</a>'