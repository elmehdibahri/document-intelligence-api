from fastapi import APIRouter, HTTPException
from app.utils.embedder import search_chunks
from pydantic import BaseModel

router = APIRouter()

# This defines the shape of the request body
class QuestionRequest(BaseModel):
    document_name: str
    question: str

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not request.document_name.strip():
        raise HTTPException(status_code=400, detail="Document name cannot be empty")
    
    # Search for relevant chunks
    relevant_chunks = search_chunks(
        query=request.question,
        document_name=request.document_name,
        top_k=3
    )
    
    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Please upload it first using /documents/upload"
        )
    
    # Build context from the top chunks
    context = "\n\n---\n\n".join([chunk["text"] for chunk in relevant_chunks])
    
    return {
        "question": request.question,
        "document": request.document_name,
        "relevant_chunks_found": len(relevant_chunks),
        "context_for_llm": context,  # This is what we'll send to the LLM in Layer 4
        "top_chunks": relevant_chunks,
        "note": "LLM answer coming in Layer 4 — for now you can see the relevant chunks retrieved"
    }