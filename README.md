# BYU-Idaho Sentiment Analysis Tool

<div align="center">
  **Professional Sentiment Analysis for Customer Satisfaction Surveys**
  
  *A comprehensive web-based application for BYU-Idaho employees to analyze customer feedback and satisfaction surveys*
</div>

---

## 📋 Overview

The BYU-Idaho Sentiment Analysis Tool is an enterprise-grade web application designed specifically for BYU-Idaho employees to analyze customer satisfaction surveys, feedback forms, and other text-based responses. This tool provides professional-grade sentiment analysis with interactive visualizations and comprehensive reporting capabilities.

### 🎯 **Primary Use Cases**

- **Customer Satisfaction Surveys** - Analyze student, parent, and stakeholder feedback
- **Course Evaluations** - Understand sentiment in student course feedback
- **Employee Feedback** - Process internal survey responses
- **Event Feedback** - Analyze satisfaction from university events and programs
- **General Text Analysis** - Any text-based feedback or survey responses

---

## ✨ Features

### 🔍 **Intelligent Analysis**

- **Interactive Column Selection** - Choose any column from your Excel file for analysis
- **State-of-the-Art AI** - Uses RoBERTa model trained specifically for sentiment analysis
- **Flexible Input** - Supports various Excel formats (.xlsx, .xls)
- **Real-time Preview** - See your data before processing

### 📊 **Professional Reporting**

- **Multiple Visualizations** - Bar charts, pie charts, confidence analysis
- **Statistical Insights** - Comprehensive metrics and confidence scores
- **BYUI Branded** - Professional styling with official university colors
- **Export Ready** - Download analyzed results in Excel format

### 🗄️ **Data Management**

- **History Tracking** - View all previous analysis runs
- **Secure Storage** - Local SQLite database for analysis history
- **Easy Retrieval** - Download previous results anytime
- **Data Privacy** - All processing happens locally on your machine

### 🎨 **User Experience**

- **Intuitive Interface** - Web-based, easy-to-use design
- **Drag & Drop Upload** - Simple file upload process
- **Responsive Design** - Works on desktop, tablet, and mobile
- **No Technical Skills Required** - Point-and-click operation

---

## 🚀 Quick Start for BYU-Idaho Employees

### Run from Source (For IT/Developers)

```bash
# Clone the repository
git clone https://github.com/BYUI-Information-Technology/CSAT-Sentiment-Analysis-Tool.git
cd sentiment-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

```

Then **Open** your web browser to `http://localhost:5001`

---

## 📖 User Guide

### Step 1: Upload Your Survey Data

- Click **"Choose File"** or drag your Excel file to the upload area
- Supported formats: `.xlsx`, `.xls`
- Maximum file size: 16MB

### Step 2: Preview and Select Column

- Review your data in the preview table
- Select the column containing text responses you want to analyze
- Common column names: "Comments", "Feedback", "Response", "Why satisfied text area"

### Step 3: Run Analysis

- Click **"Analyze Sentiment"** to start processing
- The AI model will analyze each response for sentiment (Positive, Negative, Neutral)
- Processing time depends on the number of responses

### Step 4: Review Results

- View comprehensive charts and statistics
- Understand sentiment distribution across your responses
- See confidence scores for each analysis

### Step 5: Download and Share

- Download the complete Excel file with sentiment scores
- Share insights with your team or stakeholders
- Access previous analyses from the History page

---

## 🔧 System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Memory**: 4GB RAM (2GB minimum)
- **Storage**: 2GB free space
- **Internet**: Required for initial setup (model download)

### Recommended for Large Surveys

- **Memory**: 8GB+ RAM
- **Processor**: Multi-core CPU
- **Storage**: 5GB+ free space

---

## 🛡️ Data Privacy & Security

- **Local Processing**: All data stays on your machine
- **No Cloud Upload**: Survey data never leaves your computer
- **Secure Storage**: Local SQLite database for history
- **FERPA Compliant**: Suitable for educational data analysis
- **No External APIs**: Model runs entirely offline after initial download

---

## 🎨 BYUI Branding

This application uses official BYU-Idaho brand colors and styling:

- **Primary Blue**: #006EB6
- **Secondary Blue**: #214491
- **Accent Blue**: #4F9ACF
- **Light Blue**: #A0D4ED

---

## 📞 Support & Help

### For BYU-Idaho Employees

- **Internal Help Desk**: Contact IT Services for technical support
- **Training Materials**: Available through internal training resources
- **Documentation**: Comprehensive guides included with installation

### For IT Administrators

- **Deployment Guide**: See `DISTRIBUTION.md` for enterprise deployment
- **Network Requirements**: Outbound HTTPS for initial model download
- **Port Requirements**: Application runs on port 5001 locally

---

## 🔄 Updates & Maintenance

### Automatic Updates

- The AI model updates automatically as needed
- Application updates available through GitHub releases

### Manual Updates

- Download latest release from GitHub
- Replace existing installation
- All data and history preserved

---

## 📋 Technical Specifications

### AI Model

- **Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Type**: RoBERTa-based transformer
- **Languages**: English
- **Output**: Positive, Negative, Neutral with confidence scores

### Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Charts**: Matplotlib, Seaborn
- **ML Framework**: Hugging Face Transformers

---

## 📚 Documentation

- `README.md` - This overview and user guide
- `DISTRIBUTION.md` - Deployment and distribution guide
- `requirements.txt` - Python dependencies
- `templates/` - Web interface templates

---

## 📄 License & Compliance

This tool is developed for internal BYU-Idaho use and complies with:

- Educational data privacy requirements
- University IT security policies
- Open source software licensing

---

## 🤝 Contributing

This is an internal BYU-Idaho project. For contributions or improvements:

1. Contact the IT Development team
2. Submit issues through internal channels
3. Follow university development guidelines

---

<div align="center">
  <strong>Developed for BYU-Idaho | Customer Satisfaction & Survey Analysis</strong><br>
  <em>Empowering data-driven decisions through intelligent sentiment analysis</em>
</div>
