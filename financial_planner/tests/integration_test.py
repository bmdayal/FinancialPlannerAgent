import requests
import json

BASE = 'http://localhost:5000'

def test_calculate():
    url = f"{BASE}/calculate"
    payload = {
        'age': 35,
        'current_savings': 100000,
        'annual_income': 85000,
        'retirement_age': 65,
        'children': [
            {'age': 5, 'education_goal': 'college'},
            {'age': 2, 'education_goal': 'college'}
        ]
    }
    r = requests.post(url, json=payload, timeout=10)
    print('calculate status:', r.status_code)
    try:
        data = r.json()
        print('Keys in response:', list(data.keys()))
    except Exception as e:
        print('Failed to parse JSON:', e)

def test_chat():
    url = f"{BASE}/chat"
    payload = {
        'message': 'Based on my inputs, will I run out of money in retirement?',
        'financialData': {
            'age': 35,
            'current_savings': 100000,
            'annual_income': 85000,
            'retirement_age': 65,
            'children': [
                {'age': 5, 'education_goal': 'college'},
                {'age': 2, 'education_goal': 'college'}
            ]
        }
    }
    r = requests.post(url, json=payload, timeout=10)
    print('chat status:', r.status_code)
    try:
        print('chat response:', r.json())
    except Exception as e:
        print('Failed to parse chat JSON:', e)

if __name__ == '__main__':
    print('Running integration tests against', BASE)
    test_calculate()
    test_chat()
