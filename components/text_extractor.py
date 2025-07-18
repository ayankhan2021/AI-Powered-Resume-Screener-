import PyPDF2
import docx
import streamlit as st
import io
from typing import Optional

class TextExtractor:
    """Extract text from various file formats"""
    
    @staticmethod
    def extract_from_pdf(file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_from_docx(file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_from_txt(file) -> str:
        """Extract text from TXT file"""
        try:
            return str(file.read(), "utf-8")
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    @classmethod
    def extract_text(cls, uploaded_file) -> Optional[str]:
        """Main method to extract text based on file type"""
        if uploaded_file is None:
            return None
        
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            return cls.extract_from_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return cls.extract_from_docx(uploaded_file)
        elif file_type == "text/plain":
            return cls.extract_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None