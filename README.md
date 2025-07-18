# AI Resume Screener

A comprehensive AI-powered resume screening application built with Streamlit, designed to help HR professionals and recruiters efficiently analyze and score resumes against job requirements.

## 🚀 Features

### Core Functionality
- **Multi-format Support**: Process PDF, DOCX, and TXT resume files
- **AI-Powered Analysis**: Advanced NLP-based skill extraction and resume scoring
- **Job Matching**: Compare resumes against specific job descriptions
- **Batch Processing**: Analyze multiple resumes simultaneously
- **Interactive Visualizations**: Charts, graphs, and word clouds for better insights

### Analysis Capabilities
- **Skill Extraction**: Identify technical and soft skills across multiple categories
- **Experience Analysis**: Extract years of experience and job titles
- **Education Scoring**: Evaluate educational background and CGPA
- **Readability Assessment**: Analyze resume readability and structure
- **Job Fit Score**: Calculate compatibility with job requirements

### Visualization & Reporting
- **Score Gauges**: Visual representation of overall resume scores
- **Radar Charts**: Detailed breakdown of different scoring categories
- **Skills Bar Charts**: Distribution of skills by category
- **Word Clouds**: Visual representation of candidate skills
- **Comparison Tables**: Side-by-side candidate comparisons
- **Downloadable Reports**: JSON and CSV export options

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **NLP**: spaCy, NLTK
- **Machine Learning**: scikit-learn, fuzzywuzzy
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly, matplotlib, WordCloud
- **File Processing**: PyPDF2, python-docx
- **Text Analysis**: textstat

## 📁 Project Structure

```
ResumeScreener/
├── Resumescreener/
│   ├── app.py                 # Main Streamlit application
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py     # AI analysis engine
│   │   ├── text_extractor.py  # File text extraction
│   │   └── visualizer.py      # Data visualization
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py         # Helper functions
│   ├── data/
│   │   └── skills_database.json  # Skills database
│   └── requirements.txt       # Python dependencies
├── web_app/                   # Alternative web app version
├── samples/                   # Sample resume files
└── resumes/                   # Test resume files
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayankhan2021/resume-screener.git
   cd resume-screener
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd Resumescreener
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

### Single Resume Analysis
1. Launch the application
2. Upload a resume file (PDF, DOCX, or TXT)
3. Optionally provide a job description for better matching
4. View comprehensive analysis results with visualizations
5. Download detailed reports in JSON format

### Batch Processing
1. Enable "Batch Processing Mode" in the sidebar
2. Upload multiple resume files (up to 5 files)
3. Compare candidates side-by-side
4. Export comparison results as CSV

### Job Description Matching
1. Paste job description in the sidebar
2. Upload candidate resumes
3. Get job-specific fit scores and recommendations
4. View priority skills analysis

## 🎯 Scoring System

The application uses a comprehensive scoring system based on:

- **Skills Match** (30-50%): Relevance to job requirements
- **Experience** (15-35%): Years of relevant experience
- **Education** (10-20%): Educational background and CGPA
- **Job Fit** (0-50%): Compatibility with job description (when provided)
- **Readability** (5-20%): Resume structure and clarity

## 📊 Supported Job Roles

The system is optimized for:
- Market Research Analyst
- Business Consultant
- Data Analyst
- Training Specialist
- General positions

## 🔧 Configuration

### Skills Database
The application uses a comprehensive skills database (`data/skills_database.json`) covering:
- Programming languages
- Web technologies
- Databases and cloud platforms
- Market research tools
- Business consulting skills
- Soft skills and certifications

### Customization
- Modify scoring weights in [`ai_analyzer.py`](Resumescreener/components/ai_analyzer.py)
- Add new job roles and skill categories
- Adjust visualization themes in [`visualizer.py`](Resumescreener/components/visualizer.py)

## 🤖 AI Features

### Advanced NLP Analysis
- Entity extraction using spaCy
- Fuzzy string matching for skill identification
- TF-IDF vectorization for job description matching
- Statistical analysis of resume content

### Machine Learning Components
- Cosine similarity for job matching
- Feature extraction using scikit-learn
- Text classification for role identification
- Predictive scoring algorithms

## 📈 Sample Results

The application provides detailed analysis including:
- Overall resume score (0-100)
- Skills breakdown by category
- Experience timeline analysis
- Education evaluation
- Job fit assessment
- Improvement recommendations

## 🛡️ File Validation

Built-in validation ensures:
- File size limits (10MB max)
- Supported file formats only
- Error handling for corrupted files
- Secure file processing

## 🔄 Version History

- **v1.0**: Initial release with basic resume screening
- **v1.1**: Added job description matching
- **v1.2**: Implemented batch processing
- **v1.3**: Enhanced AI analysis and visualizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- spaCy team for NLP capabilities
- Streamlit for the web framework
- Contributors to the open-source libraries used

## 📞 Support

For questions or support, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

---

**Note**: This application is designed for HR professionals and recruiters to streamline the resume screening process. It should be used as a tool to assist human decision-making, not replace it entirely.