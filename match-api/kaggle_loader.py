import os
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

load_dotenv()
logger = logging.getLogger("match-api.kaggle")


def ensure_model() -> str:
  """Ensure model file exists locally; download from Kaggle if missing.

  Environment variables:
  - KAGGLE_DATASET: e.g. "username/dataset_name"
  - KAGGLE_FILE: file name inside dataset, e.g. "model.pkl"
  - MODEL_LOCAL_PATH: local path to cache file, default ./artifacts/model.pkl
  - KAGGLE_USERNAME/KAGGLE_KEY or ~/.kaggle/kaggle.json must exist
  """
  dataset = os.getenv("KAGGLE_DATASET")
  remote_file = os.getenv("KAGGLE_FILE", "model.pkl")
  local_path = os.getenv("MODEL_LOCAL_PATH", "./artifacts/model.pkl")

  path = Path(local_path)
  path.parent.mkdir(parents=True, exist_ok=True)

  if path.exists() and path.stat().st_size > 0:
    logger.info("Model already present at %s", path)
    return str(path)

  if not dataset:
    logger.warning("KAGGLE_DATASET not set; assuming model will be created/placed at %s", path)
    return str(path)

  logger.info("Downloading model %s from Kaggle dataset %s ...", remote_file, dataset)
  api = KaggleApi()
  api.authenticate()
  api.dataset_download_file(dataset, remote_file, path=str(path.parent), force=False, quiet=False)

  # The Kaggle lib stores as .zip if multiple files; try both plain and .zip
  candidate = path
  zip_path = path.parent / f"{remote_file}.zip"

  if candidate.exists() and candidate.stat().st_size > 0:
    logger.info("Downloaded model to %s", candidate)
    return str(candidate)

  if zip_path.exists() and zip_path.stat().st_size > 0:
    import zipfile

    with zipfile.ZipFile(zip_path, 'r') as zf:
      zf.extractall(path.parent)
    if candidate.exists() and candidate.stat().st_size > 0:
      logger.info("Extracted model to %s", candidate)
      return str(candidate)

  raise RuntimeError("Failed to download model from Kaggle")


