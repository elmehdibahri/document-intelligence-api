# Document Intelligence API

A backend API that accepts PDF uploads and answers questions about their content using AI.

## Tech Stack
- Python 3.11
- FastAPI
- pdfplumber
- Docker
- Azure (deployment — coming soon)

## What it does
- Accepts PDF file uploads via REST API
- Extracts and processes text from documents
- (Coming soon) Answers natural language questions about uploaded documents

## How to run locally

git clone https://github.com/yourusername/document-intelligence-api
cd document-intelligence-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Then open http://localhost:8000/docs to test the API.

## Project Status
🔧 In active development — Layer 2 (chunking) in progress