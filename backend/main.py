"""
FastAPI Backend for Multi-Agent AI System
Provides REST API endpoints for the Data Intelligence and Research Assistant agents
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import tempfile
import os
import shutil
from pathlib import Path
import uvicorn

from agents.orchestrator_agent import OrchestratorAgent

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent AI System API",
    description="API for Data Intelligence and Research Assistant agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = OrchestratorAgent()

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    orchestrator_info: Optional[Dict[str, Any]] = None

class FileUploadResponse(BaseModel):
    success: bool
    message: str
    file_info: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Helper functions
def save_uploaded_file(upload_file: UploadFile) -> str:
    """Save uploaded file to temporary location"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, upload_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

def is_data_file(filename: str) -> bool:
    """Check if file is a data file (CSV/Excel)"""
    return filename.lower().endswith(('.csv', '.xlsx', '.xls'))

def is_pdf_file(filename: str) -> bool:
    """Check if file is a PDF"""
    return filename.lower().endswith('.pdf')

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multi-Agent AI System API",
        "version": "1.0.0",
        "endpoints": {
            "upload_data": "/upload/data",
            "upload_pdf": "/upload/pdf",
            "query": "/query",
            "status": "/status",
            "files": "/files"
        }
    }

@app.post("/upload/data", response_model=FileUploadResponse)
async def upload_data_file(file: UploadFile = File(...)):
    """Upload CSV or Excel file for data analysis"""
    try:
        # Validate file type
        if not is_data_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload CSV or Excel files."
            )
        
        # Save file temporarily
        file_path = save_uploaded_file(file)
        
        # Load through orchestrator
        result = orchestrator.load_data_file(file_path, file.filename)
        
        # Clean up temporary file
        os.unlink(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        if "error" in result:
            return FileUploadResponse(
                success=False,
                message="Failed to load data file",
                error=result["error"]
            )
        
        return FileUploadResponse(
            success=True,
            message=result["message"],
            file_info=result["info"]
        )
        
    except Exception as e:
        return FileUploadResponse(
            success=False,
            message="Upload failed",
            error=str(e)
        )

@app.post("/upload/pdf", response_model=FileUploadResponse)
async def upload_pdf_file(file: UploadFile = File(...)):
    """Upload PDF file for research analysis"""
    try:
        # Validate file type
        if not is_pdf_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload PDF files."
            )
        
        # Save file temporarily
        file_path = save_uploaded_file(file)
        
        # Load through orchestrator
        result = orchestrator.load_pdf_file(file_path, file.filename)
        
        # Clean up temporary file
        os.unlink(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        if "error" in result:
            return FileUploadResponse(
                success=False,
                message="Failed to load PDF file",
                error=result["error"]
            )
        
        return FileUploadResponse(
            success=True,
            message=result["message"],
            file_info=result["info"]
        )
        
    except Exception as e:
        return FileUploadResponse(
            success=False,
            message="Upload failed",
            error=str(e)
        )

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query through the orchestrator"""
    try:
        result = orchestrator.process_query(request.query, request.context)
        
        if "error" in result:
            return QueryResponse(
                success=False,
                error=result["error"],
                orchestrator_info=result.get("orchestrator_info")
            )
        
        return QueryResponse(
            success=True,
            result=result,
            orchestrator_info=result.get("orchestrator_info")
        )
        
    except Exception as e:
        return QueryResponse(
            success=False,
            error=f"Query processing failed: {str(e)}"
        )

@app.get("/status")
async def get_system_status():
    """Get current system status"""
    try:
        status = orchestrator._get_system_status()
        return status
    except Exception as e:
        return {"error": f"Failed to get status: {str(e)}"}

@app.get("/files")
async def get_loaded_files():
    """Get information about loaded files"""
    try:
        files_info = orchestrator.get_loaded_files()
        return {
            "success": True,
            "files": files_info
        }
    except Exception as e:
        return {"error": f"Failed to get files info: {str(e)}"}

@app.delete("/files/clear")
async def clear_all_files():
    """Clear all loaded files and data"""
    try:
        result = orchestrator.clear_all_data()
        return result
    except Exception as e:
        return {"error": f"Failed to clear files: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": {
            "orchestrator": "active",
            "data_intelligence": "active",
            "research_assistant": "active"
        }
    }

# Data-specific endpoints
@app.get("/data/datasets")
async def get_datasets():
    """Get list of loaded datasets"""
    try:
        datasets = orchestrator.data_agent.list_datasets()
        return {
            "success": True,
            "datasets": datasets
        }
    except Exception as e:
        return {"error": f"Failed to get datasets: {str(e)}"}

@app.get("/data/summary/{dataset_name}")
async def get_dataset_summary(dataset_name: str):
    """Get summary of a specific dataset"""
    try:
        summary = orchestrator.data_agent.get_dataset_summary(dataset_name)
        return summary
    except Exception as e:
        return {"error": f"Failed to get dataset summary: {str(e)}"}

# Research-specific endpoints
@app.get("/research/documents")
async def get_documents():
    """Get list of loaded research documents"""
    try:
        documents = orchestrator.research_agent.list_documents()
        return {
            "success": True,
            "documents": documents
        }
    except Exception as e:
        return {"error": f"Failed to get documents: {str(e)}"}

@app.get("/research/document/{document_name}")
async def get_document_info(document_name: str):
    """Get information about a specific document"""
    try:
        info = orchestrator.research_agent.get_document_info(document_name)
        return info
    except Exception as e:
        return {"error": f"Failed to get document info: {str(e)}"}

@app.post("/research/search")
async def search_documents(request: QueryRequest):
    """Search across research documents"""
    try:
        result = orchestrator.research_agent.search_documents(request.query)
        return result
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
