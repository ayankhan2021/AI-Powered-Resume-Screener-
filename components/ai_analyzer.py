import spacy
import json
import re
import nltk
import streamlit as st
import textstat
import numpy as np
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

class ProfessionalAIAnalyzer:
    """
    Professional AI CV Analyzer with contextual relevance scoring.
    Prioritizes job-specific fit and gives bonus points for role alignment.
    """
    
    def __init__(self):
        self.load_nlp_model()
        self.load_comprehensive_skills_database()
        self.setup_industry_mappings()
        self.setup_contextual_analyzers()
        self.setup_human_like_scoring()
        self.setup_contextual_bonus_system() 
        
    def load_nlp_model(self):
        """Load advanced spaCy model with entity recognition"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("spaCy model not found. Please install it using: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def load_comprehensive_skills_database(self):
        """Load comprehensive skills database with contextual understanding for ALL job types"""
        try:
            with open("data/skills_database.json", "r") as f:
                self.skills_db = json.load(f)
        except FileNotFoundError:
            # MASSIVE comprehensive skills database covering ALL job types
            self.skills_db = {
                # Programming & Technical Skills
                "programming_languages": {
                    "web_development": ["javascript", "typescript", "html", "css", "php", "ruby", "node.js"],
                    "backend": ["python", "java", "c#", "c++", "go", "rust", "scala", "kotlin", "asp.net"],
                    "mobile": ["swift", "objective-c", "dart", "flutter", "react native", "xamarin", "ionic"],
                    "data_science": ["python", "r", "matlab", "julia", "sql", "sas", "spss", "stata"],
                    "systems": ["c", "c++", "assembly", "verilog", "vhdl", "embedded c", "arduino"],
                    "scripting": ["bash", "powershell", "perl", "lua", "tcl", "awk", "sed"]
                },
                "web_technologies": {
                    "frontend_frameworks": ["react", "angular", "vue.js", "svelte", "ember.js", "backbone.js"],
                    "backend_frameworks": ["django", "flask", "express.js", "spring", "laravel", "rails", "fastapi"],
                    "css_frameworks": ["bootstrap", "tailwind", "bulma", "foundation", "materialize"],
                    "build_tools": ["webpack", "gulp", "grunt", "parcel", "vite", "rollup", "esbuild"],
                    "cms": ["wordpress", "drupal", "joomla", "strapi", "contentful", "sanity"]
                },
                "databases": {
                    "relational": ["mysql", "postgresql", "sqlite", "oracle", "sql server", "mariadb"],
                    "nosql": ["mongodb", "redis", "cassandra", "dynamodb", "couchdb", "firebase"],
                    "graph": ["neo4j", "amazon neptune", "arangodb", "dgraph"],
                    "time_series": ["influxdb", "timescaledb", "prometheus", "clickhouse"],
                    "data_warehousing": ["snowflake", "redshift", "bigquery", "synapse", "teradata"]
                },
                "cloud_platforms": {
                    "aws": ["ec2", "s3", "lambda", "rds", "cloudformation", "eks", "ecs", "sagemaker"],
                    "azure": ["azure functions", "blob storage", "cosmos db", "aks", "azure ml", "power platform"],
                    "gcp": ["compute engine", "cloud storage", "bigquery", "gke", "cloud functions", "vertex ai"],
                    "general": ["docker", "kubernetes", "terraform", "ansible", "vagrant", "helm"],
                    "devops": ["jenkins", "gitlab ci", "github actions", "travis ci", "circleci", "teamcity"]
                },

                # Culinary & Food Service Skills
                "culinary_skills": {
                    "cooking_techniques": ["grilling", "roasting", "sautéing", "braising", "poaching", "frying", "steaming", "baking", "broiling", "smoking", "sous vide", "confit", "flambé"],
                    "cuisine_types": ["italian", "french", "asian", "mexican", "mediterranean", "american", "indian", "thai", "chinese", "japanese", "korean", "middle eastern", "fusion"],
                    "food_preparation": ["knife skills", "food prep", "mise en place", "plating", "garnishing", "portioning", "butchery", "filleting", "vegetable carving"],
                    "kitchen_management": ["inventory", "cost control", "menu planning", "kitchen safety", "sanitation", "haccp", "food ordering", "staff scheduling", "quality control"],
                    "specialized_skills": ["pastry", "bread making", "wine pairing", "molecular gastronomy", "farm to table", "organic cooking", "dietary restrictions", "allergen management"],
                    "baking_pastry": ["bread making", "cake decorating", "pastry arts", "chocolate work", "sugar work", "lamination", "fermentation", "artisan breads"],
                    "beverage": ["coffee preparation", "tea blending", "cocktail mixing", "wine service", "beer knowledge", "spirits knowledge", "barista skills"],
                    "dietary_specializations": ["vegan cooking", "vegetarian", "gluten-free", "keto", "paleo", "diabetic-friendly", "halal", "kosher", "raw food"]
                },

                # Healthcare & Medical Skills
                "healthcare_skills": {
                    "clinical": ["patient care", "vital signs", "medication administration", "wound care", "iv therapy", "injections", "blood draws"],
                    "diagnostic": ["x-ray", "mri", "ct scan", "ultrasound", "blood work", "ecg", "ekg", "spirometry"],
                    "specialties": ["emergency medicine", "pediatrics", "cardiology", "oncology", "surgery", "anesthesia", "psychiatry", "dermatology"],
                    "certifications": ["cpr", "bls", "acls", "pals", "cna", "rn", "lpn", "nrp", "tncc"],
                    "nursing": ["bedside manner", "patient assessment", "care planning", "documentation", "family education", "discharge planning"],
                    "medical_admin": ["medical coding", "icd-10", "cpt codes", "insurance verification", "emr systems", "epic", "cerner"],
                    "laboratory": ["phlebotomy", "lab testing", "specimen collection", "microscopy", "blood bank", "microbiology"],
                    "therapy": ["physical therapy", "occupational therapy", "speech therapy", "respiratory therapy", "massage therapy"]
                },

                # Creative & Entertainment
                "creative_arts": {
                    "music": ["singing", "vocal performance", "music theory", "composition", "live performance", "stage presence", "pitch control"],
                    "performance": ["stage presence", "audience engagement", "entertainment", "acting", "dancing", "comedy", "storytelling"],
                    "production": ["studio recording", "audio production", "mixing", "mastering", "sound engineering", "music production"],
                    "instruments": ["guitar", "piano", "drums", "violin", "saxophone", "bass", "keyboard", "flute", "trumpet"],
                    "genres": ["pop", "rock", "jazz", "classical", "country", "r&b", "hip hop", "folk", "blues", "electronic"],
                    "visual_arts": ["painting", "drawing", "sculpture", "photography", "graphic design", "illustration", "digital art"],
                    "design": ["ui/ux design", "web design", "logo design", "branding", "typography", "color theory", "adobe creative suite"],
                    "video": ["video editing", "cinematography", "animation", "motion graphics", "after effects", "premiere pro"]
                },

                # Business & Finance
                "business_finance": {
                    "accounting": ["bookkeeping", "financial statements", "tax preparation", "auditing", "accounts payable", "accounts receivable", "payroll"],
                    "analysis": ["financial analysis", "budget planning", "forecasting", "cost analysis", "roi analysis", "variance analysis", "ratio analysis"],
                    "tools": ["excel", "quickbooks", "sap", "oracle", "bloomberg", "sage", "xero", "freshbooks"],
                    "certifications": ["cpa", "cfa", "frm", "cma", "cia", "acca", "ca", "cga"],
                    "banking": ["commercial banking", "investment banking", "retail banking", "credit analysis", "loan processing", "risk management"],
                    "insurance": ["underwriting", "claims processing", "actuarial analysis", "risk assessment", "policy administration"],
                    "investments": ["portfolio management", "equity research", "fixed income", "derivatives", "asset management", "wealth management"]
                },

                # Sales & Marketing
                "sales_marketing": {
                    "sales": ["lead generation", "cold calling", "client relationships", "closing deals", "crm", "b2b sales", "b2c sales", "inside sales"],
                    "digital_marketing": ["seo", "sem", "social media", "content marketing", "email marketing", "ppc", "google ads", "facebook ads"],
                    "traditional_marketing": ["print advertising", "radio", "tv", "outdoor advertising", "events", "trade shows", "direct mail"],
                    "analytics": ["google analytics", "facebook insights", "conversion tracking", "a/b testing", "marketing automation"],
                    "brand_management": ["brand strategy", "brand positioning", "brand awareness", "brand equity", "corporate identity"],
                    "public_relations": ["media relations", "press releases", "crisis communication", "event planning", "corporate communications"],
                    "e_commerce": ["shopify", "magento", "woocommerce", "amazon fba", "dropshipping", "marketplace management"]
                },

                # Education & Training
                "education_skills": {
                    "teaching": ["lesson planning", "curriculum development", "classroom management", "assessment", "differentiated instruction"],
                    "training": ["corporate training", "skill development", "workshop facilitation", "e-learning", "instructional design"],
                    "specialties": ["special education", "esl", "stem", "arts education", "adult education", "early childhood"],
                    "technology": ["learning management systems", "educational technology", "online teaching", "virtual classrooms"],
                    "administration": ["school administration", "educational leadership", "policy development", "budget management"],
                    "counseling": ["academic counseling", "career guidance", "student support", "behavioral intervention"]
                },

                # Manufacturing & Engineering
                "manufacturing_engineering": {
                    "mechanical": ["mechanical engineering", "cad design", "autocad", "solidworks", "manufacturing processes", "quality control"],
                    "electrical": ["electrical engineering", "circuit design", "plc programming", "automation", "control systems"],
                    "industrial": ["industrial engineering", "process optimization", "lean manufacturing", "six sigma", "operations research"],
                    "civil": ["civil engineering", "structural design", "construction management", "project planning", "surveying"],
                    "chemical": ["chemical engineering", "process engineering", "chemical processes", "safety protocols"],
                    "production": ["production planning", "inventory management", "supply chain", "logistics", "warehouse management"],
                    "quality": ["quality assurance", "iso standards", "statistical process control", "inspection", "testing"]
                },

                # Legal & Compliance
                "legal_skills": {
                    "practice_areas": ["corporate law", "criminal law", "family law", "real estate law", "intellectual property", "employment law"],
                    "litigation": ["trial advocacy", "legal research", "brief writing", "depositions", "negotiations", "mediation"],
                    "compliance": ["regulatory compliance", "risk management", "policy development", "audit", "governance"],
                    "documentation": ["contract drafting", "legal writing", "case management", "document review"],
                    "paralegal": ["legal assistant", "case preparation", "client communication", "filing", "research support"]
                },

                # Transportation & Logistics
                "transportation_logistics": {
                    "driving": ["commercial driving", "cdl", "truck driving", "delivery services", "route planning", "vehicle maintenance"],
                    "logistics": ["supply chain management", "inventory control", "warehouse operations", "shipping", "receiving"],
                    "aviation": ["pilot license", "air traffic control", "aircraft maintenance", "flight operations", "aviation safety"],
                    "maritime": ["ship operations", "navigation", "marine engineering", "port operations", "maritime safety"],
                    "public_transport": ["bus driving", "train operations", "transit planning", "passenger service"]
                },

                # Agriculture & Environment
                "agriculture_environment": {
                    "farming": ["crop management", "livestock care", "irrigation", "pest control", "organic farming", "sustainable agriculture"],
                    "environmental": ["environmental science", "conservation", "sustainability", "waste management", "renewable energy"],
                    "forestry": ["forest management", "timber harvesting", "wildlife conservation", "fire prevention"],
                    "veterinary": ["animal care", "veterinary medicine", "animal behavior", "pet grooming", "animal training"]
                },

                # Security & Safety
                "security_safety": {
                    "security": ["physical security", "cybersecurity", "surveillance", "access control", "security protocols", "risk assessment"],
                    "law_enforcement": ["police work", "criminal investigation", "forensics", "emergency response", "public safety"],
                    "fire_safety": ["firefighting", "fire prevention", "emergency medical services", "hazmat response", "rescue operations"],
                    "occupational_safety": ["workplace safety", "osha compliance", "safety training", "accident investigation", "safety audits"]
                },

                # Real Estate & Construction
                "real_estate_construction": {
                    "real_estate": ["property management", "real estate sales", "property valuation", "leasing", "real estate investment"],
                    "construction": ["construction management", "carpentry", "plumbing", "electrical work", "masonry", "roofing"],
                    "architecture": ["architectural design", "building codes", "construction drawings", "project management"],
                    "trades": ["welding", "painting", "flooring", "hvac", "landscaping", "demolition"]
                },

                # Hospitality & Tourism
                "hospitality_tourism": {
                    "hotel_management": ["front desk operations", "housekeeping", "concierge services", "revenue management", "guest relations"],
                    "food_service": ["restaurant management", "catering", "banquet services", "menu planning", "cost control"],
                    "tourism": ["tour guide", "travel planning", "destination management", "cultural interpretation", "language skills"],
                    "event_planning": ["event coordination", "wedding planning", "corporate events", "vendor management", "budget planning"]
                },

                # Sports & Recreation
                "sports_recreation": {
                    "coaching": ["sports coaching", "athletic training", "fitness instruction", "team management", "player development"],
                    "fitness": ["personal training", "group fitness", "yoga instruction", "nutrition counseling", "exercise physiology"],
                    "sports_specific": ["football", "basketball", "soccer", "tennis", "swimming", "track and field", "martial arts"],
                    "recreation": ["camp counseling", "outdoor recreation", "adventure sports", "community recreation"]
                },

                # Retail & Customer Service
                "retail_customer_service": {
                    "retail": ["retail sales", "merchandising", "inventory management", "pos systems", "visual merchandising"],
                    "customer_service": ["call center", "customer support", "complaint resolution", "phone etiquette", "chat support"],
                    "cashier": ["cash handling", "payment processing", "register operations", "money counting", "transaction processing"]
                },

                # Human Resources
                "human_resources": {
                    "recruiting": ["talent acquisition", "interviewing", "candidate screening", "job posting", "background checks"],
                    "hr_operations": ["payroll", "benefits administration", "employee relations", "policy development", "compliance"],
                    "training": ["employee training", "onboarding", "performance management", "career development", "succession planning"],
                    "compensation": ["compensation analysis", "salary surveys", "job evaluation", "incentive programs"]
                },

                # Data Science & Analytics
                "data_science": {
                    "machine_learning": ["scikit-learn", "tensorflow", "pytorch", "keras", "xgboost", "neural networks", "deep learning"],
                    "data_analysis": ["pandas", "numpy", "scipy", "matplotlib", "seaborn", "statistical analysis", "hypothesis testing"],
                    "visualization": ["tableau", "power bi", "d3.js", "plotly", "ggplot2", "qlik", "looker"],
                    "big_data": ["hadoop", "spark", "kafka", "airflow", "databricks", "hive", "pig"],
                    "statistics": ["regression", "classification", "clustering", "time series", "bayesian analysis", "experimental design"],
                    "business_intelligence": ["data warehousing", "etl", "reporting", "dashboards", "kpi development"]
                },

                # Market Research & Analysis
                "market_research": {
                    "quantitative": ["statistical analysis", "survey design", "a/b testing", "regression analysis", "conjoint analysis"],
                    "qualitative": ["ethnographic research", "user research", "behavioral analysis", "focus groups", "interviews"],
                    "tools": ["qualtrics", "surveymonkey", "usertesting", "hotjar", "spss", "sas", "stata"],
                    "methodologies": ["market segmentation", "brand tracking", "customer satisfaction", "pricing research", "concept testing"],
                    "digital_research": ["social media monitoring", "web analytics", "seo research", "competitive intelligence"],
                    "consumer_insights": ["consumer behavior", "purchase intent", "brand perception", "customer journey mapping"]
                },

                # Business Consulting
                "business_consulting": {
                    "strategy": ["business strategy", "strategic planning", "competitive analysis", "market entry", "growth strategy"],
                    "operations": ["process improvement", "change management", "lean six sigma", "kaizen", "business process reengineering"],
                    "management": ["project management", "stakeholder management", "business analysis", "requirements gathering"],
                    "frameworks": ["mckinsey", "bcg", "swot analysis", "porter's five forces", "value chain analysis", "balanced scorecard"],
                    "digital_transformation": ["technology implementation", "digital strategy", "automation", "workflow optimization"],
                    "organizational": ["organizational design", "culture change", "leadership development", "team effectiveness"]
                },

                # Soft Skills with Context
                "soft_skills": {
                    "leadership": ["leadership", "team management", "mentoring", "coaching", "delegation", "vision setting"],
                    "communication": ["communication", "presentation", "public speaking", "writing", "negotiation", "active listening"],
                    "analytical": ["problem solving", "analytical thinking", "critical thinking", "decision making", "research skills"],
                    "interpersonal": ["teamwork", "collaboration", "empathy", "emotional intelligence", "cultural sensitivity"],
                    "adaptability": ["flexibility", "adaptability", "learning agility", "innovation", "change management"],
                    "time_management": ["prioritization", "multitasking", "deadline management", "efficiency", "productivity"],
                    "creativity": ["creative thinking", "innovation", "brainstorming", "design thinking", "artistic vision"]
                },

                # Languages & Communication
                "languages": {
                    "english": ["english", "business english", "technical writing", "academic english", "conversational english"],
                    "european": ["spanish", "french", "german", "italian", "portuguese", "dutch", "swedish", "norwegian"],
                    "asian": ["mandarin", "japanese", "korean", "hindi", "arabic", "thai", "vietnamese", "tagalog"],
                    "south_asian": ["urdu", "hindi", "bengali", "punjabi", "tamil", "gujarati", "marathi"],
                    "middle_eastern": ["arabic", "persian", "turkish", "hebrew", "kurdish"],
                    "african": ["swahili", "afrikaans", "amharic", "yoruba", "zulu"]
                },

                # Professional Certifications
                "certifications": {
                    "it": ["cissp", "cisa", "cism", "comptia", "cisco", "microsoft", "aws", "azure", "google cloud"],
                    "project_management": ["pmp", "prince2", "agile", "scrum master", "csm", "safe", "itil"],
                    "finance": ["cpa", "cfa", "frm", "cma", "cia", "acca", "ca"],
                    "marketing": ["google ads", "facebook blueprint", "hubspot", "salesforce", "marketo"],
                    "quality": ["six sigma", "lean", "iso", "cmmi", "cobit"],
                    "healthcare": ["cpr", "bls", "acls", "pals", "tncc", "ccrn"],
                    "real_estate": ["real estate license", "property management", "appraisal certification"]
                }
            }
    
    def setup_industry_mappings(self):
        """Enhanced industry mappings with contextual bonus factors for ALL job types"""
        self.industry_role_weights = {
            # Culinary & Food Service
            "chef": {
                "required_skills": ["culinary_skills"],
                "preferred_skills": ["soft_skills", "business_finance", "languages"],
                "weights": {"skills": 0.60, "experience": 0.25, "education": 0.10, "passion": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 40
            },
            "cook": {
                "required_skills": ["culinary_skills"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.55, "experience": 0.30, "education": 0.10, "reliability": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 35
            },
            "baker": {
                "required_skills": ["culinary_skills"],
                "preferred_skills": ["soft_skills", "business_finance"],
                "weights": {"skills": 0.65, "experience": 0.25, "education": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 40
            },
            "barista": {
                "required_skills": ["culinary_skills", "retail_customer_service"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "customer_service": 0.20},
                "contextual_bonus": 50,
                "minimum_threshold": 35
            },

            # Healthcare
            "nurse": {
                "required_skills": ["healthcare_skills"],
                "preferred_skills": ["soft_skills", "certifications"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "certifications": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },
            "doctor": {
                "required_skills": ["healthcare_skills"],
                "preferred_skills": ["soft_skills", "certifications"],
                "weights": {"skills": 0.45, "experience": 0.25, "education": 0.25, "certifications": 0.05},
                "contextual_bonus": 70,
                "minimum_threshold": 70
            },
            "medical_assistant": {
                "required_skills": ["healthcare_skills"],
                "preferred_skills": ["soft_skills", "retail_customer_service"],
                "weights": {"skills": 0.55, "experience": 0.25, "education": 0.15, "certification": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },
            "pharmacist": {
                "required_skills": ["healthcare_skills"],
                "preferred_skills": ["soft_skills", "retail_customer_service"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.20, "certification": 0.05},
                "contextual_bonus": 65,
                "minimum_threshold": 60
            },

            # Technology
            "software_engineer": {
                "required_skills": ["programming_languages", "databases"],
                "preferred_skills": ["cloud_platforms", "soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.15, "projects": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "web_developer": {
                "required_skills": ["programming_languages", "web_technologies"],
                "preferred_skills": ["cloud_platforms", "soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.15, "projects": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "data_scientist": {
                "required_skills": ["data_science", "programming_languages"],
                "preferred_skills": ["cloud_platforms", "databases"],
                "weights": {"skills": 0.45, "experience": 0.25, "education": 0.20, "projects": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 60
            },
            "data_analyst": {
                "required_skills": ["data_science", "programming_languages"],
                "preferred_skills": ["databases", "soft_skills"],
                "weights": {"skills": 0.45, "experience": 0.25, "education": 0.20, "projects": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "cybersecurity_specialist": {
                "required_skills": ["security_safety", "programming_languages"],
                "preferred_skills": ["cloud_platforms", "certifications"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "certifications": 0.05},
                "contextual_bonus": 65,
                "minimum_threshold": 60
            },

            # Creative & Entertainment
            "singer_performer": {
                "required_skills": ["creative_arts"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.40, "experience": 0.35, "performance_quality": 0.15, "education": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 40
            },
            "graphic_designer": {
                "required_skills": ["creative_arts"],
                "preferred_skills": ["soft_skills", "web_technologies"],
                "weights": {"skills": 0.50, "experience": 0.30, "portfolio": 0.15, "education": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },
            "photographer": {
                "required_skills": ["creative_arts"],
                "preferred_skills": ["soft_skills", "business_finance"],
                "weights": {"skills": 0.45, "experience": 0.30, "portfolio": 0.20, "education": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 40
            },
            "video_editor": {
                "required_skills": ["creative_arts"],
                "preferred_skills": ["soft_skills", "programming_languages"],
                "weights": {"skills": 0.55, "experience": 0.25, "portfolio": 0.15, "education": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },

            # Business & Finance
            "accountant": {
                "required_skills": ["business_finance"],
                "preferred_skills": ["soft_skills", "programming_languages"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "certifications": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "financial_analyst": {
                "required_skills": ["business_finance", "data_science"],
                "preferred_skills": ["programming_languages", "soft_skills"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "certifications": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "investment_banker": {
                "required_skills": ["business_finance"],
                "preferred_skills": ["soft_skills", "data_science"],
                "weights": {"skills": 0.40, "experience": 0.35, "education": 0.20, "network": 0.05},
                "contextual_bonus": 65,
                "minimum_threshold": 65
            },

            # Sales & Marketing
            "sales_representative": {
                "required_skills": ["sales_marketing", "soft_skills"],
                "preferred_skills": ["business_finance"],
                "weights": {"skills": 0.40, "experience": 0.35, "education": 0.15, "results": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 45
            },
            "marketing_manager": {
                "required_skills": ["sales_marketing", "soft_skills"],
                "preferred_skills": ["data_science", "creative_arts"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "campaigns": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },
            "digital_marketer": {
                "required_skills": ["sales_marketing", "web_technologies"],
                "preferred_skills": ["data_science", "creative_arts"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.15, "certifications": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },

            # Education
            "teacher": {
                "required_skills": ["education_skills", "soft_skills"],
                "preferred_skills": ["languages"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.20, "passion": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },
            "professor": {
                "required_skills": ["education_skills", "soft_skills"],
                "preferred_skills": ["research_tools"],
                "weights": {"skills": 0.40, "experience": 0.25, "education": 0.25, "research": 0.10},
                "contextual_bonus": 65,
                "minimum_threshold": 60
            },
            "tutor": {
                "required_skills": ["education_skills", "soft_skills"],
                "preferred_skills": ["languages"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.20, "results": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 40
            },

            # Engineering & Manufacturing
            "mechanical_engineer": {
                "required_skills": ["manufacturing_engineering"],
                "preferred_skills": ["programming_languages", "soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "projects": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "electrical_engineer": {
                "required_skills": ["manufacturing_engineering"],
                "preferred_skills": ["programming_languages", "soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "projects": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },
            "civil_engineer": {
                "required_skills": ["manufacturing_engineering", "real_estate_construction"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "projects": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 55
            },

            # Legal
            "lawyer": {
                "required_skills": ["legal_skills"],
                "preferred_skills": ["soft_skills", "languages"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.20, "bar_exam": 0.05},
                "contextual_bonus": 65,
                "minimum_threshold": 60
            },
            "paralegal": {
                "required_skills": ["legal_skills"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "certification": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },

            # Transportation
            "truck_driver": {
                "required_skills": ["transportation_logistics"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.60, "experience": 0.25, "safety_record": 0.10, "reliability": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 40
            },
            "pilot": {
                "required_skills": ["transportation_logistics"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.15, "certifications": 0.05},
                "contextual_bonus": 70,
                "minimum_threshold": 65
            },

            # Agriculture
            "farmer": {
                "required_skills": ["agriculture_environment"],
                "preferred_skills": ["soft_skills", "business_finance"],
                "weights": {"skills": 0.55, "experience": 0.30, "education": 0.10, "sustainability": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 40
            },
            "veterinarian": {
                "required_skills": ["agriculture_environment", "healthcare_skills"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "education": 0.20, "certification": 0.05},
                "contextual_bonus": 65,
                "minimum_threshold": 60
            },

            # Security
            "security_guard": {
                "required_skills": ["security_safety"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.30, "education": 0.10, "reliability": 0.10},
                "contextual_bonus": 55,
                "minimum_threshold": 40
            },
            "police_officer": {
                "required_skills": ["security_safety"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "fitness": 0.10},
                "contextual_bonus": 65,
                "minimum_threshold": 55
            },

            # Real Estate & Construction
            "real_estate_agent": {
                "required_skills": ["real_estate_construction", "sales_marketing"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "network": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 45
            },
            "construction_worker": {
                "required_skills": ["real_estate_construction"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.60, "experience": 0.25, "safety": 0.10, "reliability": 0.05},
                "contextual_bonus": 60,
                "minimum_threshold": 35
            },

            # Hospitality
            "hotel_manager": {
                "required_skills": ["hospitality_tourism", "business_finance"],
                "preferred_skills": ["soft_skills", "languages"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "guest_satisfaction": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },
            "tour_guide": {
                "required_skills": ["hospitality_tourism", "languages"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "knowledge": 0.15, "personality": 0.10},
                "contextual_bonus": 55,
                "minimum_threshold": 40
            },

            # Sports & Fitness
            "personal_trainer": {
                "required_skills": ["sports_recreation"],
                "preferred_skills": ["soft_skills", "healthcare_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "certification": 0.15, "results": 0.10},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },
            "sports_coach": {
                "required_skills": ["sports_recreation"],
                "preferred_skills": ["soft_skills", "education_skills"],
                "weights": {"skills": 0.45, "experience": 0.35, "education": 0.10, "team_results": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 45
            },

            # Retail & Customer Service
            "retail_manager": {
                "required_skills": ["retail_customer_service", "business_finance"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "sales_results": 0.10},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },
            "cashier": {
                "required_skills": ["retail_customer_service"],
                "preferred_skills": ["soft_skills"],
                "weights": {"skills": 0.50, "experience": 0.25, "reliability": 0.15, "accuracy": 0.10},
                "contextual_bonus": 50,
                "minimum_threshold": 35
            },
            "customer_service_representative": {
                "required_skills": ["retail_customer_service"],
                "preferred_skills": ["soft_skills", "languages"],
                "weights": {"skills": 0.45, "experience": 0.30, "communication": 0.20, "problem_solving": 0.05},
                "contextual_bonus": 55,
                "minimum_threshold": 40
            },

            # Human Resources
            "hr_manager": {
                "required_skills": ["human_resources", "soft_skills"],
                "preferred_skills": ["business_finance", "legal_skills"],
                "weights": {"skills": 0.45, "experience": 0.30, "education": 0.15, "certifications": 0.10},
                "contextual_bonus": 60,
                "minimum_threshold": 50
            },
            "recruiter": {
                "required_skills": ["human_resources", "soft_skills"],
                "preferred_skills": ["sales_marketing"],
                "weights": {"skills": 0.40, "experience": 0.35, "network": 0.15, "results": 0.10},
                "contextual_bonus": 55,
                "minimum_threshold": 45
            },

            # Research & Consulting
            "market_research_analyst": {
                "required_skills": ["market_research", "data_science"],
                "preferred_skills": ["business_consulting", "soft_skills"],
            "weights": {"skills": 0.40, "experience": 0.30, "education": 0.20, "domain_knowledge": 0.10},
            "contextual_bonus": 60,
            "minimum_threshold": 50
        },
        "business_consultant": {
            "required_skills": ["business_consulting", "soft_skills"],
            "preferred_skills": ["market_research", "business_finance"],
            "weights": {"skills": 0.35, "experience": 0.35, "education": 0.15, "client_impact": 0.15},
            "contextual_bonus": 60,
            "minimum_threshold": 55
        },
        "management_consultant": {
            "required_skills": ["business_consulting", "soft_skills"],
            "preferred_skills": ["data_science", "business_finance"],
            "weights": {"skills": 0.40, "experience": 0.30, "education": 0.20, "problem_solving": 0.10},
            "contextual_bonus": 65,
            "minimum_threshold": 60
        },

        # General/Entry Level
        "general": {
            "required_skills": ["soft_skills"],
            "preferred_skills": [],
            "weights": {"skills": 0.30, "experience": 0.30, "education": 0.25, "potential": 0.15},
            "contextual_bonus": 40,
            "minimum_threshold": 30
        },
        "intern": {
            "required_skills": ["soft_skills"],
            "preferred_skills": [],
            "weights": {"skills": 0.25, "experience": 0.20, "education": 0.35, "enthusiasm": 0.20},
            "contextual_bonus": 35,
            "minimum_threshold": 25
        },
        "entry_level": {
            "required_skills": ["soft_skills"],
            "preferred_skills": [],
            "weights": {"skills": 0.35, "experience": 0.25, "education": 0.25, "trainability": 0.15},
            "contextual_bonus": 40,
            "minimum_threshold": 30
        }
    }
    
    def setup_contextual_bonus_system(self):
        """Enhanced contextual bonus system for ALL job types"""
        self.contextual_factors = {
        "role_match_bonus": {
            "perfect_match": 80,      # Perfect role-skill alignment
            "good_match": 60,         # Good role-skill alignment
            "partial_match": 40,      # Some role-skill alignment
            "no_match": 0             # No role-skill alignment
        },
        "passion_indicators": {
            "culinary": ["passion for cooking", "love of food", "culinary arts", "food enthusiast", "cooking hobby", "chef dream", "culinary passion"],
            "music": ["music passion", "performance passion", "love of music", "musical background", "singing passion", "stage passion"],
            "healthcare": ["patient care", "helping others", "medical interest", "healthcare passion", "caring for people", "health advocacy"],
            "technology": ["tech enthusiast", "coding passion", "technology lover", "programming hobby", "innovation passion", "tech geek"],
            "education": ["teaching passion", "love of learning", "educational enthusiasm", "mentoring passion", "knowledge sharing"],
            "finance": ["financial markets", "investment passion", "numbers enthusiast", "economic interest", "financial planning"],
            "sales": ["people person", "relationship building", "persuasion skills", "networking passion", "communication love"],
            "creative": ["artistic vision", "creative expression", "design passion", "visual storytelling", "artistic soul"],
            "sports": ["athletic passion", "fitness enthusiasm", "competitive spirit", "sports lover", "physical wellness"],
            "legal": ["justice passion", "legal interest", "advocacy spirit", "law enthusiasm", "rights defender"],
            "engineering": ["problem solving", "innovation drive", "technical curiosity", "building passion", "design thinking"],
            "business": ["entrepreneurial spirit", "business acumen", "leadership drive", "growth mindset", "strategic thinking"]
        },
        "desperation_bonus": {
            "high_demand_roles": [
                "chef", "cook", "nurse", "teacher", "truck_driver", "construction_worker",
                "security_guard", "cashier", "customer_service_representative", "baker",
                "barista", "personal_trainer", "tutor"
            ],
            "bonus_points": 20
        },
        "critical_shortage_roles": {
            "roles": ["nurse", "doctor", "teacher", "truck_driver", "pilot", "cybersecurity_specialist"],
            "bonus_points": 30
        }
    }
    
    def setup_contextual_analyzers(self):
        """Enhanced contextual analysis patterns"""
        self.experience_quality_indicators = {
            "high_impact": ["led", "managed", "increased", "improved", "achieved", "delivered", "transformed"],
            "quantified_results": [r"\d+%", r"\$\d+", r"\d+\s*million", r"\d+k", r"\d+\s*years"],
            "team_leadership": ["team of", "managed", "supervised", "led", "directed"],
            "client_facing": ["client", "customer", "stakeholder", "presentation", "communication"]
        }
        
        # Enhanced job role keywords with more variations
        self.job_role_keywords = {
            "chef": ["chef", "head chef", "executive chef", "sous chef", "culinary", "cooking", "kitchen", "restaurant"],
            "cook": ["cook", "line cook", "prep cook", "kitchen staff", "food preparation", "culinary assistant"],
            "nurse": ["nurse", "nursing", "rn", "lpn", "cna", "healthcare", "patient care", "medical"],
            "singer_performer": ["singer", "vocalist", "performer", "musician", "artist", "entertainer", "music"],
            "software_engineer": ["software engineer", "developer", "programmer", "coding", "programming"],
            "web_developer": ["web developer", "frontend", "backend", "full stack", "web development"],
            "data_scientist": ["data scientist", "machine learning", "ai", "analytics", "data analysis"],
            "data_analyst": ["data analyst", "business analyst", "analytics", "reporting"],
            "sales_representative": ["sales", "sales rep", "account manager", "business development"],
            "teacher": ["teacher", "educator", "instructor", "professor", "teaching"],
            "accountant": ["accountant", "accounting", "bookkeeper", "financial analyst"]
        }
    
    def setup_human_like_scoring(self):
        """Enhanced human-like scoring with contextual awareness"""
        self.scoring_criteria = {
            "excellent": {"min_score": 85, "description": "Outstanding candidate - immediate interview"},
            "very_good": {"min_score": 75, "description": "Strong candidate - high priority"},
            "good": {"min_score": 65, "description": "Good candidate - consider for interview"},
            "contextual_fit": {"min_score": 45, "description": "Role-specific fit - worth considering"},  # NEW
            "average": {"min_score": 35, "description": "Average candidate - may need development"},
            "below_average": {"min_score": 25, "description": "Below requirements - not recommended"},
            "poor": {"min_score": 0, "description": "Poor fit - significant gaps"}
        }

    def calculate_contextual_role_match(self, resume_analysis: Dict, job_requirements: Dict) -> Dict:
        """NEW: Calculate contextual role match with bonus scoring"""
        if not job_requirements:
            return {"match_level": "no_match", "bonus_points": 0, "reasoning": "No job description provided"}
        
        job_role = job_requirements.get("job_role", "general")
        resume_skills = resume_analysis.get("skills", {})
        resume_text = self._get_resume_text_from_analysis(resume_analysis)
        
        # Calculate role-specific skill alignment
        role_config = self.industry_role_weights.get(job_role, {})
        required_skills = role_config.get("required_skills", [])
        
        # Check for direct skill matches
        skill_match_score = 0
        matched_categories = []
        
        for skill_category in required_skills:
            if skill_category in resume_skills:
                skill_match_score += 1
                matched_categories.append(skill_category)
        
        # Calculate match level
        if len(required_skills) > 0:
            match_percentage = (skill_match_score / len(required_skills)) * 100
        else:
            match_percentage = 0
        
        # Determine match level and bonus
        if match_percentage >= 80:
            match_level = "perfect_match"
            bonus_points = self.contextual_factors["role_match_bonus"]["perfect_match"]
        elif match_percentage >= 60:
            match_level = "good_match"
            bonus_points = self.contextual_factors["role_match_bonus"]["good_match"]
        elif match_percentage >= 30:
            match_level = "partial_match"
            bonus_points = self.contextual_factors["role_match_bonus"]["partial_match"]
        else:
            match_level = "no_match"
            bonus_points = 0        

        # Additional passion/enthusiasm bonus
        passion_bonus = self.calculate_passion_bonus(resume_text, job_role)
        
        # High-demand role bonus
        demand_bonus = self.calculate_demand_bonus(job_role)
        
        total_bonus = bonus_points + passion_bonus + demand_bonus
        
        return {
            "match_level": match_level,
            "bonus_points": total_bonus,
            "skill_match_percentage": match_percentage,
            "matched_categories": matched_categories,
            "passion_bonus": passion_bonus,
            "demand_bonus": demand_bonus,
            "reasoning": self._generate_match_reasoning(match_level, matched_categories, job_role)
        }
    
    def calculate_passion_bonus(self, resume_text: str, job_role: str) -> int:
        """Calculate bonus points for passion indicators"""
        passion_bonus = 0
        resume_lower = resume_text.lower()
        
        # Map job roles to passion categories
        passion_mapping = {
            "chef": "culinary",
            "cook": "culinary", 
            "singer_performer": "music",
            "nurse": "healthcare",
            "software_engineer": "technology",
            "web_developer": "technology",
            "teacher": "education"
        }
        
        passion_category = passion_mapping.get(job_role)
        if passion_category and passion_category in self.contextual_factors["passion_indicators"]:
            passion_keywords = self.contextual_factors["passion_indicators"][passion_category]
            
            for keyword in passion_keywords:
                if keyword in resume_lower:
                    passion_bonus += 5  # 5 points per passion indicator
        
        return min(passion_bonus, 15)  # Cap at 15 points
    
    def calculate_demand_bonus(self, job_role: str) -> int:
        """Calculate bonus for high-demand roles"""
        high_demand_roles = self.contextual_factors["desperation_bonus"]["high_demand_roles"]
        
        if job_role in high_demand_roles:
            return self.contextual_factors["desperation_bonus"]["bonus_points"]
        
        return 0
    
    def _get_resume_text_from_analysis(self, resume_analysis: Dict) -> str:
        """Extract text content from resume analysis for passion detection"""
        text_parts = []
        
        # Add skills text
        skills = resume_analysis.get("skills", {})
        for category_skills in skills.values():
            if isinstance(category_skills, dict):
                for subcategory_skills in category_skills.values():
                    text_parts.extend(subcategory_skills)
            elif isinstance(category_skills, list):
                text_parts.extend(category_skills)
        
        # Add achievements text
        achievements = resume_analysis.get("achievements", [])
        for achievement in achievements:
            if isinstance(achievement, dict):
                text_parts.append(achievement.get("statement", ""))
            else:
                text_parts.append(str(achievement))
        
        return " ".join(text_parts).lower()
    
    def _generate_match_reasoning(self, match_level: str, matched_categories: List[str], job_role: str) -> str:
        """Generate human-readable reasoning for the match"""
        if match_level == "perfect_match":
            return f"Perfect fit for {job_role} - has all required skills: {', '.join(matched_categories)}"
        elif match_level == "good_match":
            return f"Strong fit for {job_role} - has most required skills: {', '.join(matched_categories)}"
        elif match_level == "partial_match":
            return f"Partial fit for {job_role} - has some relevant skills: {', '.join(matched_categories)}"
        else:
            return f"Limited fit for {job_role} - missing key skills"

    def calculate_resume_score(self, resume_text: str, job_description: str = "", job_title: str = "") -> Dict:
        """Enhanced main scoring method with contextual bonuses"""
        try:
            # Extract comprehensive resume information
            resume_analysis = {
                "skills": self.extract_skills_with_context(resume_text),
                "experience": self.extract_experience_with_quality(resume_text),
                "education": self.extract_education_with_context(resume_text),
                "achievements": self.extract_quantified_achievements(resume_text)
            }
            
            # Extract job requirements if provided
            job_requirements = {}
            if job_description.strip():
                job_requirements = self.extract_comprehensive_job_requirements(job_description)
            
            # NEW: Calculate contextual role match and bonuses
            contextual_match = self.calculate_contextual_role_match(resume_analysis, job_requirements)
            
            # Calculate job fit if job description provided
            job_fit_analysis = {}
            if job_requirements:
                job_fit_analysis = self.calculate_job_fit_score(resume_analysis, job_requirements)
            
            # Calculate individual scores
            skills_score = self.calculate_skills_score(resume_analysis)
            experience_score = self.calculate_experience_score(resume_analysis)
            education_score = self.calculate_education_score(resume_analysis)
            
            # Calculate base overall score
            if job_description.strip():
                # Prioritize job fit when job description is provided
                base_score = (
                    job_fit_analysis.get("overall_fit", 50) * 0.7 +
                    skills_score * 0.2 +
                    experience_score * 0.15 +
                    education_score * 0.05
                )
            else:
                # General scoring without job description
                base_score = (
                    skills_score * 0.35 +
                    experience_score * 0.30 +
                    education_score * 0.25 +
                    50 * 0.10  # Base quality score
                )
            
            # NEW: Apply contextual bonuses
            contextual_bonus = contextual_match.get("bonus_points", 0)
            final_score = min(base_score + contextual_bonus, 100)  # Cap at 100
            
            # NEW: Apply minimum threshold logic for role-specific candidates
            job_role = job_requirements.get("job_role", "general") if job_requirements else "general"
            role_config = self.industry_role_weights.get(job_role, {})
            minimum_threshold = role_config.get("minimum_threshold", 0)
            
            # If candidate has role-specific skills but low overall score, boost to minimum threshold
            if (contextual_match.get("match_level") in ["perfect_match", "good_match", "partial_match"] and 
                final_score < minimum_threshold):
                final_score = minimum_threshold
            
            # Generate enhanced recommendations
            recommendations = self.generate_enhanced_recommendations(
                resume_analysis, job_requirements, final_score, contextual_match
            )
            
            # Format for backward compatibility
            skills_found = self.format_skills_for_display(resume_analysis["skills"])
            experience_info = {
                "max_years": resume_analysis["experience"]["max_years"],
                "companies": resume_analysis["experience"]["companies"]
            }
            education_info = {
                "degrees": resume_analysis["education"]["degrees"],
                "cgpa": resume_analysis["education"]["highest_gpa"]
            }
            
            return {
                "overall_score": round(max(0, min(final_score, 100)), 2),
                "base_score": round(base_score, 2),  # NEW: Show base score before bonuses
                "contextual_bonus": contextual_bonus,  # NEW: Show bonus points
                "detailed_scores": {
                    "job_fit": job_fit_analysis.get("overall_fit") if job_fit_analysis else None,
                    "skills": round(skills_score, 2),
                    "experience": round(experience_score, 2),
                    "education": round(education_score, 2)
                },
                "contextual_analysis": contextual_match,  # NEW: Contextual match analysis
                "job_fit_analysis": job_fit_analysis,
                "skills_found": skills_found,
                "experience_info": experience_info,
                "education_info": education_info,
                "achievements": resume_analysis["achievements"],
                "total_skills_count": self.count_total_skills(resume_analysis["skills"]),
                "job_role_identified": job_role,
                "recommendations": recommendations,
                "confidence_level": job_requirements.get("role_confidence", 0.5) if job_requirements else 0.5,
                "scoring_rationale": self._generate_scoring_rationale(base_score, contextual_bonus, job_role)  # NEW
            }
            
        except Exception as e:
            st.error(f"Error in resume analysis: {str(e)}")
            return self.generate_fallback_score(resume_text)

    def generate_enhanced_recommendations(self, resume_analysis: Dict, job_requirements: Dict, 
                                        final_score: float, contextual_match: Dict) -> List[str]:
        """Enhanced recommendations that account for contextual fit"""
        recommendations = []
        
        # Overall assessment with contextual awareness
        match_level = contextual_match.get("match_level", "no_match")
        bonus_points = contextual_match.get("bonus_points", 0)
        job_role = job_requirements.get("job_role", "general") if job_requirements else "general"
        
        if final_score >= 85:
            recommendations.append("🌟 **HIGHLY RECOMMENDED**: Outstanding candidate with excellent qualifications")
        elif final_score >= 75:
            recommendations.append("✅ **RECOMMENDED**: Strong candidate with good potential")
        elif final_score >= 65:
            recommendations.append("👍 **CONSIDER**: Decent candidate worth reviewing")
        elif match_level in ["perfect_match", "good_match"] and final_score >= 45:
            # NEW: Special recommendation for role-specific fit
            recommendations.append(f"🎯 **ROLE-SPECIFIC FIT**: Strong match for {job_role} position despite limited overall experience")
        elif final_score >= 50:
            recommendations.append("⚠️ **REVIEW CAREFULLY**: Average candidate with some gaps")
        else:
            recommendations.append("❌ **NOT RECOMMENDED**: Significant gaps in qualifications")
        
        # NEW: Contextual bonus explanation
        if bonus_points > 0:
            bonus_explanation = []
            if contextual_match.get("passion_bonus", 0) > 0:
                bonus_explanation.append("passion indicators")
            if contextual_match.get("demand_bonus", 0) > 0:
                bonus_explanation.append("high-demand role")
            if match_level != "no_match":
                bonus_explanation.append("role-specific skills")
            
            if bonus_explanation:
                recommendations.append(f"⭐ **BONUS POINTS** (+{bonus_points}): {', '.join(bonus_explanation)}")
        
        # Role-specific recommendations
        if job_role == "chef" or job_role == "cook":
            culinary_skills = resume_analysis.get("skills", {}).get("culinary_skills", {})
            if culinary_skills:
                skill_count = sum(len(skills) for skills in culinary_skills.values())
                if skill_count >= 5:
                    recommendations.append("👨‍🍳 **CULINARY EXPERTISE**: Strong culinary background with diverse skills")
                else:
                    recommendations.append("🔪 **CULINARY POTENTIAL**: Some culinary skills - may need training in specific areas")
            else:
                recommendations.append("⚠️ **CULINARY TRAINING NEEDED**: No culinary background found - extensive training required")
        
        # Standard skill/experience recommendations
        skills = resume_analysis.get("skills", {})
        experience = resume_analysis.get("experience", {})
        
        if self.count_total_skills(skills) < 5:
            recommendations.append("🔧 **Skills Development**: Limited skills - focused training recommended")
        
        if experience.get("max_years", 0) < 1:
            recommendations.append("💼 **Entry Level**: No prior experience - suitable for entry-level with mentoring")
        
        # Positive highlights
        achievements = resume_analysis.get("achievements", [])
        if len(achievements) >= 2:
            recommendations.append("🎯 **Results-Oriented**: Demonstrates achievements and impact")
        
        return recommendations

    def _generate_scoring_rationale(self, base_score: float, contextual_bonus: int, job_role: str) -> str:
        """NEW: Generate explanation of how the score was calculated"""
        rationale = f"Base score: {base_score:.1f}"
        
        if contextual_bonus > 0:
            rationale += f" + {contextual_bonus} contextual bonus"
            
            if job_role in self.contextual_factors["desperation_bonus"]["high_demand_roles"]:
                rationale += f" (role-specific fit for {job_role} position)"
        
        return rationale

    def extract_skills_with_context(self, text: str) -> Dict:
        """Enhanced skill extraction with exact word boundary matching to prevent false positives"""
        text_lower = text.lower()
        extracted_skills = {}
        
        # Track already found skills to avoid duplicates
        found_skill_texts = set()
        
        for category, subcategories in self.skills_db.items():
            category_skills = {}
            
            if isinstance(subcategories, dict):
                for subcategory, skills in subcategories.items():
                    found_skills = []
                    for skill in skills:
                        skill_lower = skill.lower()
                        
                        # Skip if already found
                        if skill_lower in found_skill_texts:
                            continue
                        
                        # Use exact word boundary matching
                        if self.is_exact_skill_match(skill_lower, text_lower):
                            found_skills.append(skill)
                            found_skill_texts.add(skill_lower)
                    
                    if found_skills:
                        category_skills[subcategory] = found_skills
            else:
                # Handle flat skill lists
                found_skills = []
                for skill in subcategories:
                    skill_lower = skill.lower()
                    if skill_lower not in found_skill_texts and self.is_exact_skill_match(skill_lower, text_lower):
                        found_skills.append(skill)
                        found_skill_texts.add(skill_lower)
                if found_skills:
                    category_skills = found_skills
            
            if category_skills:
                extracted_skills[category] = category_skills
        
        # Additional context validation for problematic skills
        validated_skills = self.validate_skills_in_context(extracted_skills, text_lower)
        
        return validated_skills

    def is_exact_skill_match(self, skill: str, text: str) -> bool:
        """Check if skill appears as exact match with proper word boundaries"""
        import re
        
        # Special handling for problematic short skills
        problematic_skills = {
            'ca': r'\b(?:ca\b|chartered accountant|chartered acc\.)',
            'ai': r'\b(?:ai\b|artificial intelligence)',
            'ml': r'\b(?:ml\b|machine learning)',
            'ui': r'\b(?:ui\b|user interface)',
            'ux': r'\b(?:ux\b|user experience)',
            'r': r'\b(?:r\b|r programming|r language|r statistical)',
            'c': r'\b(?:c\b|c programming|c language)(?!\+|\#|s)',
            'go': r'\b(?:go\b|golang|go programming)(?!\s*to|\s*for|\s*with)',
            'it': r'\b(?:it\b|information technology)(?!\s*is|\s*was|\s*will)',
            'hr': r'\b(?:hr\b|human resources)(?!\s*department|\s*team)',
        }
        
        # Use special patterns for problematic skills
        if skill in problematic_skills:
            pattern = problematic_skills[skill]
            return bool(re.search(pattern, text, re.IGNORECASE))
        
        # For other skills, create appropriate patterns
        try:
            if '/' in skill:
                # For skills like "ui/ux", "c++" - match exactly
                escaped_skill = re.escape(skill)
                pattern = rf'\b{escaped_skill}\b'
            elif '+' in skill:
                # For skills like "c++", "comptia a+" - match exactly
                escaped_skill = re.escape(skill)
                pattern = rf'\b{escaped_skill}\b'
            elif '.' in skill:
                # For skills like "node.js", "d3.js" - match exactly
                escaped_skill = re.escape(skill)
                pattern = rf'\b{escaped_skill}\b'
            elif len(skill) <= 3 and skill.isalpha():
                # For short skills - require exact word boundaries
                pattern = rf'\b{re.escape(skill)}\b'
            else:
                # For regular skills - match with word boundaries
                pattern = rf'\b{re.escape(skill)}\b'
                # Also check without spaces for compound terms
                if ' ' in skill:
                    no_space_skill = skill.replace(' ', '')
                    pattern += f'|\\b{re.escape(no_space_skill)}\\b'
            
            return bool(re.search(pattern, text, re.IGNORECASE))
            
        except re.error:
            # Fallback to simple word boundary check
            return f' {skill} ' in f' {text} '

    def validate_skills_in_context(self, found_skills: Dict, text: str) -> Dict:
        """Validate found skills using context to reduce false positives"""
        from collections import defaultdict
        
        validated_skills = defaultdict(dict) if any(isinstance(v, dict) for v in found_skills.values()) else defaultdict(list)
        
        # Context validation rules
        context_rules = {
            'ca': {
                'positive_context': ['chartered accountant', 'ca final', 'ca inter', 'icai', 'institute of chartered accountants', 'accounting', 'finance'],
                'negative_context': ['education', 'application', 'statistical', 'medical', 'chemical', 'practical', 'theoretical', 'mathematics']
            },
            'ai': {
                'positive_context': ['artificial intelligence', 'machine learning', 'deep learning', 'neural networks', 'ai/ml'],
                'negative_context': ['available', 'again', 'said', 'wait', 'main', 'certain']
            },
            'go': {
                'positive_context': ['golang', 'go programming', 'go language', 'google go', 'programming'],
                'negative_context': ['go to', 'go for', 'go with', 'let go', 'going', 'go back', 'go through']
            },
            'r': {
                'positive_context': ['r programming', 'r language', 'r statistical', 'rstudio', 'cran', 'programming'],
                'negative_context': ['for', 'or', 'are', 'our', 'more', 'other', 'their', 'your', 'over']
            },
            'it': {
                'positive_context': ['information technology', 'it support', 'it department', 'it services'],
                'negative_context': ['it is', 'it was', 'it will', 'it can', 'it has', 'it would']
            }
        }
        
        for category, skills_data in found_skills.items():
            if isinstance(skills_data, dict):
                # Handle subcategorized skills
                validated_category = {}
                for subcategory, skills in skills_data.items():
                    validated_subcategory = []
                    for skill in skills:
                        if self.validate_individual_skill(skill.lower(), text, context_rules):
                            validated_subcategory.append(skill)
                    if validated_subcategory:
                        validated_category[subcategory] = validated_subcategory
                if validated_category:
                    validated_skills[category] = validated_category
            else:
                # Handle flat skill lists
                validated_category = []
                for skill in skills_data:
                    if self.validate_individual_skill(skill.lower(), text, context_rules):
                        validated_category.append(skill)
                if validated_category:
                    validated_skills[category] = validated_category
        
        return dict(validated_skills)

    def validate_individual_skill(self, skill: str, text: str, context_rules: Dict) -> bool:
        """Validate individual skill using context rules"""
        if skill not in context_rules:
            return True  # No special validation needed
        
        rule = context_rules[skill]
        
        # Check for positive context
        has_positive_context = any(context in text for context in rule['positive_context'])
        
        # Check for negative context
        has_negative_context = any(context in text for context in rule['negative_context'])
        
        # Only include if positive context exists OR no negative context
        if has_positive_context:
            return True
        elif has_negative_context:
            return False
        else:
            # For ambiguous cases, check if it appears in a skill-relevant context
            return self.is_in_skill_context(skill, text)

    def is_in_skill_context(self, skill: str, text: str) -> bool:
        """Check if skill appears in a skill-relevant context"""
        import re
        
        # Create pattern for skill mentions
        pattern = rf'\b{re.escape(skill)}\b'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            start, end = match.span()
            
            # Get surrounding context (30 characters before and after)
            context_start = max(0, start - 30)
            context_end = min(len(text), end + 30)
            context = text[context_start:context_end]
            
            # Check if it's in a skill-relevant context
            skill_indicators = [
                'programming', 'language', 'skill', 'experience', 'proficient',
                'knowledge', 'familiar', 'expert', 'certification', 'course',
                'training', 'project', 'development', 'technology', 'software',
                'tools', 'frameworks', 'languages', 'technical', 'professional'
            ]
            
            if any(indicator in context.lower() for indicator in skill_indicators):
                return True
            
            # Check if it's in a list format (common in resumes)
            if re.search(r'[,•\-\*]\s*' + re.escape(skill) + r'\s*[,•\-\*\n]', context, re.IGNORECASE):
                return True
        
        return False
        
    def extract_experience_with_quality(self, text: str) -> Dict:
        """Extract experience with quality assessment"""
        # Extract years of experience
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)',
            r'over\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:professional\s*)?(?:experience|exp)'
        ]
        
        years_found = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if isinstance(match, tuple):
                    years_found.extend([int(x) for x in match if x.isdigit()])
                else:
                    years_found.append(int(match))
        
        # Extract company names and positions
        company_patterns = [
            r'(?:at|@)\s+([A-Z][a-zA-Z\s&.,]+?)(?:\s|,|\.|\n)',
            r'([A-Z][a-zA-Z\s&.,]+?)\s+(?:company|corp|corporation|inc|ltd|llc)'
        ]
        
        companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        # Quality assessment
        quality_score = self.assess_experience_quality(text)
        
        max_years = max(years_found) if years_found else 0
        
        return {
            "years_experience": years_found,
            "max_years": max_years,
            "companies": list(set(companies))[:10],
            "quality_score": quality_score,
            "quality_indicators": self.extract_quality_indicators(text)
        }

    def assess_experience_quality(self, text: str) -> float:
        """Assess the quality of experience based on indicators"""
        text_lower = text.lower()
        quality_score = 50  # Base score
        
        # High-impact verbs
        high_impact_count = sum(1 for verb in self.experience_quality_indicators["high_impact"] 
                               if verb in text_lower)
        quality_score += min(high_impact_count * 5, 20)
        
        # Quantified results
        quantified_count = sum(1 for pattern in self.experience_quality_indicators["quantified_results"] 
                              if re.search(pattern, text_lower))
        quality_score += min(quantified_count * 3, 15)
        
        # Leadership indicators
        leadership_count = sum(1 for indicator in self.experience_quality_indicators["team_leadership"] 
                              if indicator in text_lower)
        quality_score += min(leadership_count * 4, 15)
        
        return min(quality_score, 100)

    def extract_quality_indicators(self, text: str) -> Dict:
        """Extract specific quality indicators from experience"""
        text_lower = text.lower()
        
        indicators = {
            "leadership_evidence": [],
            "quantified_achievements": [],
            "client_interaction": [],
            "technical_projects": []
        }
        
        # Leadership evidence
        leadership_patterns = [
            r'(led\s+[^.]{0,50})',
            r'(managed\s+team[^.]{0,50})',
            r'(supervised\s+[^.]{0,50})'
        ]
        
        for pattern in leadership_patterns:
            matches = re.findall(pattern, text_lower)
            indicators["leadership_evidence"].extend(matches)
        
        # Quantified achievements
        quant_patterns = [
            r'(\d+%[^.]{0,50})',
            r'(\$\d+[^.]{0,50})',
            r'(increased[^.]{0,50}\d+[^.]{0,20})',
            r'(reduced[^.]{0,50}\d+[^.]{0,20})'
        ]
        
        for pattern in quant_patterns:
            matches = re.findall(pattern, text_lower)
            indicators["quantified_achievements"].extend(matches)
        
        return indicators

    def extract_education_with_context(self, text: str) -> Dict:
        """Extract education with contextual information"""
        degree_patterns = [
            r'\b(bachelor|master|phd|doctorate|diploma|certificate)\b',
            r'\b(b\.?tech|m\.?tech|b\.?sc|m\.?sc|mba|bba|b\.?com|m\.?com|be|me)\b',
            r'\b(engineering|computer science|information technology|statistics|mathematics|business administration)\b'
        ]
        
        degrees = []
        for pattern in degree_patterns:
            matches = re.findall(pattern, text.lower())
            degrees.extend(matches)
        
        # Extract GPA/CGPA
        gpa_patterns = [
            r'gpa[:\s]*(\d+\.?\d*)',
            r'cgpa[:\s]*(\d+\.?\d*)',
            r'grade[:\s]*(\d+\.?\d*)'
        ]
        
        gpa_scores = []
        for pattern in gpa_patterns:
            matches = re.findall(pattern, text.lower())
            gpa_scores.extend([float(score) for score in matches])
        
        return {
            "degrees": list(set(degrees)),
            "gpa_scores": gpa_scores,
            "highest_gpa": max(gpa_scores) if gpa_scores else None,
            "education_quality": self.assess_education_quality(text)
        }

    def assess_education_quality(self, text: str) -> float:
        """Assess education quality based on various indicators"""
        text_lower = text.lower()
        quality_score = 50
        
        # Prestigious institutions
        prestigious_keywords = ["mit", "stanford", "harvard", "cambridge", "oxford", "iit", "nit"]
        if any(keyword in text_lower for keyword in prestigious_keywords):
            quality_score += 20
        
        # Academic achievements
        achievement_keywords = ["magna cum laude", "summa cum laude", "dean's list", "scholarship", "honors"]
        achievement_count = sum(1 for keyword in achievement_keywords if keyword in text_lower)
        quality_score += min(achievement_count * 5, 15)
        
        return min(quality_score, 100)

    def extract_quantified_achievements(self, text: str) -> List[Dict]:
        """Extract quantified achievements and impact statements"""
        achievement_patterns = [
            r'(increased[^.]{0,100}\d+[^.]{0,50})',
            r'(improved[^.]{0,100}\d+[^.]{0,50})',
            r'(reduced[^.]{0,100}\d+[^.]{0,50})',
            r'(achieved[^.]{0,100}\d+[^.]{0,50})',
            r'(delivered[^.]{0,100}\d+[^.]{0,50})'
        ]
        
        achievements = []
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                achievements.append({
                    "statement": match.strip(),
                    "type": self.categorize_achievement(match),
                    "impact_level": self.assess_impact_level(match)
                })
        
        return achievements

    def categorize_achievement(self, achievement: str) -> str:
        """Categorize the type of achievement"""
        achievement_lower = achievement.lower()
        if any(word in achievement_lower for word in ["revenue", "profit", "sales"]):
            return "financial"
        elif any(word in achievement_lower for word in ["efficiency", "process", "productivity"]):
            return "operational"
        elif any(word in achievement_lower for word in ["customer", "client", "user"]):
            return "customer_focused"
        else:
            return "general"

    def assess_impact_level(self, achievement: str) -> str:
        """Assess the impact level of an achievement"""
        # Look for percentage improvements
        percentages = re.findall(r'(\d+)%', achievement)
        if percentages:
            max_percentage = max([int(p) for p in percentages])
            if max_percentage >= 50:
                return "high"
            elif max_percentage >= 20:
                return "medium"
            else:
                return "low"
        
        # Look for monetary values
        if re.search(r'\$\d+', achievement):
            return "high"
        
        return "medium"

    def identify_job_role_with_confidence(self, job_description: str) -> Tuple[str, float]:
        """Identify job role with confidence scoring"""
        if not job_description:
            return "general", 0.0
        
        text_lower = job_description.lower()
        role_scores = {}
        
        for role, keywords in self.job_role_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            if score > 0:
                # Calculate confidence based on keyword density
                confidence = min(score / len(keywords), 1.0)
                role_scores[role] = confidence
        
        if role_scores:
            best_role = max(role_scores, key=role_scores.get)
            confidence = role_scores[best_role]
            return best_role, confidence
        
        return "general", 0.0

    def extract_comprehensive_job_requirements(self, job_description: str) -> Dict:
        """Extract comprehensive job requirements with contextual understanding"""
        if not job_description:
            return {}
        
        # Identify job role with confidence
        job_role, confidence = self.identify_job_role_with_confidence(job_description)
        
        # Extract required skills
        required_skills = self.extract_required_skills_from_job(job_description, job_role)
        
        # Extract experience requirements
        experience_req = self.extract_experience_requirements_from_job(job_description)
        
        # Extract education requirements
        education_req = self.extract_education_requirements_from_job(job_description)
        
        return {
            "job_role": job_role,
            "role_confidence": confidence,
            "required_skills": required_skills,
            "experience_requirements": experience_req,
            "education_requirements": education_req,
            "keywords": self.extract_job_keywords(job_description)
        }

    def extract_required_skills_from_job(self, job_description: str, job_role: str) -> Dict:
        """Extract required skills based on job role and description"""
        text_lower = job_description.lower()
        required_skills = defaultdict(list)
        
        # Get role-specific skill categories
        role_mapping = self.industry_role_weights.get(job_role, {})
        required_categories = role_mapping.get("required_skills", [])
        
        # Extract skills from job description
        job_skills = self.extract_skills_with_context(job_description)
        
        # Prioritize skills based on role requirements
        for category in required_categories:
            if category in job_skills:
                required_skills[category] = job_skills[category]
        
        # Add other mentioned skills
        for category, skills in job_skills.items():
            if category not in required_skills:
                required_skills[category] = skills
        
        return dict(required_skills)

    def extract_experience_requirements_from_job(self, job_description: str) -> Dict:
        """Extract experience requirements from job description"""
        text_lower = job_description.lower()
        
        # Extract years of experience
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
            r'at\s*least\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        years_found = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            years_found.extend([int(match) for match in matches])
        
        return {
            "min_years": min(years_found) if years_found else 0,
            "preferred_years": max(years_found) if years_found else 0
        }

    def extract_education_requirements_from_job(self, job_description: str) -> Dict:
        """Extract education requirements from job description"""
        text_lower = job_description.lower()
        
        education_keywords = [
            "bachelor", "master", "phd", "doctorate", "degree",
            "b.tech", "m.tech", "mba", "bba"
        ]
        
        required_education = []
        for keyword in education_keywords:
            if keyword in text_lower:
                required_education.append(keyword)
        
        return {
            "required_degrees": required_education,
            "degree_required": len(required_education) > 0
        }

    def extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract important keywords from job description using TF-IDF"""
        if not job_description:
            return []
        
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', job_description.lower())
        words = text.split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Get word frequency and return top keywords
        word_freq = Counter(meaningful_words)
        return [word for word, count in word_freq.most_common(15)]

    def calculate_job_fit_score(self, resume_analysis: Dict, job_requirements: Dict) -> Dict:
        """Calculate comprehensive job fit score"""
        if not job_requirements:
            return {
                "overall_fit": 50,
                "skills_match": 50,
                "experience_fit": 50,
                "education_fit": 50,
                "keyword_match": 50
            }
        
        # Calculate individual fit scores
        skills_match = self.calculate_skills_match(resume_analysis, job_requirements)
        experience_fit = self.calculate_experience_fit(resume_analysis, job_requirements)
        education_fit = self.calculate_education_fit(resume_analysis, job_requirements)
        keyword_match = self.calculate_keyword_match(resume_analysis, job_requirements)
        
        # Calculate weighted overall fit
        job_role = job_requirements.get("job_role", "general")
        role_weights = self.industry_role_weights.get(job_role, {}).get("weights", {})
        
        if role_weights:
            overall_fit = (
                skills_match * role_weights.get("skills", 0.4) +
                experience_fit * role_weights.get("experience", 0.3) +
                education_fit * role_weights.get("education", 0.2) +
                keyword_match * 0.1
            )
        else:
            overall_fit = (skills_match * 0.4 + experience_fit * 0.3 + 
                          education_fit * 0.2 + keyword_match * 0.1)
        
        return {
            "overall_fit": round(overall_fit, 2),
            "skills_match": round(skills_match, 2),
            "experience_fit": round(experience_fit, 2),
            "education_fit": round(education_fit, 2),
            "keyword_match": round(keyword_match, 2)
        }

    def calculate_skills_match(self, resume_analysis: Dict, job_requirements: Dict) -> float:
        """Calculate how well resume skills match job requirements"""
        resume_skills = resume_analysis.get("skills", {})
        required_skills = job_requirements.get("required_skills", {})
        
        if not required_skills:
            return 50.0
        
        total_required = 0
        matched_skills = 0
        
        for category, req_skills in required_skills.items():
            if isinstance(req_skills, dict):
                for subcategory, skills_list in req_skills.items():
                    total_required += len(skills_list)
                    
                    if category in resume_skills and subcategory in resume_skills[category]:
                        resume_category_skills = resume_skills[category][subcategory]
                        for skill in skills_list:
                            if any(skill.lower() in resume_skill.lower() for resume_skill in resume_category_skills):
                                matched_skills += 1
            elif isinstance(req_skills, list):
                total_required += len(req_skills)
                
                if category in resume_skills:
                    resume_category_skills = resume_skills[category]
                    for skill in req_skills:
                        if isinstance(resume_category_skills, dict):
                            # Check all subcategories
                            for subcategory_skills in resume_category_skills.values():
                                if any(skill.lower() in resume_skill.lower() for resume_skill in subcategory_skills):
                                    matched_skills += 1
                                    break
                        elif isinstance(resume_category_skills, list):
                            if any(skill.lower() in resume_skill.lower() for resume_skill in resume_category_skills):
                                matched_skills += 1
        
        return (matched_skills / total_required * 100) if total_required > 0 else 0

    def calculate_experience_fit(self, resume_analysis: Dict, job_requirements: Dict) -> float:
        """Calculate experience fit for the job"""
        experience = resume_analysis.get("experience", {})
        experience_req = job_requirements.get("experience_requirements", {})
        
        candidate_years = experience.get("max_years", 0)
        required_years = experience_req.get("min_years", 0)
        
        if required_years == 0:
            return 75.0  # Neutral score if no requirement
        
        if candidate_years >= required_years:
            # Bonus for exceeding requirements
            bonus = min((candidate_years - required_years) * 5, 25)
            return min(100, 75 + bonus)
        else:
            # Penalty for not meeting requirements
            penalty = (required_years - candidate_years) * 10
            return max(0, 75 - penalty)

    def calculate_education_fit(self, resume_analysis: Dict, job_requirements: Dict) -> float:
        """Calculate education fit for the job"""
        education = resume_analysis.get("education", {})
        education_req = job_requirements.get("education_requirements", {})
        
        if not education_req.get("degree_required", False):
            return 75.0  # Neutral if no degree required
        
        candidate_degrees = education.get("degrees", [])
        required_degrees = education_req.get("required_degrees", [])
        
        if not candidate_degrees:
            return 20.0  # Low score if no degree and degree required
        
        # Check for degree level match
        degree_hierarchy = {
            "certificate": 1, "diploma": 2, "bachelor": 3, "master": 4, "phd": 5
        }
        
        candidate_level = 0
        for degree in candidate_degrees:
            for level, value in degree_hierarchy.items():
                if level in degree.lower():
                    candidate_level = max(candidate_level, value)
        
        required_level = 0
        for degree in required_degrees:
            for level, value in degree_hierarchy.items():
                if level in degree.lower():
                    required_level = max(required_level, value)
        
        if candidate_level >= required_level:
            return 100
        elif candidate_level == required_level - 1:
            return 80
        else:
            return 50

    def calculate_keyword_match(self, resume_analysis: Dict, job_requirements: Dict) -> float:
        """Calculate how many job keywords appear in resume"""
        job_keywords = job_requirements.get("keywords", [])
        
        if not job_keywords:
            return 50.0
        
        # Get all text from resume analysis
        resume_text = ""
        skills = resume_analysis.get("skills", {})
        for category_skills in skills.values():
            if isinstance(category_skills, dict):
                for subcategory_skills in category_skills.values():
                    resume_text += " " + " ".join(subcategory_skills)
            elif isinstance(category_skills, list):
                resume_text += " " + " ".join(category_skills)
        
        resume_text_lower = resume_text.lower()
        
        matched_keywords = sum(1 for keyword in job_keywords if keyword in resume_text_lower)
        return (matched_keywords / len(job_keywords)) * 100

    def calculate_skills_score(self, resume_analysis: Dict, job_role: Optional[str] = "general") -> float:
        """Calculate skills score based on quantity, diversity, and relevance to job role"""
        skills = resume_analysis.get("skills", {})
        total_skills = self.count_total_skills(skills)

        if total_skills == 0:
            return 0.0

        # Base score from skill count
        base_score = min(total_skills * 3, 90)

        # Quality bonus for diverse skill categories
        category_count = len(skills)
        diversity_bonus = min(category_count * 2, 10)

        total_score = base_score + diversity_bonus

        # Penalize irrelevant skills if job_role is known
        if job_role in self.industry_role_weights:
            required_categories = set(self.industry_role_weights[job_role].get("required_skills", []))
            irrelevant_skills = sum(
                len(skills_list) for category, subskills in skills.items()
                if category not in required_categories
                for skills_list in (subskills.values() if isinstance(subskills, dict) else [subskills])
            )
            penalty = irrelevant_skills * 1.5
            total_score -= penalty

        return max(0.0, min(total_score, 100.0))


    def calculate_experience_score(self, resume_analysis: Dict) -> float:
        """Calculate experience score"""
        experience = resume_analysis.get("experience", {})
        years = experience.get("max_years", 0)
        quality_score = experience.get("quality_score", 50)
        
        # Years-based score
        years_score = min(years * 10, 80)
        
        # Quality adjustment
        quality_adjustment = (quality_score - 50) * 0.4
        
        return max(0, min(years_score + quality_adjustment, 100))

    def calculate_education_score(self, resume_analysis: Dict) -> float:
        """Calculate education score"""
        education = resume_analysis.get("education", {})
        degrees = education.get("degrees", [])
        gpa = education.get("highest_gpa")
        quality = education.get("education_quality", 50)
        
        if not degrees:
            return 30  # Base score for no formal education
        
        # Degree level scoring
        degree_hierarchy = {"certificate": 40, "diploma": 50, "bachelor": 70, "master": 85, "phd": 95}
        degree_score = 0
        
        for degree in degrees:
            for level, score in degree_hierarchy.items():
                if level in degree.lower():
                    degree_score = max(degree_score, score)
        
        # GPA bonus
        gpa_bonus = 0
        if gpa:
            if gpa >= 3.5:
                gpa_bonus = 10
            elif gpa >= 3.0:
                gpa_bonus = 5
        
        # Quality adjustment
        quality_adjustment = (quality - 50) * 0.2
        
        return min(degree_score + gpa_bonus + quality_adjustment, 100)

    def format_skills_for_display(self, skills: Dict) -> Dict:
        """Format skills for display compatibility"""
        formatted_skills = {}
        
        for category, category_data in skills.items():
            if isinstance(category_data, dict):
                # Flatten subcategories
                all_skills = []
                for subcategory_skills in category_data.values():
                    all_skills.extend(subcategory_skills)
                formatted_skills[category] = all_skills
            else:
                formatted_skills[category] = category_data
        
        return formatted_skills

    def count_total_skills(self, skills: Dict) -> int:
        """Count total number of skills"""
        total = 0
        for category_data in skills.values():
            if isinstance(category_data, dict):
                for subcategory_skills in category_data.values():
                    total += len(subcategory_skills)
            elif isinstance(category_data, list):
                total += len(category_data)
        return total

    def generate_fallback_score(self, resume_text: str) -> Dict:
        """Generate basic fallback score in case of errors"""
        # Very basic skill extraction
        basic_skills = {}
        for category, subcategories in self.skills_db.items():
            found_skills = []
            if isinstance(subcategories, dict):
                for subcat_skills in subcategories.values():
                    for skill in subcat_skills:
                        if skill.lower() in resume_text.lower():
                            found_skills.append(skill)
            if found_skills:
                basic_skills[category] = found_skills
        
        # Basic experience extraction
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_matches = re.findall(years_pattern, resume_text.lower())
        max_years = max([int(year) for year in years_matches]) if years_matches else 0
        
        basic_score = min(len([skill for skills in basic_skills.values() for skill in skills]) * 3 + max_years * 5, 100)
        
        return {
            "overall_score": basic_score,
            "detailed_scores": {"skills": basic_score * 0.6, "experience": max_years * 10, "education": 50},
            "skills_found": basic_skills,
            "experience_info": {"max_years": max_years, "companies": []},
            "education_info": {"degrees": [], "cgpa": None},
            "total_skills_count": sum(len(skills) for skills in basic_skills.values()),
            "job_role_identified": "general",
            "recommendations": ["⚠️ Basic analysis completed - some features may not be available"],
            "confidence_level": 0.3
        }

    def get_recommendations(self, analysis_result: Dict) -> List[str]:
        """Get recommendations from analysis result"""
        return analysis_result.get("recommendations", [])


# Alias for backward compatibility
JobMatchingAIAnalyzer = ProfessionalAIAnalyzer