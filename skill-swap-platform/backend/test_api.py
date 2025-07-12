import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login functionality"""
    print("Testing login...")
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
    print(f"Login status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Login successful for user: {data['user']['name']}")
        return data['token']
    else:
        print(f"Login failed: {response.text}")
        return None

def test_profile(token):
    """Test profile endpoint with token"""
    print("\nTesting profile endpoint...")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/profile', headers=headers)
    print(f"Profile status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Profile loaded: {data['name']} ({data['email']})")
        return True
    else:
        print(f"Profile failed: {response.text}")
        return False

def test_skills():
    """Test skills endpoint (public)"""
    print("\nTesting skills endpoint...")
    response = requests.get(f'{BASE_URL}/api/skills')
    print(f"Skills status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} skills")
        return data[0]['id'] if data else None
    else:
        print(f"Skills failed: {response.text}")
        return None

def test_create_request(token, skill_id):
    """Test creating a request"""
    print(f"\nTesting request creation for skill {skill_id}...")
    headers = {'Authorization': f'Bearer {token}'}
    request_data = {
        "skillId": skill_id,
        "message": "I would like to learn this skill!"
    }
    
    response = requests.post(f'{BASE_URL}/api/requests', json=request_data, headers=headers)
    print(f"Request creation status: {response.status_code}")
    
    if response.status_code == 201:
        print("Request created successfully!")
        return True
    else:
        print(f"Request creation failed: {response.text}")
        return False

def test_requests(token):
    """Test requests endpoints"""
    print("\nTesting requests endpoints...")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test sent requests
    response = requests.get(f'{BASE_URL}/api/requests/sent', headers=headers)
    print(f"Sent requests status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} sent requests")
    else:
        print(f"Sent requests failed: {response.text}")
    
    # Test received requests
    response = requests.get(f'{BASE_URL}/api/requests/received', headers=headers)
    print(f"Received requests status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} received requests")
    else:
        print(f"Received requests failed: {response.text}")

if __name__ == '__main__':
    print("=== API Test Suite ===\n")
    
    # Wait a moment for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Test login
    token = test_login()
    
    if token:
        # Test profile
        test_profile(token)
        
        # Test skills
        skill_id = test_skills()
        
        if skill_id:
            # Test request creation
            test_create_request(token, skill_id)
        
        # Test requests
        test_requests(token)
    
    print("\n=== Test Complete ===") 