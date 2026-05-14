from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI(
    title="Document Intelligence API",
    description="Upload a PDF and ask questions about it",
    version="0.1.0"
)

app.include_router(upload_router, prefix="/documents", tags=["Documents"])

@app.get("/")
def health_check():
    return {"status": "running", "message": "Document Intelligence API is live"}