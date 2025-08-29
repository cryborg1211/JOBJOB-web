#!/usr/bin/env python3
"""
Test script for /api/jobs endpoint
"""
import requests
import json

def test_api():
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test /api/jobs endpoint
        response = requests.get(f"{base_url}/api/jobs?offset=0&limit=5")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is Flask server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
