from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def get_sentiment_score(text: str) -> float:
    result = sentiment_pipeline(text[:512])[0]
    return 1.0 if result["label"] == "POSITIVE" else -1.0
