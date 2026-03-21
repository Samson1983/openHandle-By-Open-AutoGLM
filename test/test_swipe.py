"""Test script for swipe function."""

from phone_agent.bleHttp import swipe

print('Testing swipe with duration=500ms (should be limited to 300ms)...')
try:
    result = swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 500)
    print('Swipe successful')
except Exception as e:
    print(f'Swipe failed: {e}')

print('Testing swipe with duration=200ms (should work as is)...')
try:
    result = swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 200)
    print('Swipe successful')
except Exception as e:
    print(f'Swipe failed: {e}')

print('All tests completed!')
