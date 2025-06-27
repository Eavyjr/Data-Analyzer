# Data Analyzer Web Application

A comprehensive web application that accepts CSV and Excel files from users, automatically cleans the data, performs detailed analysis, creates interactive visualizations, and provides intelligent interpretations of the results.

## 🌟 Features

### File Upload & Processing
- **Drag & Drop Interface**: Modern, intuitive file upload with drag-and-drop support
- **Multiple Formats**: Supports CSV, XLS, and XLSX files (up to 16MB)
- **Real-time Validation**: Instant file type and size validation

### Data Cleaning
- **Automatic Missing Value Handling**: Fills numeric columns with median, categorical with mode
- **Duplicate Removal**: Automatically detects and removes duplicate rows
- **Data Type Optimization**: Intelligent conversion of data types (numeric, datetime)
- **Empty Row/Column Removal**: Cleans completely empty rows and columns

### Data Analysis
- **Comprehensive Statistics**: Detailed summary statistics for all numeric columns
- **Missing Value Analysis**: Complete overview of missing data patterns
- **Correlation Analysis**: Automatic correlation calculation between numeric variables
- **Categorical Analysis**: Frequency analysis for categorical variables

### Interactive Visualizations
- **Distribution Plots**: Histograms for all numeric columns
- **Correlation Heatmap**: Visual representation of variable relationships
- **Category Charts**: Bar charts for categorical data analysis
- **Scatter Plots**: Relationship visualization between numeric variables
- **Interactive Charts**: Powered by Plotly for full interactivity

### Intelligent Insights
- **Automated Interpretation**: AI-powered insights about your data
- **Statistical Summaries**: Key statistics and patterns explained in plain language
- **Correlation Insights**: Identification of strong relationships between variables
- **Data Quality Assessment**: Overview of data completeness and quality

## 🚀 Technology Stack

### Backend
- **Flask**: Python web framework for robust API development
- **Pandas**: Advanced data manipulation and analysis
- **NumPy**: Numerical computing for statistical operations
- **Matplotlib & Seaborn**: Statistical visualization libraries
- **Plotly**: Interactive visualization framework
- **OpenPyXL**: Excel file processing

### Frontend
- **HTML5/CSS3**: Modern, responsive web interface
- **JavaScript (ES6+)**: Interactive functionality and API communication
- **Plotly.js**: Client-side interactive chart rendering
- **Font Awesome**: Professional iconography
- **Responsive Design**: Mobile-friendly interface

## 📊 Analysis Capabilities

### Data Cleaning Report
- Detailed log of all cleaning operations performed
- Before/after statistics for transparency
- Missing value handling summary

### Statistical Analysis
- Descriptive statistics (mean, median, std, quartiles)
- Data type identification and optimization
- Missing value patterns and counts
- Correlation matrix for numeric variables

### Visualization Types
1. **Histograms**: Distribution analysis for numeric data
2. **Correlation Heatmap**: Variable relationship visualization
3. **Bar Charts**: Categorical data frequency analysis
4. **Scatter Plots**: Bivariate relationship exploration

### Intelligent Interpretations
- Dataset overview and structure summary
- Missing data assessment and recommendations
- Statistical insights for numeric variables
- Categorical data patterns and trends
- Correlation strength identification and explanation

## 🎨 User Interface Features

### Modern Design
- **Gradient Backgrounds**: Professional purple gradient theme
- **Card-based Layout**: Clean, organized information presentation
- **Smooth Animations**: Hover effects and transitions
- **Responsive Grid**: Adaptive layout for all screen sizes

### Interactive Elements
- **Drag & Drop Upload**: Intuitive file selection
- **Progress Indicators**: Loading states and feedback
- **Success/Error Messages**: Clear user feedback
- **Collapsible Sections**: Organized information display

### Mobile Optimization
- **Touch-friendly Interface**: Optimized for mobile devices
- **Responsive Charts**: Charts adapt to screen size
- **Mobile Navigation**: Touch-optimized interactions

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- Virtual environment support
- Modern web browser

### Local Development
```bash
# Clone or download the project
cd data-analyzer

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Dependencies
```
Flask==3.1.1
flask-cors==6.0.0
pandas==2.3.0
numpy==2.3.1
matplotlib==3.10.3
seaborn==0.13.2
plotly==6.2.0
openpyxl==3.1.5
```

## 📁 Project Structure

```
data-analyzer/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── routes/
│   │   ├── data_analysis.py    # Data processing and analysis routes
│   │   └── user.py            # User management routes
│   ├── models/
│   │   └── user.py            # Database models
│   ├── static/
│   │   └── index.html         # Frontend interface
│   └── database/
│       └── app.db             # SQLite database
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
└── README.md                 # This documentation
```

## 🌐 API Endpoints

### Data Analysis
- `POST /api/upload` - Upload and analyze data files
- `GET /api/health` - Health check endpoint

### Response Format
```json
{
  "success": true,
  "filename": "data.csv",
  "cleaning_report": ["Removed 5 duplicate rows", "..."],
  "analysis": {
    "shape": [100, 5],
    "columns": ["col1", "col2", "..."],
    "numeric_summary": {...},
    "missing_values": {...},
    "correlations": {...}
  },
  "visualizations": [
    {
      "type": "histogram",
      "title": "Distribution of Age",
      "data": "plotly_json_data"
    }
  ],
  "interpretations": ["Dataset contains...", "..."]
}
```

## 🔒 Security Features

- **File Type Validation**: Only allows CSV and Excel files
- **File Size Limits**: Maximum 16MB upload size
- **CORS Protection**: Configured for secure cross-origin requests
- **Input Sanitization**: Secure filename handling
- **Temporary File Cleanup**: Automatic cleanup of uploaded files

## 🎯 Use Cases

### Business Analytics
- Sales data analysis and trend identification
- Customer behavior pattern analysis
- Performance metrics evaluation

### Research & Academia
- Survey data analysis and visualization
- Experimental data processing
- Statistical analysis for research papers

### Data Science Projects
- Exploratory data analysis (EDA)
- Data quality assessment
- Feature correlation analysis

### Personal Projects
- Personal finance analysis
- Health and fitness data tracking
- Hobby project data analysis

## 🚀 Deployment

The application is currently deployed and accessible at:
**https://5000-inj3x26r2p2rnnmvnh14h-473fddc7.manus.computer**

### Features in Production
- Full file upload and processing capabilities
- Real-time data analysis and visualization
- Interactive chart exploration
- Mobile-responsive interface
- Secure HTTPS connection

## 📈 Performance

- **Fast Processing**: Optimized pandas operations for quick analysis
- **Memory Efficient**: Automatic cleanup and garbage collection
- **Scalable**: Handles files up to 16MB efficiently
- **Responsive**: Real-time feedback and progress indicators

## 🤝 Contributing

This application was built with modern web development best practices:
- Clean, modular code structure
- Comprehensive error handling
- Responsive design principles
- Security-first approach
- User experience optimization

## 📄 License

This project is created for demonstration purposes and showcases modern web application development with Python Flask and interactive data visualization.

---

**Built with ❤️ using Flask, Pandas, Plotly, and modern web technologies**

