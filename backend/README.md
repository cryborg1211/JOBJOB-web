# Job-CV Matching API

A FastAPI service for matching job descriptions with CVs using TF-IDF vectorization and cosine similarity.

## Features

- **Text Preprocessing**: Advanced text cleaning, tokenization, and lemmatization
- **TF-IDF Matching**: Uses scikit-learn's TF-IDF vectorizer with cosine similarity
- **Keyword Extraction**: Identifies matching skills and keywords between JD and CV
- **File Support**: Supports text, PDF, and DOCX file uploads
- **Batch Processing**: Process multiple JD-CV pairs in a single request
- **CORS Enabled**: Ready for frontend integration

## API Endpoints

### Health Check
```
GET /health
```
Returns service status and version information.

### Single Prediction
```
POST /predict
```
**Request Body:**
```json
{
  "jd_text": "Job description text...",
  "cv_text": "CV text...",
  "topk": 6
}
```

**Response:**
```json
{
  "score": 0.82,
  "percent": "82%",
  "features": ["python", "django", "rest api", "postgresql", "aws", "docker"],
  "latency_ms": 45
}
```

### Batch Prediction
```
POST /predict/batch
```
**Request Body:**
```json
{
  "pairs": [
    {"jd_text": "Job 1...", "cv_text": "CV 1..."},
    {"jd_text": "Job 2...", "cv_text": "CV 2..."}
  ],
  "topk": 6
}
```

### File Upload Prediction
```
POST /predict/files
```
**Form Data:**
- `jd_file`: Job description file (txt, pdf, docx)
- `cv_file`: CV file (txt, pdf, docx)
- `topk`: Number of features to return (optional, default: 6)

## Installation

### Using pip

1. **Clone the repository:**
```bash
git clone <repository-url>
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Using Docker

1. **Build the image:**
```bash
docker build -t job-cv-matching .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 job-cv-matching
```

## Usage Examples

### Python Client

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "jd_text": "Looking for Python developer with Django experience...",
        "cv_text": "I am a Python developer with 5 years experience...",
        "topk": 6
    }
)
result = response.json()
print(f"Match: {result['percent']}")
print(f"Features: {result['features']}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "jd_text": "Senior Python Developer with Django experience",
       "cv_text": "Python developer with 5 years Django experience",
       "topk": 6
     }'
```

### JavaScript/Frontend

```javascript
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    jd_text: 'Job description...',
    cv_text: 'CV text...',
    topk: 6
  })
});

const result = await response.json();
console.log(`Match: ${result.percent}`);
console.log(`Features: ${result.features}`);
```

## Configuration

The service can be configured through environment variables:

- `MAX_FEATURES`: Maximum TF-IDF features (default: 10000)
- `NGRAM_RANGE`: N-gram range for TF-IDF (default: (1, 3))
- `LOG_LEVEL`: Logging level (default: INFO)

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Architecture

```
backend/
├── main.py              # FastAPI application
├── inference.py         # TF-IDF and cosine similarity logic
├── preprocess.py        # Text preprocessing and keyword extraction
├── nb_loader.py         # Notebook function extraction
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── README.md           # This file
```

## Performance

- **Typical latency**: 20-100ms per prediction
- **Throughput**: ~100 predictions/second
- **Memory usage**: ~200MB base + ~50MB per batch
- **File size limits**: 10MB per file upload

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid input)
- `422`: Validation error
- `500`: Internal server error

Error responses include detailed error messages:

```json
{
  "detail": "Error description"
}
```

## License

MIT License - see LICENSE file for details.
