import os
import time
import logging
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from joblib import load as joblib_load
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from rapidfuzz import process, fuzz

load_dotenv()
logger = logging.getLogger("match-api.inference")


@dataclass
class ModelHandle:
    kind: str  # "pickle" | "st"
    model: object
    encoder: object | None = None


def load_model(local_path: str) -> ModelHandle:
    """Load model from pickle or sentence-transformers name via env.

    If `SENTENCE_TRANSFORMERS_MODEL` is set, load that and return kind="st".
    Otherwise try loading a pickle model from `local_path`.
    """
    st_name = os.getenv("SENTENCE_TRANSFORMERS_MODEL")
    if st_name:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading sentence-transformers model: %s", st_name)
        model = SentenceTransformer(st_name)
        return ModelHandle(kind="st", model=model, encoder=model)

    logger.info("Loading pickle model at %s", local_path)
    model = joblib_load(local_path)
    return ModelHandle(kind="pickle", model=model, encoder=None)


def _predict_st(handle: ModelHandle, jd_text: str, cv_text: str) -> float:
    emb = handle.encoder.encode([jd_text, cv_text])
    score = float(cosine_similarity([emb[0]], [emb[1]])[0, 0])
    score = max(0.0, min(1.0, score))
    return score


def _predict_pickle(handle: ModelHandle, jd_text: str, cv_text: str) -> float:
    model = handle.model
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([f"JD: {jd_text}\nCV: {cv_text}"])
        score = float(proba[0][-1])
    elif hasattr(model, "predict"):
        pred = model.predict([f"JD: {jd_text}\nCV: {cv_text}"])
        score = float(pred[0])
        score = max(0.0, min(1.0, score))
    else:
        raise RuntimeError("Unsupported pickle model type")
    return score


def _extract_features(jd_text: str, cv_text: str, k: int = 6) -> List[str]:
    jd_keys = [s.strip() for s in jd_text.split() if len(s) > 3]
    cv = cv_text
    matches = process.extract(
        " ".join(jd_keys[:120]),
        [" ".join(cv_text.split()[i:i+5]) for i in range(0, len(cv_text.split()), 5)],
        scorer=fuzz.partial_ratio,
        limit=k,
    )
    features = [m[0][:42] for m in matches]
    return features


def predict(handle: ModelHandle, jd_text: str, cv_text: str) -> Tuple[float, List[str]]:
    if handle.kind == "st":
        score = _predict_st(handle, jd_text, cv_text)
    else:
        score = _predict_pickle(handle, jd_text, cv_text)
    features = _extract_features(jd_text, cv_text, k=6)
    return score, features


