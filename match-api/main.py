import os
import time
import logging
from typing import List, Optional, Tuple

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from dotenv import load_dotenv

from kaggle_loader import ensure_model
from inference import load_model, predict as model_predict, ModelHandle
from preprocess import clean_text, extract_text_from_file


# ---------- Env & logging ----------
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("match-api")

MODEL_LOCAL_PATH = os.getenv("MODEL_LOCAL_PATH", "./artifacts/model.pkl")
ORIGINS = ["http://localhost:5173"]
REQUEST_TIMEOUT_SEC = 15
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))


# ---------- Pydantic models ----------
class PredictIn(BaseModel):
    jd_text: str = Field(..., max_length=50000)
    cv_text: str = Field(..., max_length=50000)


class PredictOut(BaseModel):
    score: float
    percent: str
    features: List[str]
    latency_ms: float


# ---------- App & CORS ----------
app = FastAPI(title="match-api", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Simple in-memory rate limiter ----------
class TokenBucket:
    def __init__(self, rate_per_min: int):
        self.capacity = rate_per_min
        self.tokens = rate_per_min
        self.last = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.last
        refill = (elapsed / 60.0) * self.capacity
        if refill > 0:
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


rate_buckets = {}


def rate_limit_dependency(request: Request):
    ip = request.client.host if request.client else "unknown"
    bucket = rate_buckets.setdefault(ip, TokenBucket(RATE_LIMIT_PER_MIN))
    if not bucket.allow():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


# ---------- Model lifecycle ----------
model_handle: Optional[ModelHandle] = None


@app.on_event("startup")
def startup_event():
    os.makedirs(os.path.dirname(MODEL_LOCAL_PATH), exist_ok=True)
    ensure_model()
    global model_handle
    model_handle = load_model(MODEL_LOCAL_PATH)
    logger.info("Model loaded and ready")


@app.get("/health")
def health():
    return {"ok": True}


def _predict_impl(jd_text: str, cv_text: str) -> PredictOut:
    if model_handle is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    t0 = time.monotonic()
    jd = clean_text(jd_text)
    cv = clean_text(cv_text)
    score, features = model_predict(model_handle, jd, cv)
    latency_ms = (time.monotonic() - t0) * 1000.0
    return PredictOut(
        score=float(score),
        percent=f"{round(float(score)*100)}%",
        features=features,
        latency_ms=round(latency_ms, 2),
    )


@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn, _: None = Depends(rate_limit_dependency)):
    try:
        return _predict_impl(payload.jd_text, payload.cv_text)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Predict error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/files", response_model=PredictOut)
async def predict_files(
    jd_file: UploadFile = File(...),
    cv_file: UploadFile = File(...),
    _: None = Depends(rate_limit_dependency),
):
    try:
        jd_text = await extract_text_from_file(jd_file)
        cv_text = await extract_text_from_file(cv_file)
        return _predict_impl(jd_text, cv_text)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Predict files error")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


