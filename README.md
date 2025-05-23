# 🤖 Sentiment Analysis Application

A powerful, user-friendly desktop application for analyzing sentiment in Excel data using state-of-the-art AI models.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🧠 **AI-Powered Analysis** - Uses RoBERTa model for accurate sentiment detection
- 🌐 **Beautiful Web Interface** - Modern, responsive design with drag-and-drop file upload
- 📊 **Rich Visualizations** - Interactive charts and graphs for data insights
- 📈 **Comprehensive Analytics** - Confidence scores, statistics, and detailed breakdowns
- 💾 **Export Results** - Download analyzed data with sentiment labels and confidence scores
- 🖥️ **Cross-Platform** - Available as standalone executables for Windows and macOS
- 🚀 **Easy to Use** - No technical knowledge required

## 🎯 Quick Start

### Option 1: Use Pre-built Executable (Recommended)

1. **Download the executable** for your platform
2. **Windows**: Double-click `start_app.bat`
3. **macOS**: Double-click `start_app.sh`
4. **Open browser** and go to `http://localhost:5001`

### Option 2: Run from Source

```bash
# 1. Clone or download the project
git clone <repository-url>
cd sentiment-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open browser to http://localhost:5001
```

### Option 3: Build Your Own Executable

```bash
# Install and build
pip install -r requirements.txt
python build_executable.py
```

## 📋 Requirements

### For Excel Files:

- ✅ File format: `.xlsx` or `.xls`
- ✅ Contains text data for sentiment analysis
- ✅ Maximum file size: 16MB
- ✅ Any number of columns supported - you'll select which one to analyze

### Interactive Column Selection:

The application now features an **interactive preview system** where you can:

- 📊 Preview your Excel data before analysis
- 🎯 Select which column contains the text to analyze
- 👀 See sample values from each column
- ✨ Highlight the selected column for easy identification

### Example Excel Structure:

| Response         | Ticket ID | Ticket              | Survey Completed By | Survey Completed | Requested  | Satisfied Range | Why satisfied text area      |
| ---------------- | --------- | ------------------- | ------------------- | ---------------- | ---------- | --------------- | ---------------------------- |
| Example response | 12345     | Support Request     | John Doe            | 2024-01-15       | 2024-01-10 | Very Satisfied  | "Great service! Love it!"    |
| Example response | 12346     | Technical Issue     | Jane Smith          | 2024-01-16       | 2024-01-12 | Dissatisfied    | "Poor quality, disappointed" |
| Example response | 12347     | Information Request | Bob Johnson         | 2024-01-17       | 2024-01-14 | Neutral         | "It's okay, nothing special" |

## 🎨 What You Get

### 📊 Visualizations

- **Sentiment Distribution Chart** - Bar chart showing count and percentages
- **Sentiment Pie Chart** - Proportional view of sentiment breakdown
- **Confidence Analysis Dashboard** - Multi-panel analysis of prediction confidence
- **Interactive Statistics** - Key insights and trends

### 📈 Data Analysis

- **Sentiment Labels**: POSITIVE, NEGATIVE, NEUTRAL
- **Confidence Scores**: 0.0 to 1.0 (higher = more confident)
- **Statistical Summary**: Averages, distributions, and breakdowns
- **Response Length Analysis**: Correlation between text length and sentiment

### 💾 Export Options

- **Enhanced Excel File** - Original data + sentiment columns
- **Printable Reports** - Professional formatting for presentations
- **High-Resolution Charts** - Perfect for reports and presentations

## 🛠️ Building Executables

The application can be packaged as standalone executables for easy distribution:

### Windows (.exe)

```bash
python build_executable.py
# Creates: dist/SentimentAnalyzer/SentimentAnalyzer.exe
```

### macOS (.app)

```bash
python build_executable.py
# Creates: dist/SentimentAnalyzer.app
```

### Build Features:

- ✅ **Self-contained** - No Python installation required
- ✅ **Auto-downloads AI model** on first run
- ✅ **Launcher scripts** for easy startup
- ✅ **Complete documentation** included

## 🔧 Technical Details

### AI Model

- **Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Type**: RoBERTa (Robustly Optimized BERT Pretraining Approach)
- **Training**: Optimized for social media and general text sentiment
- **Performance**: State-of-the-art accuracy for sentiment classification

### Technology Stack

- **Backend**: Flask (Python web framework)
- **AI/ML**: Transformers (Hugging Face), PyTorch
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn
- **File Handling**: OpenPyXL (Excel), Werkzeug (file uploads)
- **Frontend**: Bootstrap 5, HTML5, JavaScript

### Performance

- **Processing Speed**: ~1-5 responses per second (depending on hardware)
- **Memory Usage**: ~2-4GB RAM (includes model loading)
- **File Size Limits**: 16MB max upload, ~10,000 responses recommended
- **Supported Platforms**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

## 🚀 Usage Guide

### Step 1: Upload File

- Drag and drop Excel file or click to browse
- Supported formats: .xlsx, .xls
- Any Excel file with text data is supported

### Step 2: Preview & Column Selection

- View an interactive preview of your spreadsheet
- Select which column contains the text to analyze
- See sample values and column highlighting
- Confirm your selection before proceeding

### Step 3: Analysis

- Application automatically processes each response
- Progress shown in real-time
- AI model downloads on first use (may take a few minutes)

### Step 4: Results

- View comprehensive dashboard with insights
- Examine visualizations and statistics
- Download enhanced Excel file with results

### Step 5: Export

- Download Excel file with sentiment labels and confidence scores
- Print professional report directly from browser
- Save charts as high-resolution images

## 🔍 Troubleshooting

### Common Issues

**Port already in use**

```bash
# Solution: The app now uses port 5001 by default
# If port 5001 is also in use, modify port in app.py: app.run(port=5002)
# On macOS, port 5000 is used by AirPlay Receiver service
```

**Model download fails**

```bash
# Solution: Check internet connection
# Restart application - model will retry download
```

**Excel file not recognized**

```bash
# Solution: Upload any Excel file (.xlsx or .xls)
# Use the preview to select which column contains text
# Verify file isn't corrupted
```

**Memory errors with large files**

```bash
# Solution: Split large files into smaller chunks
# Recommend <10,000 responses per file
```

### Performance Tips

- 💡 **Smaller files process faster** - Consider splitting large datasets
- 💡 **First run slower** - AI model downloads on initial use
- 💡 **Close other applications** - Free up RAM for better performance
- 💡 **SSD storage recommended** - Faster file I/O operations

## 📝 Development

### Project Structure

```
sentiment-analysis/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Upload page
│   └── results.html      # Results dashboard
├── requirements.txt       # Python dependencies
├── build_executable.py   # Build script for executables
├── setup.py              # Package setup configuration
└── README.md             # This file
```

### Adding Features

1. **New Analysis Types**: Extend `analyze_sentiment()` function
2. **Additional Visualizations**: Add to `create_visualizations()`
3. **Custom Models**: Modify model loading in `load_sentiment_model()`
4. **UI Enhancements**: Update templates and CSS

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and included help files
- **Issues**: Report bugs and request features via GitHub issues
- **Community**: Join discussions in GitHub Discussions
- **Email**: Contact support@sentimentanalyzer.com

## 🙏 Acknowledgments

- **Hugging Face** - For the excellent Transformers library and model hosting
- **Cardiff NLP** - For the sentiment analysis model
- **Flask Team** - For the robust web framework
- **Bootstrap** - For the beautiful UI components

---

**Made with ❤️ for data analysts, researchers, and businesses who need powerful sentiment analysis tools.**
