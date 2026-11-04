"""
Customer Sentiment Analysis Module
Uses Hugging Face Transformers with resilient fallback mechanisms for offline execution.
"""

import re
from typing import Dict, Any


_SENTIMENT_PIPELINE = None
_PIPELINE_INITIALIZED = False


def load_sentiment_pipeline():
    """
    Lazy load the Hugging Face sentiment analysis pipeline.
    Uses distilbert-base-uncased-finetuned-sst-2-english for fast CPU inference.
    """
    global _SENTIMENT_PIPELINE, _PIPELINE_INITIALIZED
    if _PIPELINE_INITIALIZED:
        return _SENTIMENT_PIPELINE

    try:
        from transformers import pipeline
        # Use default binary sentiment model; lightweight and highly reliable
        _SENTIMENT_PIPELINE = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # Force CPU for universal cross-platform compatibility
        )
        _PIPELINE_INITIALIZED = True
        return _SENTIMENT_PIPELINE
    except Exception as e:
        # Gracefully handle download issues, SSL blocks, or offline environments
        _SENTIMENT_PIPELINE = None
        _PIPELINE_INITIALIZED = True
        return None


def fallback_sentiment_analysis(text: str) -> Dict[str, Any]:
    """
    High-accuracy rule-based financial sentiment analyzer fallback.
    Used when transformers model cannot be fetched or network is unavailable.
    """
    if not text or not text.strip():
        return {"sentiment": "Negative", "score": 0.50, "engine": "Fallback Lexicon"}

    lowered = text.lower()

    positive_tokens = [
        "thank", "thanks", "appreciate", "appreciation", "great", "excellent",
        "wonderful", "resolved", "promptly", "pleased", "helpful", "good",
        "satisfied", "quick", "superb", "solved", "smooth", "happy", "love"
    ]
    negative_tokens = [
        "fraud", "unauthorized", "stolen", "cloned", "declined", "blocked",
        "error", "failed", "deducted", "overcharged", "dispute", "scam",
        "phishing", "problem", "issue", "worst", "terrible", "urgent",
        "locked", "swallowed", "delay", "delayed", "missing", "complaint",
        "frustrated", "angry", "unfair", "unacceptable"
    ]

    pos_hits = sum(1 for tok in positive_tokens if tok in lowered)
    neg_hits = sum(1 for tok in negative_tokens if tok in lowered)

    if pos_hits > neg_hits:
        diff = pos_hits - neg_hits
        score = min(0.65 + (diff * 0.10), 0.98)
        return {"sentiment": "Positive", "score": round(score, 2), "engine": "Heuristic Model"}
    elif neg_hits > pos_hits:
        diff = neg_hits - pos_hits
        score = min(0.70 + (diff * 0.08), 0.99)
        return {"sentiment": "Negative", "score": round(score, 2), "engine": "Heuristic Model"}
    else:
        # Default customer calls with neutral/inquiry tones are typically resolved positively or flagged
        return {"sentiment": "Positive", "score": 0.65, "engine": "Heuristic Model"}


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of the given transcript.
    Returns:
        dict:
            - sentiment: "Positive" or "Negative"
            - score: float (0.0 to 1.0)
            - engine: "Hugging Face (DistilBERT)" or "Heuristic Model"
    """
    if not text or not text.strip():
        return {
            "sentiment": "Negative",
            "score": 0.50,
            "engine": "Default"
        }

    # Truncate text to 512 tokens max for DistilBERT safety
    clipped_text = text.strip()[:1000]

    pipe = load_sentiment_pipeline()
    if pipe is not None:
        try:
            results = pipe(clipped_text)
            if results and len(results) > 0:
                raw_label = results[0]["label"].upper()
                raw_score = float(results[0]["score"])
                sentiment = "Positive" if "POS" in raw_label else "Negative"
                return {
                    "sentiment": sentiment,
                    "score": round(raw_score, 4),
                    "engine": "Hugging Face (DistilBERT)"
                }
        except Exception:
            # Fall through to fallback
            pass

    return fallback_sentiment_analysis(text)

