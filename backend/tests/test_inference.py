"""
Unit tests for inference module
"""
import pytest
import time
from inference import JobCVMatchingModel, predict, batch_predict


class TestJobCVMatchingModel:
    """Test cases for JobCVMatchingModel class"""
    
    def test_model_initialization(self):
        """Test model initialization"""
        model = JobCVMatchingModel()
        assert model.max_features == 10000
        assert model.ngram_range == (1, 3)
        assert not model.is_fitted
    
    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters"""
        model = JobCVMatchingModel(max_features=5000, ngram_range=(1, 2))
        assert model.max_features == 5000
        assert model.ngram_range == (1, 2)
    
    def test_preprocess_texts(self):
        """Test text preprocessing"""
        model = JobCVMatchingModel()
        jd_text = "Looking for Python developer"
        cv_text = "I am a Python developer"
        
        jd_clean, cv_clean = model._preprocess_texts(jd_text, cv_text)
        
        assert isinstance(jd_clean, str)
        assert isinstance(cv_clean, str)
        assert "python" in jd_clean.lower()
        assert "python" in cv_clean.lower()
    
    def test_calculate_similarity_identical_texts(self):
        """Test similarity calculation with identical texts"""
        model = JobCVMatchingModel()
        text = "Python developer with Django experience"
        
        similarity = model._calculate_similarity(text, text)
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0.8  # Should be very similar
    
    def test_calculate_similarity_different_texts(self):
        """Test similarity calculation with different texts"""
        model = JobCVMatchingModel()
        jd_text = "Looking for Python developer"
        cv_text = "I am a Java developer"
        
        similarity = model._calculate_similarity(jd_text, cv_text)
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        assert similarity < 0.5  # Should be less similar
    
    def test_calculate_similarity_empty_texts(self):
        """Test similarity calculation with empty texts"""
        model = JobCVMatchingModel()
        
        similarity = model._calculate_similarity("", "")
        assert similarity == 0.0
        
        similarity = model._calculate_similarity("test", "")
        assert similarity == 0.0
    
    def test_predict_basic(self):
        """Test basic prediction"""
        model = JobCVMatchingModel()
        jd_text = "Looking for Python developer with Django experience"
        cv_text = "I am a Python developer with 5 years Django experience"
        
        result = model.predict(jd_text, cv_text, topk=3)
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'percent' in result
        assert 'features' in result
        assert 'latency_ms' in result
        
        assert isinstance(result['score'], float)
        assert 0.0 <= result['score'] <= 1.0
        assert isinstance(result['percent'], str)
        assert '%' in result['percent']
        assert isinstance(result['features'], list)
        assert len(result['features']) <= 3
        assert isinstance(result['latency_ms'], int)
        assert result['latency_ms'] >= 0
    
    def test_predict_empty_inputs(self):
        """Test prediction with empty inputs"""
        model = JobCVMatchingModel()
        
        result = model.predict("", "test")
        assert result['score'] == 0.0
        assert result['percent'] == '0%'
        assert result['features'] == []
        
        result = model.predict("test", "")
        assert result['score'] == 0.0
        assert result['percent'] == '0%'
        assert result['features'] == []
    
    def test_predict_high_similarity(self):
        """Test prediction with highly similar texts"""
        model = JobCVMatchingModel()
        jd_text = "Senior Python Developer with Django, Flask, and REST API experience"
        cv_text = "Python Developer with 5 years experience in Django, Flask, and REST API development"
        
        result = model.predict(jd_text, cv_text, topk=5)
        
        assert result['score'] > 0.7  # Should be highly similar
        assert len(result['features']) > 0
        assert any('python' in f.lower() for f in result['features'])
        assert any('django' in f.lower() for f in result['features'])


class TestPredictFunction:
    """Test cases for predict function"""
    
    def test_predict_function(self):
        """Test the convenience predict function"""
        jd_text = "Looking for Python developer"
        cv_text = "I am a Python developer"
        
        result = predict(jd_text, cv_text, topk=3)
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'percent' in result
        assert 'features' in result
        assert 'latency_ms' in result
    
    def test_predict_function_empty_inputs(self):
        """Test predict function with empty inputs"""
        result = predict("", "")
        assert result['score'] == 0.0
        assert result['percent'] == '0%'
        assert result['features'] == []


class TestBatchPredict:
    """Test cases for batch_predict function"""
    
    def test_batch_predict_basic(self):
        """Test basic batch prediction"""
        pairs = [
            ("Looking for Python developer", "I am a Python developer"),
            ("Looking for Java developer", "I am a Java developer")
        ]
        
        results = batch_predict(pairs, topk=3)
        
        assert isinstance(results, list)
        assert len(results) == 2
        
        for result in results:
            assert isinstance(result, dict)
            assert 'score' in result
            assert 'percent' in result
            assert 'features' in result
            assert 'latency_ms' in result
    
    def test_batch_predict_empty_list(self):
        """Test batch prediction with empty list"""
        results = batch_predict([], topk=3)
        assert results == []
    
    def test_batch_predict_mixed_quality(self):
        """Test batch prediction with mixed quality matches"""
        pairs = [
            ("Python developer", "Python developer"),  # High similarity
            ("Python developer", "Java developer"),    # Low similarity
            ("", "test"),                               # Empty input
        ]
        
        results = batch_predict(pairs, topk=3)
        
        assert len(results) == 3
        assert results[0]['score'] > results[1]['score']  # First should be more similar
        assert results[2]['score'] == 0.0  # Empty input should return 0


class TestPerformance:
    """Test cases for performance aspects"""
    
    def test_prediction_latency(self):
        """Test that prediction completes within reasonable time"""
        jd_text = "Looking for Python developer with Django experience"
        cv_text = "I am a Python developer with 5 years Django experience"
        
        start_time = time.time()
        result = predict(jd_text, cv_text)
        end_time = time.time()
        
        latency_ms = (end_time - start_time) * 1000
        assert latency_ms < 5000  # Should complete within 5 seconds
        assert result['latency_ms'] > 0
        assert result['latency_ms'] < 5000
    
    def test_batch_prediction_latency(self):
        """Test batch prediction latency"""
        pairs = [
            ("Python developer", "Python developer"),
            ("Java developer", "Java developer"),
            ("React developer", "React developer")
        ]
        
        start_time = time.time()
        results = batch_predict(pairs, topk=3)
        end_time = time.time()
        
        total_latency = (end_time - start_time) * 1000
        assert total_latency < 10000  # Should complete within 10 seconds
        assert len(results) == 3


if __name__ == "__main__":
    pytest.main([__file__])
