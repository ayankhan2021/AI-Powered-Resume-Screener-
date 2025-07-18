import spacy
import json
import re
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import textstat
import streamlit as st
from typing import Dict, List, Tuple
import numpy as np

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class JobMatchingAIAnalyzer:
    """AI analyzer that prioritizes job description matching"""
    
    def __init__(self):
        self.load_nlp_model()
        self.load_skills_database()
        self.setup_job_role_mappings()
    
    def load_nlp_model(self):
        """Load spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("spaCy model not found. Please install it using: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def load_skills_database(self):
        """Load skills database"""
        try:
            with open("data/skills_database.json", "r") as f:
                self.skills_db = json.load(f)
        except FileNotFoundError:
            st.error("Skills database not found. Using default skills.")
            self.skills_db = {
                "programming_languages": ["python", "java", "javascript", "c++", "c#", "php", "ruby", "swift"],
                "web_technologies": ["html", "css", "react", "angular", "vue.js", "node.js", "express.js"],
                "databases": ["mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle"],
                "cloud_platforms": ["aws", "azure", "google cloud", "heroku", "digitalocean"],
                "data_science": ["machine learning", "deep learning", "data science", "pandas", "numpy"],
                "market_research": ["market research", "consumer research", "survey design", "focus groups"],
                "business_consulting": ["business strategy", "strategic planning", "process improvement"],
                "soft_skills": ["leadership", "communication", "teamwork", "problem solving", "analytical thinking"]
            }
    
    def setup_job_role_mappings(self):
        """Setup job role to skill category mappings with weights"""
        self.job_role_weights = {
            "market research analyst": {
                "market_research": 0.40,
                "data_science": 0.25,
                "programming_languages": 0.15,
                "analytics_visualization": 0.10,
                "soft_skills": 0.10
            },
            "business consultant": {
                "business_consulting": 0.35,
                "market_research": 0.20,
                "project_management": 0.20,
                "soft_skills": 0.15,
                "industry_knowledge": 0.10
            },
            "data analyst": {
                "programming_languages": 0.30,
                "data_science": 0.25,
                "analytics_visualization": 0.20,
                "databases": 0.15,
                "soft_skills": 0.10
            },
            "training specialist": {
                "training_development": 0.40,
                "communication_tools": 0.20,
                "soft_skills": 0.20,
                "project_management": 0.10,
                "certifications": 0.10
            }
        }
    
    def extract_job_requirements(self, job_description: str) -> Dict[str, any]:
        """Extract detailed requirements from job description"""
        if not job_description:
            return {}
        
        job_text = job_description.lower()
        
        # Extract required skills
        required_skills = self.extract_skills_precise(job_description)
        
        # Extract experience requirements
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
            r'at\s*least\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)'
        ]
        
        required_years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, job_text)
            for match in matches:
                if isinstance(match, tuple):
                    required_years.extend([int(x) for x in match if x.isdigit()])
                else:
                    required_years.append(int(match))
        
        # Extract education requirements
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'graduation',
            'b.tech', 'm.tech', 'mba', 'bba', 'b.sc', 'm.sc'
        ]
        
        required_education = []
        for keyword in education_keywords:
            if keyword in job_text:
                required_education.append(keyword)
        
        # Extract key responsibilities and requirements
        requirement_sections = []
        if 'responsibilities' in job_text or 'duties' in job_text:
            requirement_sections.append('responsibilities')
        if 'requirements' in job_text or 'qualifications' in job_text:
            requirement_sections.append('requirements')
        if 'preferred' in job_text or 'nice to have' in job_text:
            requirement_sections.append('preferred')
        
        # Identify job role
        job_role = self.identify_job_role(job_description)
        
        return {
            "required_skills": required_skills,
            "required_years": max(required_years) if required_years else 0,
            "required_education": required_education,
            "job_role": job_role,
            "sections": requirement_sections,
            "priority_skills": self.get_priority_skills_for_role(job_role)
        }
    
    def get_priority_skills_for_role(self, job_role: str) -> List[str]:
        """Get priority skills for specific job roles"""
        priority_skills = {
            "market research analyst": [
                "market research", "statistical analysis", "survey design", "spss", "r", "python",
                "consumer research", "data analysis", "focus groups", "questionnaire design"
            ],
            "business consultant": [
                "business strategy", "strategic planning", "process improvement", "change management",
                "stakeholder management", "business analysis", "project management"
            ],
            "data analyst": [
                "python", "r", "sql", "tableau", "power bi", "excel", "statistical analysis",
                "data visualization", "machine learning", "predictive modeling"
            ],
            "training specialist": [
                "training design", "curriculum development", "e-learning", "instructional design",
                "adult learning", "facilitation", "presentation skills"
            ]
        }
        
        return priority_skills.get(job_role, [])
    
    def calculate_job_fit_score(self, resume_text: str, job_requirements: Dict) -> Dict[str, float]:
        """Calculate how well resume fits job requirements"""
        if not job_requirements:
            return {"overall_fit": 0, "skills_fit": 0, "experience_fit": 0, "education_fit": 0}
        
        # Extract resume information
        resume_skills = self.extract_skills_precise(resume_text)
        resume_experience = self.extract_experience_precise(resume_text)
        resume_education = self.extract_education_precise(resume_text)
        
        # Calculate skills fit
        skills_fit = self.calculate_skills_fit(resume_skills, job_requirements)
        
        # Calculate experience fit
        experience_fit = self.calculate_experience_fit(resume_experience, job_requirements)
        
        # Calculate education fit
        education_fit = self.calculate_education_fit(resume_education, job_requirements)
        
        # Calculate overall fit with job-specific weights
        job_role = job_requirements.get("job_role", "general")
        
        if job_role == "market research analyst":
            fit_weights = {"skills": 0.50, "experience": 0.30, "education": 0.20}
        elif job_role == "business consultant":
            fit_weights = {"skills": 0.45, "experience": 0.35, "education": 0.20}
        elif job_role == "data analyst":
            fit_weights = {"skills": 0.55, "experience": 0.25, "education": 0.20}
        else:
            fit_weights = {"skills": 0.50, "experience": 0.30, "education": 0.20}
        
        overall_fit = (
            skills_fit * fit_weights["skills"] +
            experience_fit * fit_weights["experience"] +
            education_fit * fit_weights["education"]
        )
        
        return {
            "overall_fit": round(overall_fit, 2),
            "skills_fit": round(skills_fit, 2),
            "experience_fit": round(experience_fit, 2),
            "education_fit": round(education_fit, 2),
            "fit_weights": fit_weights
        }
    
    def calculate_skills_fit(self, resume_skills: Dict, job_requirements: Dict) -> float:
        """Calculate how well resume skills match job requirements"""
        required_skills = job_requirements.get("required_skills", {})
        priority_skills = job_requirements.get("priority_skills", [])
        
        if not required_skills and not priority_skills:
            return 50  # Neutral score if no requirements
        
        total_score = 0
        total_weight = 0
        
        # Check required skills by category
        for category, req_skills in required_skills.items():
            if req_skills:  # Only if there are required skills in this category
                resume_cat_skills = set(resume_skills.get(category, []))
                req_cat_skills = set(req_skills)
                
                if req_cat_skills:
                    match_ratio = len(resume_cat_skills.intersection(req_cat_skills)) / len(req_cat_skills)
                    category_weight = self.job_role_weights.get(
                        job_requirements.get("job_role", "general"), {}
                    ).get(category, 0.1)
                    
                    total_score += match_ratio * 100 * category_weight
                    total_weight += category_weight
        
        # Check priority skills
        if priority_skills:
            all_resume_skills = []
            for skills_list in resume_skills.values():
                all_resume_skills.extend([skill.lower() for skill in skills_list])
            
            priority_matches = 0
            for priority_skill in priority_skills:
                if priority_skill.lower() in all_resume_skills:
                    priority_matches += 1
            
            if priority_skills:
                priority_score = (priority_matches / len(priority_skills)) * 100
                total_score += priority_score * 0.3  # 30% weight for priority skills
                total_weight += 0.3
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def calculate_experience_fit(self, resume_experience: Dict, job_requirements: Dict) -> float:
        """Calculate experience fit"""
        required_years = job_requirements.get("required_years", 0)
        resume_years = resume_experience.get("max_years", 0)
        
        if required_years == 0:
            return 75  # Neutral score if no experience requirement
        
        if resume_years >= required_years:
            return 100  # Perfect fit
        elif resume_years >= required_years * 0.8:
            return 80   # Close fit
        elif resume_years >= required_years * 0.6:
            return 60   # Acceptable fit
        elif resume_years >= required_years * 0.4:
            return 40   # Below requirements
        else:
            return 20   # Significantly below requirements
    
    def calculate_education_fit(self, resume_education: Dict, job_requirements: Dict) -> float:
        """Calculate education fit"""
        required_education = job_requirements.get("required_education", [])
        resume_degrees = [degree.lower() for degree in resume_education.get("degrees", [])]
        
        if not required_education:
            return 75  # Neutral score if no education requirement
        
        # Check for degree level matches
        education_score = 0
        for req_edu in required_education:
            req_edu_lower = req_edu.lower()
            
            if req_edu_lower in resume_degrees:
                education_score = 100
                break
            elif 'master' in req_edu_lower and any('master' in deg or 'mba' in deg for deg in resume_degrees):
                education_score = 100
                break
            elif 'bachelor' in req_edu_lower and any('bachelor' in deg or 'b.' in deg for deg in resume_degrees):
                education_score = 90
                break
            elif any(word in resume_degrees for word in req_edu_lower.split()):
                education_score = max(education_score, 70)
        
        return education_score if education_score > 0 else 30
    
    def extract_skills_precise(self, text: str) -> Dict[str, List[str]]:
        """Precise skill extraction with strict matching"""
        text_lower = text.lower()
        text_normalized = ' '.join(text_lower.split())
        
        extracted_skills = {}
        
        for category, skills in self.skills_db.items():
            found_skills = []
            
            for skill in skills:
                skill_lower = skill.lower()
                
                # Exact phrase matching
                if skill_lower in text_normalized:
                    found_skills.append(skill)
                    continue
                
                # Word boundary matching for single words
                if len(skill_lower.split()) == 1:
                    pattern = r'\b' + re.escape(skill_lower) + r'\b'
                    if re.search(pattern, text_normalized):
                        found_skills.append(skill)
                        continue
                
                # Multi-word skills
                if len(skill_lower.split()) > 1:
                    skill_pattern = r'\b' + r'\s+'.join([re.escape(word) for word in skill_lower.split()]) + r'\b'
                    if re.search(skill_pattern, text_normalized):
                        found_skills.append(skill)
            
            extracted_skills[category] = list(set(found_skills))
        
        return extracted_skills
    
    def extract_experience_precise(self, text: str) -> Dict[str, any]:
        """Precise experience extraction"""
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)(?:\s|$|[.,])',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)(?:\s|$|[.,])',
            r'over\s*(\d+)\s*(?:years?|yrs?)(?:\s|$|[.,])',
            r'more\s*than\s*(\d+)\s*(?:years?|yrs?)(?:\s|$|[.,])'
        ]
        
        years_found = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if isinstance(match, tuple):
                    years_found.extend([int(x) for x in match if x.isdigit()])
                else:
                    years_found.append(int(match))
        
        max_years = max(years_found) if years_found else 0
        
        return {
            "years_experience": years_found,
            "max_years": max_years,
            "experience_score": min(max_years * 15, 100)
        }
    
    def extract_education_precise(self, text: str) -> Dict[str, any]:
        """Precise education extraction"""
        degree_patterns = [
            r'\b(bachelor|master|phd|doctorate|diploma|certificate)\b',
            r'\b(b\.?tech|m\.?tech|b\.?sc|m\.?sc|mba|bba|b\.?com|m\.?com|be|me)\b',
            r'\b(engineering|computer science|information technology|statistics|mathematics|business administration)\b'
        ]
        
        degrees = []
        for pattern in degree_patterns:
            matches = re.findall(pattern, text.lower())
            degrees.extend(matches)
        
        return {
            "degrees": list(set(degrees)),
            "education_score": 50 if degrees else 0
        }
    
    def identify_job_role(self, text: str) -> str:
        """Identify job role from text"""
        text_lower = text.lower()
        
        role_keywords = {
            "market research analyst": ["market research", "consumer research", "research analyst", "market analyst"],
            "business consultant": ["business consultant", "strategy consultant", "management consultant", "consulting"],
            "data analyst": ["data analyst", "business analyst", "analytics", "data science"],
            "training specialist": ["training specialist", "trainer", "learning specialist", "instructional designer"]
        }
        
        for role, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return role
        
        return "general"
    
    def calculate_resume_score(self, resume_text: str, job_description: str = "", job_title: str = "") -> Dict[str, any]:
        """Calculate comprehensive resume score with job matching priority"""
        
        # Extract job requirements if job description is provided
        job_requirements = self.extract_job_requirements(job_description) if job_description else {}
        
        # Extract resume information
        skills = self.extract_skills_precise(resume_text)
        experience = self.extract_experience_precise(resume_text)
        education = self.extract_education_precise(resume_text)
        
        # Calculate job fit score
        job_fit = self.calculate_job_fit_score(resume_text, job_requirements)
        
        # Calculate individual scores
        skills_score = min(sum(len(skill_list) for skill_list in skills.values()) * 5, 100)
        experience_score = experience["experience_score"]
        education_score = education["education_score"]
        readability_score = max(0, textstat.flesch_reading_ease(resume_text))
        
        # Determine scoring weights based on whether job description is provided
        if job_description:
            # When job description is provided, prioritize job fit
            weights = {
                "job_fit": 0.50,      # 50% weight for job matching
                "skills": 0.20,       # 20% for general skills
                "experience": 0.15,   # 15% for experience
                "education": 0.10,    # 10% for education
                "readability": 0.05   # 5% for readability
            }
            
            scores = {
                "job_fit": job_fit["overall_fit"],
                "skills": skills_score,
                "experience": experience_score,
                "education": education_score,
                "readability": min(readability_score, 100)
            }
        else:
            # When no job description, use general scoring
            weights = {
                "skills": 0.35,
                "experience": 0.25,
                "education": 0.20,
                "readability": 0.20
            }
            
            scores = {
                "skills": skills_score,
                "experience": experience_score,
                "education": education_score,
                "readability": min(readability_score, 100)
            }
        
        # Calculate weighted overall score
        overall_score = sum(scores[key] * weights[key] for key in scores.keys())
        
        return {
            "overall_score": round(overall_score, 2),
            "detailed_scores": scores,
            "job_fit_analysis": job_fit,
            "skills_found": skills,
            "experience_info": experience,
            "education_info": education,
            "total_skills_count": sum(len(skill_list) for skill_list in skills.values()),
            "job_role_identified": job_requirements.get("job_role", "general"),
            "scoring_weights": weights,
            "job_requirements": job_requirements
        }
    
    def get_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate job-specific recommendations"""
        recommendations = []
        scores = analysis_result["detailed_scores"]
        job_fit = analysis_result.get("job_fit_analysis", {})
        job_requirements = analysis_result.get("job_requirements", {})
        
        # Job fit recommendations
        if job_fit.get("overall_fit", 0) < 70:
            recommendations.append("🎯 Improve job fit by adding skills and experience mentioned in the job description")
        
        if job_fit.get("skills_fit", 0) < 60:
            priority_skills = job_requirements.get("priority_skills", [])
            if priority_skills:
                missing_skills = priority_skills[:3]  # Show top 3 missing skills
                recommendations.append(f"🔧 Add these key skills: {', '.join(missing_skills)}")
        
        if job_fit.get("experience_fit", 0) < 70:
            required_years = job_requirements.get("required_years", 0)
            if required_years > 0:
                recommendations.append(f"💼 Highlight {required_years}+ years of relevant experience or related projects")
        
        # General recommendations
        if scores.get("skills", 0) < 60:
            recommendations.append("🛠️ Expand your technical skills portfolio")
        
        if scores.get("experience", 0) < 50:
            recommendations.append("📈 Add more detailed work experience with quantifiable achievements")
        
        if not recommendations:
            recommendations.append("✅ Excellent match for this position!")
        
        return recommendations