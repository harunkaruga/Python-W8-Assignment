# COVID-19 Data Analysis Project

This project provides a comprehensive analysis of the CORD-19 research dataset, focusing on COVID-19 research papers. It includes both a command-line analysis script and an interactive Streamlit web application.

## 🎯 Project Overview

This assignment demonstrates fundamental data science skills including:
- Data loading and exploration
- Data cleaning and preprocessing
- Statistical analysis and visualization
- Interactive web application development
- Documentation and code organization

## 📊 Dataset Information

The project analyzes the CORD-19 dataset metadata, which contains:
- Paper titles and abstracts
- Publication dates and journals
- Author information
- Source databases (PMC, Medline, bioRxiv, etc.)

**Note**: If the actual CORD-19 dataset is not available, the application generates realistic sample data for demonstration purposes.

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone or download this repository**
   \`\`\`bash
   git clone <your-repo-url>
   cd Frameworks_Assignment
   \`\`\`

2. **Install required packages**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Download the CORD-19 dataset 
   - Visit: https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
   - Download the `metadata.csv` file
   - Place it in the project root directory

## 🚀 Usage

### Running the Analysis Script

Execute the standalone analysis script:

\`\`\`bash
python data_analysis.py
\`\`\`

This will:
- Load the dataset (or create sample data)
- Perform data exploration and cleaning
- Generate visualizations
- Display summary statistics

### Running the Streamlit Application

Launch the interactive web application:

\`\`\`bash
streamlit run streamlit_app.py
\`\`\`

Then open your browser to `http://localhost:8501`

### Streamlit App Features

The web application provides:
- **Interactive Controls**: Adjust sample size, year range, and number of top journals
- **Real-time Metrics**: Total papers, date ranges, unique journals, average title length
- **Dynamic Visualizations**:
  - Publications over time (bar chart)
  - Top publishing journals (horizontal bar chart)
  - Source distribution (pie chart)
  - Word cloud of paper titles
- **Data Export**: Download filtered datasets as CSV
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

\`\`\`
Frameworks_Assignment/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── data_analysis.py         # Main analysis script
├── streamlit_app.py         # Streamlit web application
├── analysis_report.md       # Detailed findings report
└── metadata.csv            # CORD-19 dataset (if available)
\`\`\`

## 📈 Key Features

### Data Analysis Capabilities
- **Data Loading**: Handles both real CORD-19 data and generates sample data
- **Data Cleaning**: Removes missing values, converts data types, creates derived features
- **Exploratory Analysis**: Basic statistics, missing value analysis, data profiling
- **Visualizations**: Time series, bar charts, pie charts, word clouds

### Interactive Web Application
- **User Controls**: Sliders and selectors for customizing analysis
- **Real-time Updates**: Charts update based on user selections
- **Modern UI**: Clean, professional interface with custom styling
- **Export Functionality**: Download processed data for further analysis

## 🔍 Analysis Results

### Key Findings

1. **Publication Trends**: COVID-19 research showed rapid growth during 2020-2021
2. **Journal Distribution**: Multiple high-impact journals contributed to the research effort
3. **Research Themes**: Analysis reveals key topics through title word frequency
4. **Data Sources**: Papers sourced from various databases (PMC, Medline, preprint servers)

### Visualizations Generated

1. **Publications by Year**: Bar chart showing research output over time
2. **Top Journals**: Horizontal bar chart of most prolific publishers
3. **Source Distribution**: Pie chart of paper sources
4. **Title Word Cloud**: Visual representation of common research themes

## 🧪 Technical Implementation

### Data Processing Pipeline
1. **Loading**: Pandas DataFrame with error handling
2. **Cleaning**: Missing value treatment, data type conversion
3. **Feature Engineering**: Derived columns (year, word counts)
4. **Analysis**: Statistical summaries and aggregations
5. **Visualization**: Multiple chart types using Matplotlib and Plotly

### Web Application Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python data processing with caching
- **Interactivity**: Real-time chart updates based on user input
- **Performance**: Data caching for improved response times


Through this project, the following skills were demonstrated:
- Real-world dataset handling and preprocessing
- Statistical analysis and data exploration techniques
- Data visualization best practices
- Web application development with Streamlit
- Code organization and documentation
- Interactive dashboard creation

## 🔧 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   \`\`\`bash
   pip install --upgrade pip
   pip install -r requirements.txt
   \`\`\`

2. **Dataset Not Found**
   - The application will automatically generate sample data
   - For real data, download metadata.csv from Kaggle

3. **Streamlit Port Issues**
   \`\`\`bash
   streamlit run streamlit_app.py --server.port 8502
   \`\`\`

4. **Memory Issues with Large Datasets**
   - Use the sample size slider to reduce data volume
   - Consider using data chunking for very large files

## 📚 Dependencies

- **pandas**: Data manipulation and analysis
- **matplotlib**: Static plotting and visualization
- **seaborn**: Statistical data visualization
- **streamlit**: Web application framework
- **plotly**: Interactive plotting
- **wordcloud**: Text visualization
- **numpy**: Numerical computing

## 🤝 Contributing

This is an educational project. For improvements or suggestions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request



