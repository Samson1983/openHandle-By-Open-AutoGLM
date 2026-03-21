"""Test script to verify swipe duration limit."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Mock the requests module to avoid actual network calls
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def json(self):
        return self.json_data
    def raise_for_status(self):
        pass

# Mock the requests.get function
def mock_get(url, params=None, timeout=None):
    print(f"Mock HTTP GET: {url}")
    if params:
        print(f"Params: {params}")
        # Check if duration is <= 300ms
        if 'duration' in params:
            duration = params['duration']
            if duration > 300:
                print(f"ERROR: duration should be <= 300ms, but got {duration}ms")
                return MockResponse({"error": "duration too long"}, 400)
    return MockResponse({"success": True}, 200)

# Replace requests.get with our mock
import phone_agent.bleHttp.device
phone_agent.bleHttp.device.requests.get = mock_get

# Also mock ensure_connected
def mock_ensure_connected(base_url):
    print(f"Mock ensure_connected: {base_url}")

phone_agent.bleHttp.device.ensure_connected = mock_ensure_connected

# Import the swipe function
from phone_agent.bleHttp.device import swipe

print('Testing swipe duration limit...')

# Test with duration=500ms (should be limited to 300ms)
print('\nTest 1: duration=500ms')
try:
    result = swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 500)
    print('Result:', result)
except Exception as e:
    print(f'Error: {e}')

# Test with duration=200ms (should work as is)
print('\nTest 2: duration=200ms')
try:
    result = swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 200)
    print('Result:', result)
except Exception as e:
    print(f'Error: {e}')

# Test with duration=300ms (should work as is)
print('\nTest 3: duration=300ms')
try:
    result = swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 300)
    print('Result:', result)
except Exception as e:
    print(f'Error: {e}')

print('\nAll tests completed!')
