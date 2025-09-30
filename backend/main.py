"""
FastAPI application for job-CV matching service
"""
import time
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from inference import predict, batch_predict
from preprocess import preprocess_text_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Job-CV Matching API",
    description="API for matching job descriptions with CVs using TF-IDF and cosine similarity",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    jd_text: str = Field(..., description="Job description text", min_length=1)
    cv_text: str = Field(..., description="CV text", min_length=1)
    topk: int = Field(default=6, description="Number of top features to return", ge=1, le=20)

class PredictionResponse(BaseModel):
    score: float = Field(..., description="Matching score between 0 and 1")
    percent: str = Field(..., description="Matching percentage as string")
    features: List[str] = Field(..., description="Top matching features/keywords")
    latency_ms: int = Field(..., description="Processing latency in milliseconds")

class BatchPredictionRequest(BaseModel):
    pairs: List[Dict[str, str]] = Field(..., description="List of JD-CV text pairs")
    topk: int = Field(default=6, description="Number of top features to return", ge=1, le=20)

class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse] = Field(..., description="List of prediction results")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: float = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_matching(request: PredictionRequest):
    """
    Predict matching score between job description and CV
    
    Args:
        request: PredictionRequest containing JD text, CV text, and topk
        
    Returns:
        PredictionResponse with score, percent, features, and latency
    """
    try:
        logger.info(f"Received prediction request - JD length: {len(request.jd_text)}, CV length: {len(request.cv_text)}")
        
        # Make prediction
        result = predict(request.jd_text, request.cv_text, request.topk)
        
        # Validate result
        if not isinstance(result, dict) or 'score' not in result:
            raise HTTPException(status_code=500, detail="Invalid prediction result")
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch_json", response_model=BatchPredictionResponse)
async def predict_batch_matching(request: BatchPredictionRequest):
    """
    Predict matching scores for multiple JD-CV pairs
    
    Args:
        request: BatchPredictionRequest containing list of JD-CV pairs
        
    Returns:
        BatchPredictionResponse with list of prediction results
    """
    try:
        logger.info(f"Received batch prediction request - {len(request.pairs)} pairs")
        
        # Validate input
        if not request.pairs or len(request.pairs) == 0:
            raise HTTPException(status_code=400, detail="No pairs provided")
        
        if len(request.pairs) > 100:  # Limit batch size
            raise HTTPException(status_code=400, detail="Too many pairs (max 100)")
        
        # Prepare pairs
        jd_cv_pairs = []
        for pair in request.pairs:
            if 'jd_text' not in pair or 'cv_text' not in pair:
                raise HTTPException(status_code=400, detail="Invalid pair format")
            jd_cv_pairs.append((pair['jd_text'], pair['cv_text']))
        
        # Make batch predictions
        results = batch_predict(jd_cv_pairs, request.topk)
        
        # Convert to response format
        response_results = [PredictionResponse(**result) for result in results]
        
        return BatchPredictionResponse(results=response_results)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.post("/predict/files", response_model=PredictionResponse)
async def predict_from_files(
    jd_file: UploadFile = File(..., description="Job description file"),
    cv_file: UploadFile = File(..., description="CV file"),
    topk: int = Form(default=6, description="Number of top features to return")
):
    """
    Predict matching score from uploaded files
    
    Args:
        jd_file: Job description file (txt, pdf, docx)
        cv_file: CV file (txt, pdf, docx)
        topk: Number of top features to return
        
    Returns:
        PredictionResponse with score, percent, features, and latency
    """
    try:
        logger.info(f"Received file prediction request - JD: {jd_file.filename}, CV: {cv_file.filename}")
        
        # Extract text from files
        jd_text = await extract_text_from_file(jd_file)
        cv_text = await extract_text_from_file(cv_file)
        
        if not jd_text or not cv_text:
            raise HTTPException(status_code=400, detail="Could not extract text from files")
        
        # Make prediction
        result = predict(jd_text, cv_text, topk)
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in file prediction: {e}")
        raise HTTPException(status_code=500, detail=f"File prediction failed: {str(e)}")


@app.post("/predict/batch")
async def predict_batch_files(
    jd_file: UploadFile = File(..., description="JD PDF (required)"),
    cv_files: List[UploadFile] = File(..., description="One or more CV PDFs (required)"),
    topk: int = Form(default=6)
):
    """Multipart batch: one JD PDF against many CV PDFs.

    Returns: { jd_name, results: [{ cv_name, score, percent, features, latency_ms }] }
    """
    # Basic validations
    if jd_file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="JD must be a PDF")
    if not cv_files or len(cv_files) == 0:
        raise HTTPException(status_code=400, detail="No CVs uploaded")
    if len(cv_files) > 100:
        raise HTTPException(status_code=400, detail="Too many CV files (max 100)")

    for f in cv_files:
        if f.content_type != "application/pdf":
            raise HTTPException(status_code=415, detail=f"{f.filename} is not a PDF")

    # Extract JD text once
    jd_text = await extract_text_from_file(jd_file)
    results: List[dict] = []

    for cv in cv_files:
        t0 = time.monotonic()
        try:
            cv_text = await extract_text_from_file(cv)
            pred = predict(jd_text, cv_text, topk)
            latency = int((time.monotonic() - t0) * 1000)
            results.append({
                "cv_name": cv.filename,
                "score": float(pred.get("score", 0.0)),
                "percent": pred.get("percent", "0%"),
                "features": pred.get("features", []),
                "latency_ms": latency,
            })
        except Exception as e:  # pragma: no cover - robust logging in production
            logger.exception(f"Batch item failed {cv.filename}: {e}")
            results.append({
                "cv_name": cv.filename,
                "score": 0.0,
                "percent": "0%",
                "features": [],
                "latency_ms": 0,
            })

    return {"jd_name": jd_file.filename, "results": results}


async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extract text from uploaded file based on file type
    
    Args:
        file: Uploaded file
        
    Returns:
        Extracted text content
    """
    try:
        content = await file.read()
        
        # Determine file type
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        if file_extension == 'txt':
            return content.decode('utf-8')
        elif file_extension == 'pdf':
            return await extract_text_from_pdf(content)
        elif file_extension in ['doc', 'docx']:
            return await extract_text_from_docx(content)
        else:
            # Try to decode as text
            try:
                return content.decode('utf-8')
            except:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
                
    except Exception as e:
        logger.error(f"Error extracting text from file: {e}")
        raise HTTPException(status_code=400, detail=f"Could not extract text from file: {str(e)}")


async def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF content"""
    try:
        from pdfminer.high_level import extract_text
        from io import BytesIO
        return extract_text(BytesIO(content))
    except ImportError:
        raise HTTPException(status_code=500, detail="PDF processing not available")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF extraction failed: {str(e)}")


async def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX content"""
    try:
        from docx import Document
        from io import BytesIO
        doc = Document(BytesIO(content))
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        raise HTTPException(status_code=500, detail="DOCX processing not available")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX extraction failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Job-CV Matching API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_batch_json": "/predict/batch_json",
            "predict_files": "/predict/files",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
