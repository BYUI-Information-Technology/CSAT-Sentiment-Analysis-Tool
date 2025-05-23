# Sentiment Data Analysis and Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

# Set style for better-looking plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class SentimentAnalyzer:
    def __init__(self, file_path="clean_sentiment.xlsx"):
        """Initialize the analyzer with the cleaned sentiment data."""
        self.file_path = file_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and prepare the sentiment data."""
        try:
            self.df = pd.read_excel(self.file_path)
            print(
                f"✅ Successfully loaded {len(self.df)} responses from {self.file_path}"
            )
            print(f"📊 Columns available: {list(self.df.columns)}")
        except FileNotFoundError:
            print(f"❌ Error: File '{self.file_path}' not found.")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None

    def basic_statistics(self):
        """Generate basic statistics about the sentiment data."""
        if self.df is None:
            return

        print("\n" + "=" * 50)
        print("📈 BASIC STATISTICS")
        print("=" * 50)

        # Data overview
        print(f"Total responses: {len(self.df)}")
        print(f"Columns: {list(self.df.columns)}")

        # Sentiment distribution
        if "Sentiment" in self.df.columns:
            sentiment_counts = self.df["Sentiment"].value_counts()
            print(f"\n📊 Sentiment Distribution:")
            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(self.df)) * 100
                print(f"  {sentiment}: {count} ({percentage:.1f}%)")

        # Confidence statistics
        if "Confidence" in self.df.columns:
            conf_stats = self.df["Confidence"].describe()
            print(f"\n🎯 Confidence Score Statistics:")
            print(f"  Mean: {conf_stats['mean']:.3f}")
            print(f"  Median: {conf_stats['50%']:.3f}")
            print(f"  Min: {conf_stats['min']:.3f}")
            print(f"  Max: {conf_stats['max']:.3f}")
            print(f"  Std Dev: {conf_stats['std']:.3f}")

    def create_sentiment_distribution_chart(self):
        """Create a bar chart showing sentiment distribution."""
        if self.df is None or "Sentiment" not in self.df.columns:
            return

        plt.figure(figsize=(10, 6))
        sentiment_counts = self.df["Sentiment"].value_counts()

        # Create bar chart
        bars = plt.bar(
            sentiment_counts.index,
            sentiment_counts.values,
            color=["#2E8B57", "#DC143C", "#4682B4", "#DAA520"],
        )

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 1,
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
        total = len(self.df)
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
        plt.savefig("sentiment_distribution.png", dpi=300, bbox_inches="tight")
        plt.show()
        print("📊 Chart saved as 'sentiment_distribution.png'")

    def create_sentiment_pie_chart(self):
        """Create a pie chart showing sentiment proportions."""
        if self.df is None or "Sentiment" not in self.df.columns:
            return

        plt.figure(figsize=(10, 8))
        sentiment_counts = self.df["Sentiment"].value_counts()

        # Define colors for different sentiments
        colors = ["#2E8B57", "#DC143C", "#4682B4", "#DAA520", "#8A2BE2"]

        # Create pie chart
        wedges, texts, autotexts = plt.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct="%1.1f%%",
            colors=colors[: len(sentiment_counts)],
            explode=[0.05] * len(sentiment_counts),
            shadow=True,
            startangle=90,
        )

        # Enhance text
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
        plt.savefig("sentiment_pie_chart.png", dpi=300, bbox_inches="tight")
        plt.show()
        print("🥧 Pie chart saved as 'sentiment_pie_chart.png'")

    def create_confidence_analysis(self):
        """Analyze and visualize confidence scores."""
        if self.df is None or "Confidence" not in self.df.columns:
            return

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # 1. Confidence distribution histogram
        ax1.hist(
            self.df["Confidence"],
            bins=20,
            color="skyblue",
            alpha=0.7,
            edgecolor="black",
        )
        ax1.set_title("Distribution of Confidence Scores", fontweight="bold")
        ax1.set_xlabel("Confidence Score")
        ax1.set_ylabel("Frequency")
        ax1.grid(alpha=0.3)

        # 2. Box plot of confidence by sentiment
        if "Sentiment" in self.df.columns:
            sns.boxplot(data=self.df, x="Sentiment", y="Confidence", ax=ax2)
            ax2.set_title("Confidence Scores by Sentiment", fontweight="bold")
            ax2.tick_params(axis="x", rotation=45)

        # 3. Confidence vs Response Length (if Response column exists)
        if "Response" in self.df.columns:
            self.df["Response_Length"] = self.df["Response"].astype(str).str.len()
            ax3.scatter(
                self.df["Response_Length"],
                self.df["Confidence"],
                alpha=0.6,
                color="coral",
            )
            ax3.set_title("Confidence vs Response Length", fontweight="bold")
            ax3.set_xlabel("Response Length (characters)")
            ax3.set_ylabel("Confidence Score")
            ax3.grid(alpha=0.3)

        # 4. High vs Low Confidence Distribution
        high_conf = self.df[self.df["Confidence"] >= 0.8]
        low_conf = self.df[self.df["Confidence"] < 0.5]

        categories = [
            "High Confidence\n(≥0.8)",
            "Medium Confidence\n(0.5-0.8)",
            "Low Confidence\n(<0.5)",
        ]
        counts = [
            len(high_conf),
            len(
                self.df[(self.df["Confidence"] >= 0.5) & (self.df["Confidence"] < 0.8)]
            ),
            len(low_conf),
        ]

        bars = ax4.bar(categories, counts, color=["green", "orange", "red"], alpha=0.7)
        ax4.set_title("Confidence Level Distribution", fontweight="bold")
        ax4.set_ylabel("Number of Responses")

        # Add value labels on bars
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
        plt.savefig("confidence_analysis.png", dpi=300, bbox_inches="tight")
        plt.show()
        print("🎯 Confidence analysis saved as 'confidence_analysis.png'")

    def create_combined_heatmap(self):
        """Create a heatmap showing sentiment vs confidence ranges."""
        if (
            self.df is None
            or "Sentiment" not in self.df.columns
            or "Confidence" not in self.df.columns
        ):
            return

        # Create confidence bins
        self.df["Confidence_Range"] = pd.cut(
            self.df["Confidence"],
            bins=[0, 0.5, 0.7, 0.9, 1.0],
            labels=[
                "Low (0-0.5)",
                "Medium (0.5-0.7)",
                "High (0.7-0.9)",
                "Very High (0.9-1.0)",
            ],
        )

        # Create crosstab
        heatmap_data = pd.crosstab(self.df["Sentiment"], self.df["Confidence_Range"])

        plt.figure(figsize=(10, 6))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt="d",
            cmap="YlOrRd",
            cbar_kws={"label": "Number of Responses"},
        )
        plt.title(
            "Sentiment vs Confidence Level Heatmap",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )
        plt.xlabel("Confidence Range", fontweight="bold")
        plt.ylabel("Sentiment", fontweight="bold")

        plt.tight_layout()
        plt.savefig("sentiment_confidence_heatmap.png", dpi=300, bbox_inches="tight")
        plt.show()
        print("🔥 Heatmap saved as 'sentiment_confidence_heatmap.png'")

    def generate_insights(self):
        """Generate key insights from the data."""
        if self.df is None:
            return

        print("\n" + "=" * 50)
        print("💡 KEY INSIGHTS")
        print("=" * 50)

        # Most common sentiment
        if "Sentiment" in self.df.columns:
            most_common = self.df["Sentiment"].mode()[0]
            most_common_pct = (
                self.df["Sentiment"].value_counts()[most_common] / len(self.df)
            ) * 100
            print(f"🏆 Most common sentiment: {most_common} ({most_common_pct:.1f}%)")

        # Confidence insights
        if "Confidence" in self.df.columns:
            avg_confidence = self.df["Confidence"].mean()
            high_conf_count = len(self.df[self.df["Confidence"] >= 0.8])
            high_conf_pct = (high_conf_count / len(self.df)) * 100

            print(f"📊 Average confidence score: {avg_confidence:.3f}")
            print(
                f"🎯 High confidence predictions (≥0.8): {high_conf_count} ({high_conf_pct:.1f}%)"
            )

            # Most confident sentiment
            conf_by_sentiment = (
                self.df.groupby("Sentiment")["Confidence"]
                .mean()
                .sort_values(ascending=False)
            )
            print(
                f"🔥 Most confident sentiment: {conf_by_sentiment.index[0]} (avg: {conf_by_sentiment.iloc[0]:.3f})"
            )

        # Response length insights (if available)
        if "Response" in self.df.columns:
            self.df["Response_Length"] = self.df["Response"].astype(str).str.len()
            avg_length = self.df["Response_Length"].mean()
            print(f"📝 Average response length: {avg_length:.0f} characters")

            # Length by sentiment
            length_by_sentiment = (
                self.df.groupby("Sentiment")["Response_Length"]
                .mean()
                .sort_values(ascending=False)
            )
            print(
                f"📏 Longest responses on average: {length_by_sentiment.index[0]} ({length_by_sentiment.iloc[0]:.0f} chars)"
            )

    def export_summary_report(self):
        """Export a summary report to Excel."""
        if self.df is None:
            return

        # Create summary statistics
        summary_data = {}

        if "Sentiment" in self.df.columns:
            sentiment_summary = self.df["Sentiment"].value_counts().reset_index()
            sentiment_summary.columns = ["Sentiment", "Count"]
            sentiment_summary["Percentage"] = (
                sentiment_summary["Count"] / len(self.df)
            ) * 100

        if "Confidence" in self.df.columns:
            confidence_summary = self.df["Confidence"].describe().reset_index()
            confidence_summary.columns = ["Statistic", "Value"]

        # Write to Excel with multiple sheets
        with pd.ExcelWriter(
            "sentiment_analysis_report.xlsx", engine="openpyxl"
        ) as writer:
            # Original data
            self.df.to_excel(writer, sheet_name="Data", index=False)

            # Sentiment summary
            if "Sentiment" in self.df.columns:
                sentiment_summary.to_excel(
                    writer, sheet_name="Sentiment_Summary", index=False
                )

            # Confidence summary
            if "Confidence" in self.df.columns:
                confidence_summary.to_excel(
                    writer, sheet_name="Confidence_Summary", index=False
                )

        print("📊 Summary report exported to 'sentiment_analysis_report.xlsx'")

    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        if self.df is None:
            print("❌ No data available for analysis.")
            return

        print("🚀 Starting Complete Sentiment Analysis...")

        # Basic statistics
        self.basic_statistics()

        # Generate insights
        self.generate_insights()

        # Create visualizations
        print("\n📊 Creating visualizations...")
        self.create_sentiment_distribution_chart()
        self.create_sentiment_pie_chart()
        self.create_confidence_analysis()
        self.create_combined_heatmap()

        # Export report
        self.export_summary_report()

        print("\n✅ Analysis complete! Check the generated files:")
        print("  📊 sentiment_distribution.png")
        print("  🥧 sentiment_pie_chart.png")
        print("  🎯 confidence_analysis.png")
        print("  🔥 sentiment_confidence_heatmap.png")
        print("  📋 sentiment_analysis_report.xlsx")


if __name__ == "__main__":
    # Run the analysis
    analyzer = SentimentAnalyzer("clean_sentiment.xlsx")
    analyzer.run_complete_analysis()
