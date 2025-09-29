"""
Quick Start Script for CORD-19 Analysis
Python Frameworks Assignment

This script provides a simple way to run both the analysis and Streamlit app
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'pandas', 'matplotlib', 'seaborn', 'streamlit', 
        'wordcloud', 'numpy', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def run_analysis():
    """Run the data analysis script"""
    print("="*60)
    print("RUNNING DATA ANALYSIS")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, "data_analysis.py"], check=True)
        print("\n✅ Data analysis completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running analysis: {e}")
        return False
    except FileNotFoundError:
        print("❌ data_analysis.py not found in current directory")
        return False
    
    return True

def run_streamlit_app():
    """Launch the Streamlit application"""
    print("\n" + "="*60)
    print("LAUNCHING STREAMLIT APPLICATION")
    print("="*60)
    print("The app will open in your default web browser...")
    print("URL: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("="*60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running Streamlit app: {e}")
        return False
    except FileNotFoundError:
        print("❌ streamlit_app.py not found in current directory")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 Streamlit application stopped by user")
        return True
    
    return True

def main():
    """Main function with user menu"""
    print("🦠 CORD-19 Data Analysis Project")
    print("Python Frameworks Assignment")
    print("="*50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Run data analysis script")
        print("2. Launch Streamlit web application")
        print("3. Run analysis then launch app")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_analysis()
        
        elif choice == "2":
            run_streamlit_app()
        
        elif choice == "3":
            if run_analysis():
                input("\nPress Enter to launch the Streamlit app...")
                run_streamlit_app()
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
