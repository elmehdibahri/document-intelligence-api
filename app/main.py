from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.query import router as query_router

app = FastAPI(
    title="Document Intelligence API",
    description="Upload a PDF and ask questions about it using AI",
    version="0.3.0"
)

app.include_router(upload_router, prefix="/documents", tags=["Documents"])
app.include_router(query_router, prefix="/documents", tags=["Questions"])

@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Document Intelligence API is live",
        "version": "0.3.0",
        "endpoints": {
            "upload": "POST /documents/upload",
            "ask": "POST /documents/ask",
            "docs": "GET /docs"
        }
    }