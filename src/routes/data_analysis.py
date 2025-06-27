import os
import io
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

data_analysis_bp = Blueprint('data_analysis', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
UPLOAD_FOLDER = '/tmp/uploads'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_data(df):
    """Clean the uploaded data"""
    cleaning_report = []
    
    # Remove completely empty rows and columns
    initial_shape = df.shape
    df = df.dropna(how='all').dropna(axis=1, how='all')
    if df.shape != initial_shape:
        cleaning_report.append(f"Removed empty rows/columns. Shape changed from {initial_shape} to {df.shape}")
    
    # Handle missing values
    missing_before = df.isnull().sum().sum()
    if missing_before > 0:
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
                else:
                    df[col].fillna('Unknown', inplace=True)
        
        missing_after = df.isnull().sum().sum()
        cleaning_report.append(f"Filled {missing_before - missing_after} missing values")
    
    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        cleaning_report.append(f"Removed {duplicates} duplicate rows")
    
    # Convert data types appropriately
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try to convert to numeric if possible
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
            
            # Try to convert to datetime if possible
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
    
    return df, cleaning_report

def analyze_data(df):
    """Perform basic data analysis"""
    analysis = {}
    
    # Basic info
    analysis['shape'] = df.shape
    analysis['columns'] = list(df.columns)
    analysis['dtypes'] = df.dtypes.astype(str).to_dict()
    
    # Summary statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        analysis['numeric_summary'] = df[numeric_cols].describe().to_dict()
    
    # Missing values
    analysis['missing_values'] = df.isnull().sum().to_dict()
    
    # Categorical analysis
    categorical_cols = df.select_dtypes(include=['object']).columns
    categorical_info = {}
    for col in categorical_cols:
        if len(df[col].unique()) <= 20:  # Only for columns with reasonable number of categories
            categorical_info[col] = df[col].value_counts().head(10).to_dict()
    analysis['categorical_summary'] = categorical_info
    
    # Correlations for numeric data
    if len(numeric_cols) > 1:
        correlation_matrix = df[numeric_cols].corr()
        analysis['correlations'] = correlation_matrix.to_dict()
    
    return analysis

def create_visualizations(df):
    """Create various visualizations"""
    visualizations = []
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # 1. Distribution plots for numeric columns
    for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
        fig = px.histogram(df, x=col, title=f'Distribution of {col}')
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        visualizations.append({
            'type': 'histogram',
            'title': f'Distribution of {col}',
            'data': graph_json
        })
    
    # 2. Correlation heatmap
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, 
                       title='Correlation Heatmap',
                       color_continuous_scale='RdBu_r',
                       aspect='auto')
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        visualizations.append({
            'type': 'heatmap',
            'title': 'Correlation Heatmap',
            'data': graph_json
        })
    
    # 3. Bar charts for categorical columns
    for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
        if len(df[col].unique()) <= 20:
            value_counts = df[col].value_counts().head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values,
                        title=f'Top Categories in {col}',
                        labels={'x': col, 'y': 'Count'})
            graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
            visualizations.append({
                'type': 'bar',
                'title': f'Top Categories in {col}',
                'data': graph_json
            })
    
    # 4. Scatter plots for numeric pairs
    if len(numeric_cols) >= 2:
        col1, col2 = numeric_cols[0], numeric_cols[1]
        fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}')
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        visualizations.append({
            'type': 'scatter',
            'title': f'{col1} vs {col2}',
            'data': graph_json
        })
    
    return visualizations

def interpret_results(df, analysis):
    """Generate interpretations of the analysis results"""
    interpretations = []
    
    # Dataset overview
    interpretations.append(f"Dataset contains {analysis['shape'][0]} rows and {analysis['shape'][1]} columns.")
    
    # Missing values interpretation
    total_missing = sum(analysis['missing_values'].values())
    if total_missing > 0:
        interpretations.append(f"Found {total_missing} missing values across the dataset.")
    else:
        interpretations.append("No missing values found in the dataset.")
    
    # Numeric data insights
    if 'numeric_summary' in analysis:
        numeric_cols = list(analysis['numeric_summary'].keys())
        interpretations.append(f"Dataset contains {len(numeric_cols)} numeric columns: {', '.join(numeric_cols)}")
        
        # Check for outliers (values beyond 3 standard deviations)
        for col in numeric_cols:
            mean_val = analysis['numeric_summary'][col]['mean']
            std_val = analysis['numeric_summary'][col]['std']
            if std_val > 0:
                outlier_threshold = 3 * std_val
                interpretations.append(f"Column '{col}' has mean {mean_val:.2f} and standard deviation {std_val:.2f}")
    
    # Categorical data insights
    if analysis['categorical_summary']:
        cat_cols = list(analysis['categorical_summary'].keys())
        interpretations.append(f"Dataset contains {len(cat_cols)} categorical columns: {', '.join(cat_cols)}")
        
        for col, values in analysis['categorical_summary'].items():
            top_category = max(values, key=values.get)
            interpretations.append(f"Most common value in '{col}' is '{top_category}' with {values[top_category]} occurrences")
    
    # Correlation insights
    if 'correlations' in analysis:
        correlations = analysis['correlations']
        strong_correlations = []
        for col1 in correlations:
            for col2 in correlations[col1]:
                if col1 != col2 and abs(correlations[col1][col2]) > 0.7:
                    strong_correlations.append(f"{col1} and {col2} (r={correlations[col1][col2]:.2f})")
        
        if strong_correlations:
            interpretations.append(f"Strong correlations found between: {', '.join(strong_correlations)}")
        else:
            interpretations.append("No strong correlations (>0.7) found between numeric variables.")
    
    return interpretations

@data_analysis_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and initial processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload CSV or Excel files.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read file based on extension
        file_ext = filename.rsplit('.', 1)[1].lower()
        try:
            if file_ext == 'csv':
                df = pd.read_csv(filepath)
            else:  # xls or xlsx
                df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
        
        # Clean data
        cleaned_df, cleaning_report = clean_data(df)
        
        # Analyze data
        analysis = analyze_data(cleaned_df)
        
        # Create visualizations
        visualizations = create_visualizations(cleaned_df)
        
        # Generate interpretations
        interpretations = interpret_results(cleaned_df, analysis)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'cleaning_report': cleaning_report,
            'analysis': analysis,
            'visualizations': visualizations,
            'interpretations': interpretations
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@data_analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'data-analysis'})

