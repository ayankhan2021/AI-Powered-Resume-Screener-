import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import Dict, List

class Visualizer:
    """Create visualizations for resume analysis results"""
    
    @staticmethod
    def create_score_gauge(score: float) -> go.Figure:
        """Create a gauge chart for overall score"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Resume Score"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300, font={'size': 16})
        return fig
    
    @staticmethod
    def create_skills_bar_chart(skills_data: Dict[str, List[str]]) -> go.Figure:
        """Create bar chart for skills by category"""
        categories = []
        counts = []
        
        for category, skills in skills_data.items():
            categories.append(category.replace('_', ' ').title())
            counts.append(len(skills))
        
        fig = px.bar(
            x=categories,
            y=counts,
            title="Skills Distribution by Category",
            labels={'x': 'Skill Category', 'y': 'Number of Skills'},
            color=counts,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    @staticmethod
    def create_detailed_scores_radar(scores: Dict[str, float]) -> go.Figure:
        """Create radar chart for detailed scores"""
        categories = [key.replace('_', ' ').title() for key in scores.keys()]
        values = list(scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Score',
            line_color='blue'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Detailed Score Analysis",
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_skills_wordcloud(skills_data: Dict[str, List[str]]) -> plt.Figure:
        """Create word cloud for skills"""
        all_skills = []
        for skills_list in skills_data.values():
            all_skills.extend(skills_list)
        
        if not all_skills:
            return None
        
        skills_text = ' '.join(all_skills)
        
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(skills_text)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.title('Skills Word Cloud', fontsize=16, fontweight='bold')
        
        return fig
    
    @staticmethod
    def create_comparison_chart(candidates_data: List[Dict]) -> go.Figure:
        """Create comparison chart for multiple candidates"""
        if len(candidates_data) < 2:
            return None
        
        df = pd.DataFrame(candidates_data)
        
        fig = px.bar(
            df,
            x='name',
            y='overall_score',
            title="Candidates Comparison",
            labels={'name': 'Candidate', 'overall_score': 'Overall Score'},
            color='overall_score',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(height=400)
        return fig
    
    @staticmethod
    def display_skills_breakdown(skills_data: Dict[str, List[str]]):
        """Display skills breakdown in expandable sections"""
        for category, skills in skills_data.items():
            if skills:
                with st.expander(f"{category.replace('_', ' ').title()} ({len(skills)} skills)"):
                    cols = st.columns(3)
                    for i, skill in enumerate(skills):
                        with cols[i % 3]:
                            st.write(f"• {skill.title()}")