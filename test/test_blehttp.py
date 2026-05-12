"""Test script for BLE HTTP module."""

from phone_agent.bleHttp import get_screenshot, connect, tap, home, back, recent_apps

print('Testing app function interfaces (no connection required)...')
try:
    screenshot = get_screenshot('http://192.168.2.152:9123')
    print('Screenshot successful (no connection required)')
    print(f'Screenshot size: {screenshot.width}x{screenshot.height}')
except Exception as e:
    print(f'Screenshot failed: {e}')

print('Testing Bluetooth interfaces (connection required)...')
try:
    tap('http://192.168.2.152:9123', 100, 100)
    print('Tap successful (connection automatically established)')
except Exception as e:
    print(f'Tap failed: {e}')

print('Testing function keys (should use device-specific config)...')
try:
    home('http://192.168.2.152:9123')
    print('Home button successful')
    back('http://192.168.2.152:9123')
    print('Back button successful')
    recent_apps('http://192.168.2.152:9123')
    print('Recent apps button successful')
except Exception as e:
    print(f'Function keys failed: {e}')

print('All tests completed!')
