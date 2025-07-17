from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# Load only once (GPU-compatible if available)
model = SentenceTransformer('all-MiniLM-L6-v2')
kw_model = KeyBERT(model)

def extract_keywords(text: str, top_n: int = 10):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=top_n,
        use_maxsum=True,
        nr_candidates=20
    )
    return keywords
