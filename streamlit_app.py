"""
COVID-19 Data Explorer - Streamlit Application

Interactive web application for exploring COVID-19 research data
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import numpy as np
from data_analysis import CORD19Analyzer
import io
import base64

# Configure page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data(sample_size=1000):
    """Load and process data with caching"""
    analyzer = CORD19Analyzer()
    analyzer.load_data(sample_size=sample_size)
    analyzer.clean_data()
    return analyzer

def create_year_chart(df, year_range):
    """Create interactive year-based publication chart"""
    # Filter data by year range
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    year_counts = filtered_df['year'].value_counts().sort_index()
    
    # Create plotly chart
    fig = px.bar(
        x=year_counts.index, 
        y=year_counts.values,
        title=f"COVID-19 Research Publications ({year_range[0]}-{year_range[1]})",
        labels={'x': 'Year', 'y': 'Number of Publications'},
        color=year_counts.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        title_font_size=16
    )
    
    return fig, year_counts

def create_journal_chart(df, top_n):
    """Create interactive journal chart"""
    journal_counts = df['journal'].value_counts().head(top_n)
    
    fig = px.bar(
        x=journal_counts.values,
        y=journal_counts.index,
        orientation='h',
        title=f"Top {top_n} Journals Publishing COVID-19 Research",
        labels={'x': 'Number of Publications', 'y': 'Journal'},
        color=journal_counts.values,
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        showlegend=False,
        height=max(400, top_n * 30),
        title_font_size=16
    )
    
    return fig, journal_counts

def create_source_chart(df):
    """Create source distribution pie chart"""
    source_col = 'source_x' if 'source_x' in df.columns else 'source'
    if source_col not in df.columns:
        return None, None
    
    source_counts = df[source_col].value_counts()
    
    fig = px.pie(
        values=source_counts.values,
        names=source_counts.index,
        title="Distribution of Papers by Source"
    )
    
    fig.update_layout(height=400, title_font_size=16)
    
    return fig, source_counts

def create_wordcloud_image(df):
    """Create word cloud image"""
    import re
    
    # Combine all titles
    all_titles = ' '.join(df['title'].astype(str))
    
    # Clean text
    all_titles = re.sub(r'[^\w\s]', ' ', all_titles.lower())
    
    # Create word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        max_words=100,
        colormap='viridis'
    ).generate(all_titles)
    
    return wordcloud

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🦠 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Interactive exploration of COVID-19 research papers metadata
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("🔧 Controls")
    
    # Sample size selector
    sample_size = st.sidebar.slider(
        "Dataset Sample Size",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="Select the number of papers to analyze (larger samples take more time)"
    )
    
    # Load data
    with st.spinner("Loading and processing data..."):
        analyzer = load_and_process_data(sample_size)
        df = analyzer.cleaned_df
    
    if df is None or df.empty:
        st.error("Failed to load data. Please check your data source.")
        return
    
    # Year range selector
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Select the range of years to analyze"
    )
    
    # Top N journals selector
    top_n_journals = st.sidebar.slider(
        "Number of Top Journals",
        min_value=5,
        max_value=20,
        value=10,
        help="Select how many top journals to display"
    )
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    # Key metrics
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    with col1:
        st.metric(
            label="📄 Total Papers",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        st.metric(
            label="📅 Year Range",
            value=f"{year_range[1] - year_range[0] + 1} years",
            delta=f"{year_range[0]}-{year_range[1]}"
        )
    
    with col3:
        st.metric(
            label="📚 Unique Journals",
            value=filtered_df['journal'].nunique()
        )
    
    with col4:
        avg_title_length = filtered_df['title_word_count'].mean()
        st.metric(
            label="📝 Avg Title Length",
            value=f"{avg_title_length:.1f} words"
        )
    
    # Visualizations
    st.markdown("---")
    
    # Publications by year
    st.subheader("📈 Publications Over Time")
    year_fig, year_counts = create_year_chart(df, year_range)
    st.plotly_chart(year_fig, use_container_width=True)
    
    # Show year statistics
    if not year_counts.empty:
        peak_year = year_counts.index[0]
        peak_count = year_counts.iloc[0]
        st.markdown(f"""
        <div class="insight-box">
            <strong>📊 Insight:</strong> Peak publication year was <strong>{peak_year}</strong> 
            with <strong>{peak_count:,}</strong> papers published.
        </div>
        """, unsafe_allow_html=True)
    
    # Two column layout for next visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Top Publishing Journals")
        journal_fig, journal_counts = create_journal_chart(filtered_df, top_n_journals)
        st.plotly_chart(journal_fig, use_container_width=True)
        
        # Show top journal
        if not journal_counts.empty:
            top_journal = journal_counts.index[0]
            top_count = journal_counts.iloc[0]
            st.markdown(f"""
            <div class="insight-box">
                <strong>🏆 Top Journal:</strong> <em>{top_journal}</em><br>
                <strong>Publications:</strong> {top_count:,}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Distribution by Source")
        source_fig, source_counts = create_source_chart(filtered_df)
        if source_fig:
            st.plotly_chart(source_fig, use_container_width=True)
            
            # Show source statistics
            if source_counts is not None and not source_counts.empty:
                top_source = source_counts.index[0]
                top_source_count = source_counts.iloc[0]
                st.markdown(f"""
                <div class="insight-box">
                    <strong>📚 Primary Source:</strong> {top_source}<br>
                    <strong>Papers:</strong> {top_source_count:,} ({top_source_count/len(filtered_df)*100:.1f}%)
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Source information not available in the dataset")
    
    # Word cloud
    st.subheader("☁️ Most Frequent Words in Titles")
    
    try:
        wordcloud = create_wordcloud_image(filtered_df)
        
        # Convert wordcloud to image
        img_buffer = io.BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        st.image(img_buffer, use_column_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 Word Cloud Insight:</strong> This visualization shows the most frequently 
            used words in paper titles, helping identify key research themes and topics.
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Could not generate word cloud: {str(e)}")
        st.info("Word cloud generation requires additional dependencies")
    
    # Data sample
    st.markdown("---")
    st.subheader("📋 Sample Data")
    
    # Show sample of filtered data
    sample_df = filtered_df.head(10)[['title', 'journal', 'year', 'title_word_count']]
    st.dataframe(sample_df, use_container_width=True)
    
    # Download option
    st.subheader("💾 Download Data")
    
    # Create download button for filtered data
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"cord19_filtered_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dataset Overview:**")
        st.write(f"• Total papers analyzed: {len(filtered_df):,}")
        st.write(f"• Date range: {year_range[0]} - {year_range[1]}")
        st.write(f"• Unique journals: {filtered_df['journal'].nunique()}")
        st.write(f"• Average title length: {filtered_df['title_word_count'].mean():.1f} words")
    
    with col2:
        st.markdown("**Key Findings:**")
        if not year_counts.empty:
            st.write(f"• Peak year: {year_counts.index[0]} ({year_counts.iloc[0]:,} papers)")
        if not journal_counts.empty:
            st.write(f"• Top journal: {journal_counts.index[0]}")
        st.write("• Research spans multiple disciplines")
        st.write("• Rapid growth during pandemic period")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>📚 Python Frameworks Assignment - CORD-19 Data Analysis</p>
        <p>Built with Streamlit, Pandas, and Plotly</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
