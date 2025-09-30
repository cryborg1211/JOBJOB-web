"""
Inference module for job-CV matching using TF-IDF and cosine similarity
"""
import time
import logging
from typing import Tuple, List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import clean_for_model, extract_keywords

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobCVMatchingModel:
    """
    Job-CV matching model using TF-IDF vectorization and cosine similarity
    """
    
    def __init__(self, max_features: int = 10000, ngram_range: Tuple[int, int] = (1, 3)):
        """
        Initialize the matching model
        
        Args:
            max_features: Maximum number of features for TF-IDF
            ngram_range: Range of n-grams to consider
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True,
            strip_accents='unicode',
            analyzer='word',
            token_pattern=r'\b\w+\b',
            min_df=1,
            max_df=0.95
        )
        self.is_fitted = False
        
    def _preprocess_texts(self, jd_text: str, cv_text: str) -> Tuple[str, str]:
        """
        Preprocess job description and CV texts
        
        Args:
            jd_text: Job description text
            cv_text: CV text
            
        Returns:
            Tuple of cleaned texts
        """
        jd_clean = clean_for_model(jd_text)
        cv_clean = clean_for_model(cv_text)
        
        return jd_clean, cv_clean
    
    def _calculate_similarity(self, jd_text: str, cv_text: str) -> float:
        """
        Calculate cosine similarity between JD and CV
        
        Args:
            jd_text: Cleaned job description text
            cv_text: Cleaned CV text
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        try:
            # Fit vectorizer on both texts
            texts = [jd_text, cv_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = similarity_matrix[0][0]
            
            # Ensure score is between 0 and 1
            similarity_score = max(0.0, min(1.0, similarity_score))
            
            return float(similarity_score)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def predict(self, jd_text: str, cv_text: str, topk: int = 6) -> Dict[str, Any]:
        """
        Predict matching score between job description and CV
        
        Args:
            jd_text: Job description text
            cv_text: CV text
            topk: Number of top matching features to return
            
        Returns:
            Dictionary containing score, percent, features, and latency
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not jd_text or not cv_text:
                return {
                    'score': 0.0,
                    'percent': '0%',
                    'features': [],
                    'latency_ms': 0
                }
            
            # Preprocess texts
            jd_clean, cv_clean = self._preprocess_texts(jd_text, cv_text)
            
            if not jd_clean or not cv_clean:
                return {
                    'score': 0.0,
                    'percent': '0%',
                    'features': [],
                    'latency_ms': 0
                }
            
            # Calculate similarity score
            score = self._calculate_similarity(jd_clean, cv_clean)
            
            # Extract matching features/keywords
            features = extract_keywords(jd_text, cv_text, topk=topk)
            
            # Calculate percentage
            percent = f"{int(score * 100)}%"
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"Prediction completed - Score: {score:.3f}, Features: {len(features)}, Latency: {latency_ms}ms")
            
            return {
                'score': score,
                'percent': percent,
                'features': features,
                'latency_ms': latency_ms
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                'score': 0.0,
                'percent': '0%',
                'features': [],
                'latency_ms': latency_ms
            }


# Global model instance
_model_instance = None


def get_model() -> JobCVMatchingModel:
    """
    Get or create the global model instance
    """
    global _model_instance
    if _model_instance is None:
        _model_instance = JobCVMatchingModel()
    return _model_instance


def predict(jd_text: str, cv_text: str, topk: int = 6) -> Dict[str, Any]:
    """
    Convenience function to make predictions
    
    Args:
        jd_text: Job description text
        cv_text: CV text
        topk: Number of top matching features to return
        
    Returns:
        Dictionary containing prediction results
    """
    model = get_model()
    return model.predict(jd_text, cv_text, topk)


def batch_predict(jd_cv_pairs: List[Tuple[str, str]], topk: int = 6) -> List[Dict[str, Any]]:
    """
    Make predictions for multiple JD-CV pairs
    
    Args:
        jd_cv_pairs: List of (jd_text, cv_text) tuples
        topk: Number of top matching features to return
        
    Returns:
        List of prediction results
    """
    model = get_model()
    results = []
    
    for jd_text, cv_text in jd_cv_pairs:
        result = model.predict(jd_text, cv_text, topk)
        results.append(result)
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Test the model
    jd_sample = """
    We are looking for a Senior Python Developer with experience in:
    - Python, Django, Flask
    - REST API development
    - PostgreSQL, Redis
    - AWS, Docker, Kubernetes
    - Machine Learning, TensorFlow
    - 5+ years experience
    """
    
    cv_sample = """
    I am a Python Developer with 6 years of experience:
    - Python, Django, FastAPI
    - REST API and GraphQL
    - PostgreSQL, MongoDB
    - AWS, Docker, Jenkins
    - Machine Learning, PyTorch
    - Data Science background
    """
    
    result = predict(jd_sample, cv_sample)
    print("Prediction Result:")
    print(f"Score: {result['score']:.3f}")
    print(f"Percent: {result['percent']}")
    print(f"Features: {result['features']}")
    print(f"Latency: {result['latency_ms']}ms")
