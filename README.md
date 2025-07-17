# MCP Server - Model Context Protocol API

The **MCP Server** is a FastAPI-based HTTP server that exposes three powerful NLP endpoints:

- 🔹 `/v1/summarize`: Generate a concise summary of input text.  
- 🔹 `/v1/keywords`: Extract key phrases from text.  
- 🔹 `/v1/sentiment`: Perform sentiment analysis on input text.

It includes request logging, API key authorization, OpenAPI schema, test coverage, and a minimal web frontend.

---

## 🚀 Features

- ✅ **3 NLP Tasks** via Hugging Face Transformers  
- ✅ **API Key Authentication** (middleware-based)  
- ✅ **Structured Error Handling** with unique `requestId`  
- ✅ **Request Logging** (path, status, duration)  
- ✅ **OpenAPI Docs** available at `/docs`  
- ✅ **Minimal Frontend UI** to test endpoints visually (`index.html`)  
- ✅ **Test Suite** using `pytest` + `httpx`

---

## 📦 Project Structure

MCP_Server/
├── app/
│ ├── main.py
│ ├── routes/
│ │ ├── summarize.py
│ │ ├── keywords.py
│ │ └── sentiment.py
│ └── utils/
│ └── logger.py
├── static/
│ └── index.html
├── tests/
│ ├── conftest.py
│ ├── test_keywords.py
│ ├── test_sentiment.py
│ └── test_summarize.py
├── openapi.json
├── requirements.txt
└── README.md


---

## 🔐 API Key Protection

All routes are protected with API key authentication, except:

- `/`
- `/docs`
- `/openapi.json`
- `/static/*`

Use this test key in your headers:

X-Api-Key: my-secret-api-key


---

## 📋 Example Usage

### ✅ 1. Health Check

```bash
curl http://localhost:8000/health
✅ 2. Sentiment Analysis
bash:
curl -X POST http://localhost:8000/v1/sentiment \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: my-secret-api-key" \
     -d '{ "text": "I love working on AI projects!" }'
✅ 3. Summarize
bash:

curl -X POST http://localhost:8000/v1/summarize \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: my-secret-api-key" \
     -d '{ "text": "Artificial Intelligence is transforming industries by enabling machines to learn from data..." }'
✅ 4. Keyword Extraction
bash:

curl -X POST http://localhost:8000/v1/keywords \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: my-secret-api-key" \
     -d '{ "text": "Transformers like BERT and GPT have revolutionized NLP." }'
🧪 Running Tests
To run all unit tests:

bash:

python -m pytest -v tests/
🖥️ Frontend UI
A minimal client interface is available at:

http://localhost:8000/
You can:

Paste input text

Choose task (Summarize, Keywords, Sentiment)

View output directly in the browser

API key is auto-attached via frontend JS

📄 OpenAPI Spec
To download the OpenAPI spec:

bash:
curl http://localhost:8000/openapi.json -H "X-Api-Key: my-secret-api-key" -o openapi.json
Swagger UI available at:

bash:

http://localhost:8000/docs
✅ Setup Instructions
bash
# Create virtual environment
python -m venv venv

# Activate
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
🧠 Models Used
Task	Model Name
Summarization	facebook/bart-large-cnn
Keywords	Custom logic via KeyBERT
Sentiment	distilbert-base-uncased-finetuned-sst-2-english

✨ Future Enhancements
🔐 Switch to token-based auth (OAuth2 / JWT)

💻 Frontend improvements using React/Vue

⚡ Add caching for repeated results

🙋 Author
Mayank Singh
AI/ML Engineer – Take-home assignment
Built  using FastAPI + HuggingFace + HTML