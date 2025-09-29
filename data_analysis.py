"""
COVID-19 Data Analysis Script

This script performs basic analysis of the COVID-19 research dataset
including data loading, cleaning, exploration, and visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

class CORD19Analyzer:
    def __init__(self, data_path=None):
        """Initialize the analyzer with optional data path"""
        self.data_path = data_path
        self.df = None
        self.cleaned_df = None
        
    def load_data(self, sample_size=None):
        """
        Load the CORD-19 metadata CSV file
        
        Args:
            sample_size (int): Optional sample size for testing with smaller dataset
        """
        try:
            if self.data_path:
                print("Loading CORD-19 metadata...")
                self.df = pd.read_csv(self.data_path)
                
                if sample_size:
                    self.df = self.df.sample(n=min(sample_size, len(self.df)), random_state=42)
                    print(f"Using sample of {len(self.df)} records")
                
                print(f"Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            else:
                # Create sample data for demonstration
                print("No data path provided. Creating sample data for demonstration...")
                self.create_sample_data()
                
        except FileNotFoundError:
            print("Data file not found. Creating sample data for demonstration...")
            self.create_sample_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            print("Creating sample data for demonstration...")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for demonstration purposes"""
        np.random.seed(42)
        
        # Sample journals
        journals = [
            'Nature', 'Science', 'Cell', 'The Lancet', 'NEJM', 
            'PLOS ONE', 'BMJ', 'JAMA', 'Nature Medicine', 'Cell Host & Microbe'
        ]
        
        # Sample COVID-related keywords for titles
        covid_terms = [
            'COVID-19', 'SARS-CoV-2', 'coronavirus', 'pandemic', 'vaccine',
            'antiviral', 'respiratory', 'infection', 'immunity', 'treatment'
        ]
        
        # Generate sample data
        n_samples = 1000
        data = {
            'cord_uid': [f'cord_{i:06d}' for i in range(n_samples)],
            'title': [
                f"{np.random.choice(covid_terms)} {np.random.choice(['study', 'analysis', 'research', 'investigation'])} "
                f"of {np.random.choice(['patients', 'treatment', 'vaccine', 'therapy', 'diagnosis'])}"
                for _ in range(n_samples)
            ],
            'abstract': [
                f"This study investigates {np.random.choice(covid_terms).lower()} "
                f"in {np.random.choice(['clinical', 'laboratory', 'epidemiological'])} settings. "
                f"Results show significant {np.random.choice(['improvement', 'correlation', 'reduction'])}."
                for _ in range(n_samples)
            ],
            'authors': [
                f"Author{i % 20 + 1}, A.; Author{(i+1) % 20 + 1}, B." 
                for i in range(n_samples)
            ],
            'journal': np.random.choice(journals, n_samples),
            'publish_time': pd.date_range('2020-01-01', '2023-12-31', periods=n_samples),
            'source_x': np.random.choice(['PMC', 'Medline', 'bioRxiv', 'medRxiv'], n_samples)
        }
        
        self.df = pd.DataFrame(data)
        print(f"Sample data created: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
    
    def explore_data(self):
        """Perform basic data exploration"""
        if self.df is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n" + "="*50)
        print("DATA EXPLORATION")
        print("="*50)
        
        # Basic info
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        
        # Data types
        print("\nData Types:")
        print(self.df.dtypes)
        
        # Missing values
        print("\nMissing Values:")
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing_data,
            'Percentage': missing_percent
        })
        print(missing_df[missing_df['Missing Count'] > 0])
        
        # Basic statistics
        print("\nFirst 5 rows:")
        print(self.df.head())
        
        return missing_df
    
    def clean_data(self):
        """Clean and prepare data for analysis"""
        if self.df is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n" + "="*50)
        print("DATA CLEANING")
        print("="*50)
        
        # Create a copy for cleaning
        self.cleaned_df = self.df.copy()
        
        # Handle missing values
        print("Handling missing values...")
        
        # Remove rows with missing titles (essential for analysis)
        initial_rows = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.dropna(subset=['title'])
        print(f"Removed {initial_rows - len(self.cleaned_df)} rows with missing titles")
        
        # Fill missing abstracts with empty string
        self.cleaned_df['abstract'] = self.cleaned_df['abstract'].fillna('')
        
        # Fill missing journal names
        self.cleaned_df['journal'] = self.cleaned_df['journal'].fillna('Unknown Journal')
        
        # Convert publish_time to datetime
        if 'publish_time' in self.cleaned_df.columns:
            self.cleaned_df['publish_time'] = pd.to_datetime(
                self.cleaned_df['publish_time'], errors='coerce'
            )
            
            # Extract year for analysis
            self.cleaned_df['year'] = self.cleaned_df['publish_time'].dt.year
            
            # Remove rows with invalid dates
            self.cleaned_df = self.cleaned_df.dropna(subset=['year'])
        
        # Create additional features
        self.cleaned_df['title_word_count'] = self.cleaned_df['title'].str.split().str.len()
        self.cleaned_df['abstract_word_count'] = self.cleaned_df['abstract'].str.split().str.len()
        
        print(f"Cleaned dataset shape: {self.cleaned_df.shape}")
        print("Data cleaning completed!")
        
        return self.cleaned_df
    
    def analyze_publications_by_year(self):
        """Analyze publication trends by year"""
        if self.cleaned_df is None:
            print("Please clean data first.")
            return None
        
        year_counts = self.cleaned_df['year'].value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        plt.bar(year_counts.index, year_counts.values, color='steelblue', alpha=0.7)
        plt.title('COVID-19 Research Publications by Year', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Publications', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(year_counts.values):
            plt.text(year_counts.index[i], v + max(year_counts.values) * 0.01, 
                    str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        return year_counts
    
    def analyze_top_journals(self, top_n=10):
        """Analyze top publishing journals"""
        if self.cleaned_df is None:
            print("Please clean data first.")
            return None
        
        journal_counts = self.cleaned_df['journal'].value_counts().head(top_n)
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(journal_counts)), journal_counts.values, color='lightcoral')
        plt.yticks(range(len(journal_counts)), journal_counts.index)
        plt.title(f'Top {top_n} Journals Publishing COVID-19 Research', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Publications', fontsize=12)
        plt.ylabel('Journal', fontsize=12)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + max(journal_counts.values) * 0.01, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        plt.show()
        
        return journal_counts
    
    def create_title_wordcloud(self):
        """Create word cloud from paper titles"""
        if self.cleaned_df is None:
            print("Please clean data first.")
            return None
        
        # Combine all titles
        all_titles = ' '.join(self.cleaned_df['title'].astype(str))
        
        # Clean text (remove common words, punctuation)
        all_titles = re.sub(r'[^\w\s]', ' ', all_titles.lower())
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800, height=400, 
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(all_titles)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Frequent Words in Paper Titles', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return wordcloud
    
    def analyze_sources(self):
        """Analyze distribution by source"""
        if self.cleaned_df is None:
            print("Please clean data first.")
            return None
        
        source_col = 'source_x' if 'source_x' in self.cleaned_df.columns else 'source'
        if source_col not in self.cleaned_df.columns:
            print("No source column found in data")
            return None
        
        source_counts = self.cleaned_df[source_col].value_counts()
        
        plt.figure(figsize=(10, 6))
        plt.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=plt.cm.Set3.colors)
        plt.title('Distribution of Papers by Source', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        
        return source_counts
    
    def generate_summary_report(self):
        """Generate a summary report of findings"""
        if self.cleaned_df is None:
            print("Please clean data first.")
            return
        
        print("\n" + "="*60)
        print("SUMMARY REPORT")
        print("="*60)
        
        print(f"Total papers analyzed: {len(self.cleaned_df):,}")
        print(f"Date range: {self.cleaned_df['year'].min():.0f} - {self.cleaned_df['year'].max():.0f}")
        print(f"Number of unique journals: {self.cleaned_df['journal'].nunique()}")
        
        # Top journal
        top_journal = self.cleaned_df['journal'].value_counts().index[0]
        top_journal_count = self.cleaned_df['journal'].value_counts().iloc[0]
        print(f"Most prolific journal: {top_journal} ({top_journal_count} papers)")
        
        # Peak year
        peak_year = self.cleaned_df['year'].value_counts().index[0]
        peak_year_count = self.cleaned_df['year'].value_counts().iloc[0]
        print(f"Peak publication year: {peak_year:.0f} ({peak_year_count} papers)")
        
        # Average title length
        avg_title_length = self.cleaned_df['title_word_count'].mean()
        print(f"Average title length: {avg_title_length:.1f} words")
        
        print("\nKey Insights:")
        print("- COVID-19 research showed rapid growth during the pandemic")
        print("- Multiple journals contributed to the research effort")
        print("- Research spans various aspects of the virus and its impact")

def main():
    """Main function to run the analysis"""
    print("CORD-19 Dataset Analysis")
    print("Python Frameworks Assignment")
    print("="*50)
    
    # Initialize analyzer
    analyzer = CORD19Analyzer()
    
    # Load data (will create sample data if no file provided)
    analyzer.load_data(sample_size=1000)  # Use sample for demonstration
    
    # Explore data
    analyzer.explore_data()
    
    # Clean data
    analyzer.clean_data()
    
    # Perform analyses
    print("\nGenerating visualizations...")
    
    # Publications by year
    analyzer.analyze_publications_by_year()
    
    # Top journals
    analyzer.analyze_top_journals()
    
    # Word cloud
    analyzer.create_title_wordcloud()
    
    # Source distribution
    analyzer.analyze_sources()
    
    # Summary report
    analyzer.generate_summary_report()
    
    print("\nAnalysis completed! Check the generated visualizations.")

if __name__ == "__main__":
    main()
