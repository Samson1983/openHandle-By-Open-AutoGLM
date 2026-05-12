"""Test script for all BLE HTTP interfaces."""

from phone_agent.bleHttp import (
    connect, get_state, get_app_list, get_screenshot,
    tap, swipe, long_press, back, home, recent_apps,
    type_text, copy, paste
)

print('Testing all BLE HTTP interfaces...')

# Test connection related interfaces
print('\n1. Testing connection interfaces:')
try:
    connect('http://192.168.2.152:9123')
    print('   connect: successful')
except Exception as e:
    print(f'   connect: failed - {e}')

try:
    state = get_state('http://192.168.2.152:9123')
    print('   get_state: successful')
except Exception as e:
    print(f'   get_state: failed - {e}')

try:
    app_list = get_app_list('http://192.168.2.152:9123')
    print(f'   get_app_list: successful (found {len(app_list.get("data", []))} apps)')
except Exception as e:
    print(f'   get_app_list: failed - {e}')

# Test device control interfaces
print('\n2. Testing device control interfaces:')
try:
    tap('http://192.168.2.152:9123', 100, 100)
    print('   tap: successful')
except Exception as e:
    print(f'   tap: failed - {e}')

try:
    swipe('http://192.168.2.152:9123', 100, 100, 200, 200, 500)  # Should be limited to 300ms
    print('   swipe: successful')
except Exception as e:
    print(f'   swipe: failed - {e}')

try:
    long_press('http://192.168.2.152:9123', 100, 100, 500)
    print('   long_press: successful')
except Exception as e:
    print(f'   long_press: failed - {e}')

try:
    back('http://192.168.2.152:9123')
    print('   back: successful')
except Exception as e:
    print(f'   back: failed - {e}')

try:
    home('http://192.168.2.152:9123')
    print('   home: successful')
except Exception as e:
    print(f'   home: failed - {e}')

try:
    recent_apps('http://192.168.2.152:9123')
    print('   recent_apps: successful')
except Exception as e:
    print(f'   recent_apps: failed - {e}')

# Test input interfaces
print('\n3. Testing input interfaces:')
try:
    type_text('http://192.168.2.152:9123', 500, 1000, '测试文本')
    print('   type_text: successful')
except Exception as e:
    print(f'   type_text: failed - {e}')

try:
    copy('http://192.168.2.152:9123')
    print('   copy: successful')
except Exception as e:
    print(f'   copy: failed - {e}')

try:
    paste('http://192.168.2.152:9123')
    print('   paste: successful')
except Exception as e:
    print(f'   paste: failed - {e}')

# Test screenshot interface
print('\n4. Testing screenshot interface:')
try:
    screenshot = get_screenshot('http://192.168.2.152:9123')
    print(f'   get_screenshot: successful (size: {screenshot.width}x{screenshot.height})')
except Exception as e:
    print(f'   get_screenshot: failed - {e}')

print('\nAll tests completed!')
