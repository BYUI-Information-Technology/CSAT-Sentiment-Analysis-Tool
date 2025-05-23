# Sentiment Analysis Pipeline using RoBERTa
import pandas as pd
from transformers.pipelines import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_sentiment():
    """
    Analyze sentiment from responses.xlsx and save results back to the file.
    Reads from 'Response' column and saves sentiment results to 'Sentiment' column.
    """

    try:
        # Load the sentiment analysis pipeline using a proper sentiment model
        logger.info("Loading sentiment analysis model...")
        pipe = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        )
        logger.info("Model loaded successfully!")

        # Read the Excel file
        logger.info("Reading responses.xlsx...")
        df = pd.read_excel("responses.xlsx")

        # Check if required column exists
        if "Response" not in df.columns:
            raise ValueError("Column 'Response' not found in the Excel file")

        # Display basic info about the data
        logger.info(f"Found {len(df)} responses to analyze")
        logger.info(f"Columns in file: {list(df.columns)}")

        # Initialize sentiment column if it doesn't exist
        if "Sentiment" not in df.columns:
            df["Sentiment"] = None
            df["Confidence"] = None

        # Analyze sentiment for each response
        sentiments = []
        confidences = []

        for idx, response in enumerate(df["Response"]):
            if pd.isna(response) or response == "":
                sentiments.append("UNKNOWN")
                confidences.append(0.0)
                continue

            try:
                # Get sentiment prediction
                result = pipe(str(response))

                # Handle the pipeline result which is typically a list of dicts
                if isinstance(result, list) and len(result) > 0:
                    prediction = result[0]
                elif hasattr(result, "__iter__"):
                    # Convert iterator/generator to list
                    result_list = list(result)
                    prediction = result_list[0] if result_list else {}
                else:
                    prediction = result if isinstance(result, dict) else {}

                # Extract sentiment and confidence with fallbacks
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

                logger.info(f"Processed {idx + 1}/{len(df)} responses")

            except Exception as e:
                logger.warning(f"Error processing response {idx + 1}: {e}")
                sentiments.append("ERROR")
                confidences.append(0.0)

        # Update the dataframe
        df["Sentiment"] = sentiments
        df["Confidence"] = confidences

        # Save results back to Excel
        output_file = "responses_with_sentiment.xlsx"
        df.to_excel(output_file, index=False)
        logger.info(f"Results saved to {output_file}")

        # Display summary statistics
        sentiment_counts = df["Sentiment"].value_counts()
        logger.info("Sentiment Analysis Summary:")
        for sentiment, count in sentiment_counts.items():
            logger.info(f"  {sentiment}: {count} responses")

        return df

    except FileNotFoundError:
        logger.error(
            "File 'responses.xlsx' not found. Please ensure the file exists in the current directory."
        )
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    result = analyze_sentiment()
    if result is not None:
        print("\nSentiment analysis completed successfully!")
        print(f"Results saved to 'responses_with_sentiment.xlsx'")
    else:
        print("Sentiment analysis failed. Please check the logs above.")
