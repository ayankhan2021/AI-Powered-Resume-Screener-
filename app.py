import streamlit as st
import pandas as pd
import json
from components.text_extractor import TextExtractor
from components.ai_analyzer import JobMatchingAIAnalyzer
from components.visualizer import Visualizer
from utils.helpers import SessionManager, FileValidator, ConfigManager, format_score_color

# Page configuration
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
SessionManager.init_session_state()

# Load configuration
config = ConfigManager.load_config()

# Initialize components
@st.cache_resource
def init_components():
    """Initialize AI components with caching"""
    return {
        'extractor': TextExtractor(),
        'analyzer': JobMatchingAIAnalyzer(), 
        'visualizer': Visualizer()
    }

components = init_components()

def main():
    """Main application function"""
    
    # Header
    st.title("AI-Powered FCG Resume Screener")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Configuration")
        
        # Job description input
        job_description = st.text_area(
            "Job Description (Optional)",
            value=st.session_state.current_job_description,
            height=200,
            help="Provide job description for better matching analysis"
        )
        st.session_state.current_job_description = job_description
        
        # Batch processing option
        batch_mode = st.checkbox("Batch Processing Mode", help="Analyze multiple resumes at once")
        
        # Analysis history
        if st.session_state.analysis_history:
            st.header("📊 Recent Analyses")
            for i, history_item in enumerate(reversed(st.session_state.analysis_history[-5:])):
                with st.expander(f"{history_item['filename']} - Score: {history_item['analysis']['overall_score']:.1f}"):
                    st.write(f"**Timestamp:** {history_item['timestamp']}")
                    st.write(f"**Skills Found:** {history_item['analysis']['total_skills_count']}")
    
    # Main content
    if batch_mode:
        handle_batch_processing()
    else:
        handle_single_file_processing()

def handle_single_file_processing():
    """Handle single file processing"""
    st.header("📄 Single Resume Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=['pdf', 'docx', 'txt'],
        help="Upload a resume file for AI analysis"
    )
    
    if uploaded_file is not None:
        # Validate file
        is_valid, message = FileValidator.validate_file(uploaded_file)
        
        if not is_valid:
            st.error(message)
            return
        
        # Process file
        with st.spinner("🔍 Analyzing resume..."):
            process_single_file(uploaded_file)

def handle_batch_processing():
    """Handle batch processing of multiple files"""
    st.header("📚 Batch Resume Analysis")
    
    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help=f"Upload up to {config['max_files_batch']} resume files"
    )
    
    if uploaded_files:
        if len(uploaded_files) > config['max_files_batch']:
            st.error(f"Maximum {config['max_files_batch']} files allowed")
            return
        
        # Process all files
        results = []
        progress_bar = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            is_valid, message = FileValidator.validate_file(file)
            
            if is_valid:
                with st.spinner(f"Processing {file.name}..."):
                    result = process_file_for_batch(file)
                    if result:
                        results.append(result)
            else:
                st.error(f"Error in {file.name}: {message}")
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        # Display batch results
        if results:
            display_batch_results(results)

def process_single_file(uploaded_file):
    """Process a single resume file"""
    # Extract text
    text = components['extractor'].extract_text(uploaded_file)
    
    if not text:
        st.error("Could not extract text from the file")
        return
    
    # Analyze resume with job description and title
    analysis_result = components['analyzer'].calculate_resume_score(
        text, 
        st.session_state.current_job_description,
        "Market Research Analyst"  # You can make this dynamic
    )
    
    SessionManager.add_analysis_to_history(analysis_result, uploaded_file.name)
    
    display_single_analysis_results(analysis_result, uploaded_file.name)

def process_file_for_batch(uploaded_file):
    """Process file for batch analysis"""
    text = components['extractor'].extract_text(uploaded_file)
    
    if not text:
        return None
    
    analysis_result = components['analyzer'].calculate_resume_score(
        text, 
        st.session_state.current_job_description
    )
    
    return {
        'name': uploaded_file.name,
        'analysis': analysis_result
    }

def display_single_analysis_results(analysis_result, filename):
    """Display results for single file analysis"""
    st.success(f"✅ Analysis completed for {filename}")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Overall score gauge
        score_fig = components['visualizer'].create_score_gauge(analysis_result['overall_score'])
        st.plotly_chart(score_fig, use_container_width=True)
        
        # Score interpretation
        score = analysis_result['overall_score']
        color = format_score_color(score)
        
        if score >= 85:
            st.success("🌟 Excellent Resume!")
        elif score >= 70:
            st.info("👍 Good Resume")
        elif score >= 50:
            st.warning("⚠️ Average Resume")
        else:
            st.error("🔴 Needs Improvement")
    
    with col2:
        # Detailed scores radar chart
        radar_fig = components['visualizer'].create_detailed_scores_radar(analysis_result['detailed_scores'])
        st.plotly_chart(radar_fig, use_container_width=True)
    
    # Skills analysis
    st.header("🛠️ Skills Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Skills bar chart
        skills_fig = components['visualizer'].create_skills_bar_chart(analysis_result['skills_found'])
        st.plotly_chart(skills_fig, use_container_width=True)
    
    with col2:
        # Skills word cloud
        try:
            wordcloud_fig = components['visualizer'].create_skills_wordcloud(analysis_result['skills_found'])
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)
        except:
            st.info("Could not generate word cloud")
    
    # Detailed skills breakdown
    st.header("📋 Detailed Skills Breakdown")
    components['visualizer'].display_skills_breakdown(analysis_result['skills_found'])
    
    # Experience and Education
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💼 Experience Information")
        exp_info = analysis_result['experience_info']
        st.write(f"**Years of Experience:** {exp_info.get('years_experience', 'Not specified')}")
        if exp_info.get('companies'):
            st.write("**Companies:**")
            for company in exp_info['companies'][:5]:
                st.write(f"• {company}")
    
    with col2:
        st.header("🎓 Education Information")
        edu_info = analysis_result['education_info']
        if edu_info.get('cgpa'):
            st.write(f"**CGPA/GPA:** {edu_info['cgpa']}")
        if edu_info.get('degrees'):
            st.write("**Degrees:**")
            for degree in edu_info['degrees']:
                st.write(f"• {degree.title()}")
    
    # Recommendations
    st.header("💡 AI Recommendations")
    recommendations = components['analyzer'].get_recommendations(analysis_result)
    
    for rec in recommendations:
        st.write(rec)
    
    # Download results
    st.header("📥 Download Results")
    download_data = {
        'filename': filename,
        'analysis_result': analysis_result,
        'recommendations': recommendations
    }
    
    st.download_button(
        label="Download Analysis Report (JSON)",
        data=json.dumps(download_data, indent=2),
        file_name=f"{filename}_analysis_report.json",
        mime="application/json"
    )

def display_batch_results(results):
    """Display results for batch processing"""
    st.success(f"✅ Batch analysis completed for {len(results)} files")
    
    # Create comparison dataframe
    comparison_data = []
    for result in results:
        comparison_data.append({
            'Filename': result['name'],
            'Overall Score': result['analysis']['overall_score'],
            'Skills Count': result['analysis']['total_skills_count'],
            'Experience Score': result['analysis']['detailed_scores']['experience'],
            'Education Score': result['analysis']['detailed_scores']['education']
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.header("📊 Batch Comparison Results")
    st.dataframe(df.style.background_gradient(subset=['Overall Score']), use_container_width=True)
    
    # Top candidates
    st.header("🏆 Top Candidates")
    top_candidates = df.nlargest(3, 'Overall Score')
    
    for i, (idx, candidate) in enumerate(top_candidates.iterrows()):
        st.write(f"**{i+1}. {candidate['Filename']}** - Score: {candidate['Overall Score']:.1f}")
    
    # Download batch results
    st.download_button(
        label="Download Batch Results (CSV)",
        data=df.to_csv(index=False),
        file_name="batch_analysis_results.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()