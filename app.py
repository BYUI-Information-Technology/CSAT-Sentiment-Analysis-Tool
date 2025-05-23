import os
import pandas as pd
import matplotlib
import sqlite3
import json

matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    jsonify,
)
from werkzeug.utils import secure_filename
from transformers.pipelines import pipeline
import logging
import io
import base64
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Configure matplotlib and seaborn
plt.style.use("default")
sns.set_palette("husl")

app = Flask(__name__)
app.secret_key = "sentiment_analysis_app_2024"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Configure upload folder
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"
DATABASE_FILE = "sentiment_analysis.db"

for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULTS_FOLDER"] = RESULTS_FOLDER

# Global variables
sentiment_pipeline = None
analysis_results = {}


def init_database():
    """Initialize the SQLite database for storing analysis history"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_filename TEXT NOT NULL,
            result_filename TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_responses INTEGER,
            sentiment_distribution TEXT,  -- JSON string
            confidence_stats TEXT,       -- JSON string
            avg_confidence REAL,
            most_common_sentiment TEXT,
            most_common_percentage REAL,
            high_confidence_count INTEGER,
            high_confidence_percentage REAL,
            processing_time REAL
        )
    """
    )

    conn.commit()
    conn.close()


def save_analysis_to_db(original_filename, result_filename, insights, processing_time):
    """Save analysis results to the database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Prepare data for insertion
        sentiment_dist = json.dumps(insights.get("sentiment_distribution", {}))
        confidence_stats = json.dumps(insights.get("confidence_stats", {}))

        cursor.execute(
            """
            INSERT INTO analysis_runs (
                original_filename, result_filename, total_responses,
                sentiment_distribution, confidence_stats, avg_confidence,
                most_common_sentiment, most_common_percentage,
                high_confidence_count, high_confidence_percentage,
                processing_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                original_filename,
                result_filename,
                insights.get("total_responses", 0),
                sentiment_dist,
                confidence_stats,
                insights.get("confidence_stats", {}).get("mean", 0.0),
                insights.get("most_common_sentiment", {}).get("sentiment", "Unknown"),
                insights.get("most_common_sentiment", {}).get("percentage", 0.0),
                insights.get("high_confidence", {}).get("count", 0),
                insights.get("high_confidence", {}).get("percentage", 0.0),
                processing_time,
            ),
        )

        conn.commit()
        run_id = cursor.lastrowid
        conn.close()
        return run_id

    except Exception as e:
        logging.error(f"Error saving to database: {e}")
        return None


def get_analysis_history():
    """Retrieve all analysis runs from the database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, original_filename, upload_date, total_responses,
                   sentiment_distribution, most_common_sentiment, 
                   most_common_percentage, avg_confidence,
                   high_confidence_percentage, processing_time
            FROM analysis_runs 
            ORDER BY upload_date DESC
        """
        )

        runs = []
        for row in cursor.fetchall():
            run_data = {
                "id": row[0],
                "original_filename": row[1],
                "upload_date": row[2],
                "total_responses": row[3],
                "sentiment_distribution": json.loads(row[4]) if row[4] else {},
                "most_common_sentiment": row[5],
                "most_common_percentage": row[6],
                "avg_confidence": row[7],
                "high_confidence_percentage": row[8],
                "processing_time": row[9],
            }
            runs.append(run_data)

        conn.close()
        return runs

    except Exception as e:
        logging.error(f"Error retrieving analysis history: {e}")
        return []


def get_analysis_by_id(run_id):
    """Retrieve a specific analysis run by ID"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM analysis_runs WHERE id = ?
        """,
            (run_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "original_filename": row[1],
                "result_filename": row[2],
                "upload_date": row[3],
                "total_responses": row[4],
                "sentiment_distribution": json.loads(row[5]) if row[5] else {},
                "confidence_stats": json.loads(row[6]) if row[6] else {},
                "avg_confidence": row[7],
                "most_common_sentiment": row[8],
                "most_common_percentage": row[9],
                "high_confidence_count": row[10],
                "high_confidence_percentage": row[11],
                "processing_time": row[12],
            }
        return None

    except Exception as e:
        logging.error(f"Error retrieving analysis by ID: {e}")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"xlsx", "xls"}


def load_sentiment_model():
    """Load the sentiment analysis model"""
    global sentiment_pipeline
    try:
        if sentiment_pipeline is None:
            logging.info("Loading sentiment analysis model...")
            sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            )
            logging.info("Model loaded successfully!")
        return True
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return False


def analyze_sentiment(df, column_name="Why satisfied text area"):
    """Perform sentiment analysis on the specified column of the dataframe"""
    global sentiment_pipeline

    if sentiment_pipeline is None:
        if not load_sentiment_model():
            return None, "Failed to load sentiment model"

    try:
        # Check if required column exists
        if column_name not in df.columns:
            return None, f"Column '{column_name}' not found in the Excel file"

        # Initialize sentiment columns
        df["Sentiment"] = None
        df["Confidence"] = None

        sentiments = []
        confidences = []

        for idx, response in enumerate(df[column_name]):
            if pd.isna(response) or response == "":
                sentiments.append("UNKNOWN")
                confidences.append(0.0)
                continue

            try:
                # Get sentiment prediction
                if sentiment_pipeline is not None:
                    result = sentiment_pipeline(str(response))
                else:
                    sentiments.append("ERROR")
                    confidences.append(0.0)
                    continue

                # Handle the pipeline result
                if isinstance(result, list) and len(result) > 0:
                    prediction = result[0]
                elif hasattr(result, "__iter__") and not isinstance(result, str):
                    try:
                        result_list = list(result) if result is not None else []
                        prediction = result_list[0] if result_list else {}
                    except:
                        prediction = {}
                else:
                    prediction = result if isinstance(result, dict) else {}

                # Extract sentiment and confidence
                sentiment = (
                    prediction.get("label", "UNKNOWN")
                    if isinstance(prediction, dict)
                    else "UNKNOWN"
                )
                confidence = (
                    prediction.get("score", 0.0)
                    if isinstance(prediction, dict)
                    else 0.0
                )

                sentiments.append(sentiment)
                confidences.append(confidence)

            except Exception as e:
                logging.warning(f"Error processing response {idx + 1}: {e}")
                sentiments.append("ERROR")
                confidences.append(0.0)

        # Update the dataframe
        df["Sentiment"] = sentiments
        df["Confidence"] = confidences

        return df, None

    except Exception as e:
        return None, f"Error during sentiment analysis: {e}"


def create_visualizations(df):
    """Create all visualizations and return as base64 encoded images"""
    plots = {}

    # BYUI Brand Colors
    byui_colors = {
        "primary": "#006EB6",  # BYUI Brand Blue
        "secondary": "#214491",  # BYUI Accent Blue Dark
        "accent": "#4F9ACF",  # BYUI Accent Blue Medium
        "light": "#A0D4ED",  # BYUI Accent Blue Light
        "gray": "#949598",  # BYUI Gray
        "black": "#000000",  # BYUI Black
        "positive": "#006EB6",  # Use brand blue for positive
        "negative": "#214491",  # Use dark blue for negative
        "neutral": "#4F9ACF",  # Use medium blue for neutral
        "unknown": "#949598",  # Use gray for unknown
    }

    try:
        # 1. Sentiment Distribution Bar Chart
        plt.figure(figsize=(10, 6))
        sentiment_counts = df["Sentiment"].value_counts()

        # Map sentiments to BYUI colors
        color_map = {
            "POSITIVE": byui_colors["positive"],
            "NEGATIVE": byui_colors["negative"],
            "NEUTRAL": byui_colors["neutral"],
            "UNKNOWN": byui_colors["unknown"],
            "ERROR": byui_colors["gray"],
        }

        bar_colors = [
            color_map.get(sentiment, byui_colors["primary"])
            for sentiment in sentiment_counts.index
        ]

        bars = plt.bar(
            sentiment_counts.index,
            sentiment_counts.values,
            color=bar_colors,
        )

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.5,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        plt.title("Sentiment Distribution", fontsize=16, fontweight="bold", pad=20)
        plt.xlabel("Sentiment", fontsize=12, fontweight="bold")
        plt.ylabel("Number of Responses", fontsize=12, fontweight="bold")
        plt.grid(axis="y", alpha=0.3)

        # Add percentage labels
        total = len(df)
        for i, (sentiment, count) in enumerate(sentiment_counts.items()):
            percentage = (count / total) * 100
            plt.text(
                i,
                count / 2,
                f"{percentage:.1f}%",
                ha="center",
                va="center",
                fontweight="bold",
                color="white",
                fontsize=10,
            )

        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format="png", dpi=300, bbox_inches="tight")
        img.seek(0)
        plots["sentiment_distribution"] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # 2. Sentiment Pie Chart
        plt.figure(figsize=(10, 8))
        pie_colors = [
            color_map.get(sentiment, byui_colors["primary"])
            for sentiment in sentiment_counts.index
        ]

        pie_result = plt.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct="%1.1f%%",
            colors=pie_colors,
            explode=[0.05] * len(sentiment_counts),
            shadow=True,
            startangle=90,
        )

        # Handle different return types from pie chart
        if len(pie_result) >= 3:
            wedges, texts, autotexts = pie_result
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(10)

        plt.title(
            "Sentiment Distribution (Proportions)",
            fontsize=16,
            fontweight="bold",
            pad=20,
        )
        plt.axis("equal")

        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format="png", dpi=300, bbox_inches="tight")
        img.seek(0)
        plots["sentiment_pie"] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # 3. Confidence Analysis
        if "Confidence" in df.columns:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

            # Confidence distribution
            ax1.hist(
                df["Confidence"],
                bins=20,
                color=byui_colors["primary"],
                alpha=0.7,
                edgecolor=byui_colors["black"],
            )
            ax1.set_title("Distribution of Confidence Scores", fontweight="bold")
            ax1.set_xlabel("Confidence Score")
            ax1.set_ylabel("Frequency")
            ax1.grid(alpha=0.3)

            # Box plot by sentiment
            sns.boxplot(
                data=df,
                x="Sentiment",
                y="Confidence",
                ax=ax2,
                palette=[
                    color_map.get(sentiment, byui_colors["primary"])
                    for sentiment in df["Sentiment"].unique()
                ],
            )
            ax2.set_title("Confidence Scores by Sentiment", fontweight="bold")
            ax2.tick_params(axis="x", rotation=45)

            # Confidence vs response length
            if "Why satisfied text area" in df.columns:
                df["Response_Length"] = (
                    df["Why satisfied text area"].astype(str).str.len()
                )
                ax3.scatter(
                    df["Response_Length"],
                    df["Confidence"],
                    alpha=0.6,
                    color=byui_colors["accent"],
                )
                ax3.set_title("Confidence vs Response Length", fontweight="bold")
                ax3.set_xlabel("Response Length (characters)")
                ax3.set_ylabel("Confidence Score")
                ax3.grid(alpha=0.3)

            # Confidence level distribution
            high_conf = len(df[df["Confidence"] >= 0.8])
            med_conf = len(df[(df["Confidence"] >= 0.5) & (df["Confidence"] < 0.8)])
            low_conf = len(df[df["Confidence"] < 0.5])

            categories = ["High\n(≥0.8)", "Medium\n(0.5-0.8)", "Low\n(<0.5)"]
            counts = [high_conf, med_conf, low_conf]

            bars = ax4.bar(
                categories,
                counts,
                color=[
                    byui_colors["primary"],
                    byui_colors["accent"],
                    byui_colors["gray"],
                ],
                alpha=0.7,
            )
            ax4.set_title("Confidence Level Distribution", fontweight="bold")
            ax4.set_ylabel("Number of Responses")

            for bar in bars:
                height = bar.get_height()
                ax4.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 0.5,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

            plt.tight_layout()
            img = io.BytesIO()
            plt.savefig(img, format="png", dpi=300, bbox_inches="tight")
            img.seek(0)
            plots["confidence_analysis"] = base64.b64encode(img.getvalue()).decode()
            plt.close()

        return plots

    except Exception as e:
        logging.error(f"Error creating visualizations: {e}")
        return {}


def generate_insights(df, column_name="Why satisfied text area"):
    """Generate key insights from the data"""
    insights = {}

    try:
        # Basic statistics
        insights["total_responses"] = len(df)
        insights["columns"] = list(df.columns)
        insights["column_analyzed"] = column_name

        # Sentiment distribution
        if "Sentiment" in df.columns:
            sentiment_counts = df["Sentiment"].value_counts()
            insights["sentiment_distribution"] = sentiment_counts.to_dict()

            most_common = sentiment_counts.index[0]
            most_common_pct = (sentiment_counts.iloc[0] / len(df)) * 100
            insights["most_common_sentiment"] = {
                "sentiment": most_common,
                "count": sentiment_counts.iloc[0],
                "percentage": round(most_common_pct, 1),
            }

        # Confidence statistics
        if "Confidence" in df.columns:
            conf_stats = df["Confidence"].describe()
            insights["confidence_stats"] = {
                "mean": round(conf_stats["mean"], 3),
                "median": round(conf_stats["50%"], 3),
                "min": round(conf_stats["min"], 3),
                "max": round(conf_stats["max"], 3),
                "std": round(conf_stats["std"], 3),
            }

            high_conf_count = len(df[df["Confidence"] >= 0.8])
            high_conf_pct = (high_conf_count / len(df)) * 100
            insights["high_confidence"] = {
                "count": high_conf_count,
                "percentage": round(high_conf_pct, 1),
            }

            # Most confident sentiment
            conf_by_sentiment = (
                df.groupby("Sentiment")["Confidence"]
                .mean()
                .sort_values(ascending=False)
            )
            if len(conf_by_sentiment) > 0:
                insights["most_confident_sentiment"] = {
                    "sentiment": conf_by_sentiment.index[0],
                    "avg_confidence": round(conf_by_sentiment.iloc[0], 3),
                }

        # Response length analysis
        if column_name in df.columns:
            df["Response_Length"] = df[column_name].astype(str).str.len()
            avg_length = df["Response_Length"].mean()
            insights["avg_response_length"] = round(avg_length, 0)

            length_by_sentiment = (
                df.groupby("Sentiment")["Response_Length"]
                .mean()
                .sort_values(ascending=False)
            )
            if len(length_by_sentiment) > 0:
                insights["longest_responses_sentiment"] = {
                    "sentiment": length_by_sentiment.index[0],
                    "avg_length": round(length_by_sentiment.iloc[0], 0),
                }

        return insights

    except Exception as e:
        logging.error(f"Error generating insights: {e}")
        return {}


@app.route("/")
def index():
    """Main page with file upload"""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and show preview"""
    if "file" not in request.files:
        flash("No file selected")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename or "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        return redirect(url_for("preview", filename=filename))
    else:
        flash("Please upload an Excel file (.xlsx or .xls)")
        return redirect(request.url)


@app.route("/preview/<filename>")
def preview(filename):
    """Preview the uploaded Excel file and allow column selection"""
    try:
        # Load the Excel file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        if not os.path.exists(filepath):
            flash(f"File not found: {filename}")
            return redirect(url_for("index"))

        df = pd.read_excel(filepath)

        # Get first 10 rows for preview
        preview_df = df.head(10)

        # Convert to HTML table
        preview_table = preview_df.to_html(
            classes="table table-striped table-hover",
            table_id="previewTable",
            escape=False,
        )

        # Get column names for selection
        columns = list(df.columns)

        # Get basic info
        total_rows = len(df)

        return render_template(
            "preview.html",
            filename=filename,
            preview_table=preview_table,
            columns=columns,
            total_rows=total_rows,
            preview_rows=len(preview_df),
        )

    except Exception as e:
        logging.error(f"Error in preview route: {e}")
        flash(f"Error reading Excel file: {e}")
        return redirect(url_for("index"))


@app.route("/analyze/<filename>")
def analyze(filename):
    """Perform sentiment analysis on uploaded file"""
    # Get selected column from query parameter
    column_name = request.args.get("column", "Why satisfied text area")
    return analyze_with_column(filename, column_name)


@app.route("/analyze/<filename>/<column_name>")
def analyze_with_column(filename, column_name):
    """Perform sentiment analysis on uploaded file with specified column"""
    global analysis_results

    start_time = datetime.now()

    try:
        # Load the Excel file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        df = pd.read_excel(filepath)

        # Check if model is loaded
        if not load_sentiment_model():
            flash("Error loading sentiment analysis model")
            return redirect(url_for("index"))

        # Perform sentiment analysis
        analyzed_df, error = analyze_sentiment(df, column_name)
        if error or analyzed_df is None:
            flash(f"Error during analysis: {error}")
            return redirect(url_for("index"))

        # Save analyzed results
        result_filename = f"analyzed_{filename}"
        result_filepath = os.path.join(app.config["RESULTS_FOLDER"], result_filename)
        analyzed_df.to_excel(result_filepath, index=False)

        # Generate visualizations
        plots = create_visualizations(analyzed_df)

        # Generate insights
        insights = generate_insights(analyzed_df, column_name)

        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Save to database
        run_id = save_analysis_to_db(
            filename, result_filename, insights, processing_time
        )

        # Store results globally
        analysis_results = {
            "df": analyzed_df,
            "plots": plots,
            "insights": insights,
            "filename": result_filename,
            "original_filename": filename,
            "run_id": run_id,
            "processing_time": processing_time,
            "column_analyzed": column_name,
        }

        return redirect(url_for("results"))

    except Exception as e:
        flash(f"Error processing file: {e}")
        return redirect(url_for("index"))


@app.route("/results")
def results():
    """Display analysis results"""
    global analysis_results

    if not analysis_results:
        flash("No analysis results available")
        return redirect(url_for("index"))

    return render_template(
        "results.html",
        insights=analysis_results["insights"],
        plots=analysis_results["plots"],
        filename=analysis_results["filename"],
    )


@app.route("/download")
def download():
    """Download analyzed Excel file"""
    global analysis_results

    if not analysis_results:
        flash("No analysis results available")
        return redirect(url_for("index"))

    filepath = os.path.join(app.config["RESULTS_FOLDER"], analysis_results["filename"])
    return send_file(filepath, as_attachment=True)


@app.route("/history")
def history():
    """Display analysis history"""
    runs = get_analysis_history()
    return render_template("history.html", runs=runs)


@app.route("/view/<int:run_id>")
def view_analysis(run_id):
    """View a specific analysis run"""
    run_data = get_analysis_by_id(run_id)
    if not run_data:
        flash("Analysis run not found")
        return redirect(url_for("history"))

    # Check if result file still exists
    result_filepath = os.path.join(
        app.config["RESULTS_FOLDER"], run_data["result_filename"]
    )
    if not os.path.exists(result_filepath):
        flash("Result file no longer exists")
        return redirect(url_for("history"))

    # Load the Excel file and regenerate visualizations
    try:
        df = pd.read_excel(result_filepath)
        plots = create_visualizations(df)

        # Prepare insights from database data
        insights = {
            "total_responses": run_data["total_responses"],
            "sentiment_distribution": run_data["sentiment_distribution"],
            "confidence_stats": run_data["confidence_stats"],
            "most_common_sentiment": {
                "sentiment": run_data["most_common_sentiment"],
                "percentage": run_data["most_common_percentage"],
            },
            "high_confidence": {
                "count": run_data["high_confidence_count"],
                "percentage": run_data["high_confidence_percentage"],
            },
        }

        return render_template(
            "view_analysis.html", run_data=run_data, insights=insights, plots=plots
        )

    except Exception as e:
        flash(f"Error loading analysis: {e}")
        return redirect(url_for("history"))


@app.route("/download/<int:run_id>")
def download_analysis(run_id):
    """Download a specific analysis result file"""
    run_data = get_analysis_by_id(run_id)
    if not run_data:
        flash("Analysis run not found")
        return redirect(url_for("history"))

    filepath = os.path.join(app.config["RESULTS_FOLDER"], run_data["result_filename"])
    if not os.path.exists(filepath):
        flash("Result file no longer exists")
        return redirect(url_for("history"))

    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"analysis_{run_data['original_filename']}",
    )


@app.route("/delete_analysis/<int:run_id>", methods=["POST"])
def delete_analysis(run_id):
    """Delete an analysis run and its associated files"""
    try:
        run_data = get_analysis_by_id(run_id)
        if run_data:
            # Delete from database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analysis_runs WHERE id = ?", (run_id,))
            conn.commit()
            conn.close()

            # Delete result file if it exists
            result_filepath = os.path.join(
                app.config["RESULTS_FOLDER"], run_data["result_filename"]
            )
            if os.path.exists(result_filepath):
                os.remove(result_filepath)

            flash("Analysis deleted successfully")
        else:
            flash("Analysis not found")

    except Exception as e:
        flash(f"Error deleting analysis: {e}")

    return redirect(url_for("history"))


@app.route("/api/status")
def status():
    """API endpoint to check model status"""
    model_loaded = sentiment_pipeline is not None
    return jsonify({"model_loaded": model_loaded})


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Initialize database
    print("📊 Initializing database...")
    init_database()
    print("✅ Database initialized!")

    # Load model on startup
    print("🚀 Starting Sentiment Analysis Application...")
    print("📥 Loading sentiment analysis model...")
    if load_sentiment_model():
        print("✅ Model loaded successfully!")
    else:
        print("❌ Failed to load model")

    print("🌐 Starting Flask server...")
    print("🔗 Application will be available at: http://localhost:5001")
    app.run(debug=False, host="0.0.0.0", port=5001)
