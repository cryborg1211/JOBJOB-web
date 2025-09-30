"""
Test script for the Job-CV matching API
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_predict():
    """Test prediction endpoint"""
    print("\nTesting prediction endpoint...")
    
    test_data = {
        "jd_text": "We are looking for a Senior Python Developer with experience in Django, Flask, REST API development, PostgreSQL, Redis, AWS, Docker, and Machine Learning. 5+ years experience required.",
        "cv_text": "I am a Python Developer with 6 years of experience in Django, FastAPI, REST API and GraphQL development. I have worked with PostgreSQL, MongoDB, AWS, Docker, Jenkins, and have a strong background in Machine Learning with PyTorch and Data Science.",
        "topk": 6
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   Score: {data['score']:.3f}")
            print(f"   Percent: {data['percent']}")
            print(f"   Features: {data['features']}")
            print(f"   Latency: {data['latency_ms']}ms")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_batch_predict():
    """Test batch prediction endpoint"""
    print("\nTesting batch prediction endpoint...")
    
    test_data = {
        "pairs": [
            {
                "jd_text": "Looking for Python developer with Django experience",
                "cv_text": "I am a Python developer with 5 years Django experience"
            },
            {
                "jd_text": "Looking for Java developer with Spring Boot experience",
                "cv_text": "I am a Java developer with 3 years Spring Boot experience"
            }
        ],
        "topk": 4
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch prediction successful:")
            for i, result in enumerate(data['results']):
                print(f"   Pair {i+1}: Score={result['score']:.3f}, Features={result['features']}")
            return True
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch prediction error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint successful: {data['message']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print(f"Testing API at: {BASE_URL}")
    
    tests = [
        test_health,
        test_root,
        test_predict,
        test_batch_predict
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server.")

if __name__ == "__main__":
    main()
