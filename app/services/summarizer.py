from transformers import pipeline

# Load once on module load
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_sentences: int = 3) -> str:
    max_length = max(60, max_sentences * 20)
    summary = summarizer_pipeline(text, max_length=max_length, min_length=20, do_sample=False)
    return summary[0]['summary_text']
