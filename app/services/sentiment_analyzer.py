from transformers import pipeline

# Load the model once
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text: str):
    result = sentiment_pipeline(text)[0]
    return result['label'].lower(), result['score']
