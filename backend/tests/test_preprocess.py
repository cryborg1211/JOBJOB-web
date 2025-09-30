"""
Unit tests for preprocess module
"""
import pytest
from preprocess import clean_for_model, extract_keywords, extract_skills_from_text, preprocess_text_pipeline


class TestCleanForModel:
    """Test cases for clean_for_model function"""
    
    def test_clean_basic_text(self):
        """Test basic text cleaning"""
        text = "Hello World! This is a test."
        result = clean_for_model(text)
        assert isinstance(result, str)
        assert "hello" in result
        assert "world" in result
        assert "!" not in result
    
    def test_clean_html_text(self):
        """Test cleaning HTML text"""
        text = "<p>Hello <b>World</b>!</p>"
        result = clean_for_model(text)
        assert "<" not in result
        assert ">" not in result
        assert "hello" in result
        assert "world" in result
    
    def test_clean_url_text(self):
        """Test cleaning URLs"""
        text = "Visit https://example.com for more info"
        result = clean_for_model(text)
        assert "https://example.com" not in result
        assert "visit" in result
        assert "more" in result
        assert "info" in result
    
    def test_clean_email_text(self):
        """Test cleaning email addresses"""
        text = "Contact me at john@example.com"
        result = clean_for_model(text)
        assert "john@example.com" not in result
        assert "contact" in result
        assert "john" not in result
    
    def test_clean_empty_text(self):
        """Test cleaning empty or None text"""
        assert clean_for_model("") == ""
        assert clean_for_model(None) == ""
    
    def test_clean_special_characters(self):
        """Test cleaning special characters"""
        text = "Hello@#$%^&*()World!"
        result = clean_for_model(text)
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
        assert "hello" in result
        assert "world" in result


class TestExtractKeywords:
    """Test cases for extract_keywords function"""
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        jd_text = "Looking for Python developer with Django experience"
        cv_text = "I am a Python developer with 5 years Django experience"
        keywords = extract_keywords(jd_text, cv_text, topk=3)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 3
        assert any("python" in kw.lower() for kw in keywords)
        assert any("django" in kw.lower() for kw in keywords)
    
    def test_extract_keywords_no_match(self):
        """Test keyword extraction with no matches"""
        jd_text = "Looking for Java developer"
        cv_text = "I am a Python developer"
        keywords = extract_keywords(jd_text, cv_text, topk=3)
        
        assert isinstance(keywords, list)
        assert len(keywords) == 0
    
    def test_extract_keywords_empty_input(self):
        """Test keyword extraction with empty inputs"""
        assert extract_keywords("", "test") == []
        assert extract_keywords("test", "") == []
        assert extract_keywords("", "") == []
    
    def test_extract_keywords_topk_limit(self):
        """Test keyword extraction respects topk limit"""
        jd_text = "Python Django Flask React JavaScript TypeScript"
        cv_text = "Python Django Flask React JavaScript TypeScript"
        keywords = extract_keywords(jd_text, cv_text, topk=2)
        
        assert len(keywords) <= 2


class TestExtractSkillsFromText:
    """Test cases for extract_skills_from_text function"""
    
    def test_extract_technical_skills(self):
        """Test extraction of technical skills"""
        text = "I have experience with Python, Django, React, and AWS"
        skills = extract_skills_from_text(text)
        
        assert isinstance(skills, list)
        assert any("python" in skill.lower() for skill in skills)
        assert any("django" in skill.lower() for skill in skills)
        assert any("react" in skill.lower() for skill in skills)
        assert any("aws" in skill.lower() for skill in skills)
    
    def test_extract_education_skills(self):
        """Test extraction of education-related terms"""
        text = "I have a Bachelor's degree in Computer Science"
        skills = extract_skills_from_text(text)
        
        assert isinstance(skills, list)
        assert any("bachelor" in skill.lower() for skill in skills)
        assert any("degree" in skill.lower() for skill in skills)
    
    def test_extract_empty_text(self):
        """Test extraction from empty text"""
        assert extract_skills_from_text("") == []
        assert extract_skills_from_text(None) == []


class TestPreprocessTextPipeline:
    """Test cases for preprocess_text_pipeline function"""
    
    def test_pipeline_basic(self):
        """Test basic pipeline functionality"""
        text = "I am a Python developer with Django experience"
        cleaned, skills = preprocess_text_pipeline(text)
        
        assert isinstance(cleaned, str)
        assert isinstance(skills, list)
        assert "python" in cleaned.lower()
        assert "django" in cleaned.lower()
    
    def test_pipeline_empty_input(self):
        """Test pipeline with empty input"""
        cleaned, skills = preprocess_text_pipeline("")
        assert cleaned == ""
        assert skills == []


if __name__ == "__main__":
    pytest.main([__file__])
