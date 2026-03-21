"""Test script to check if all BLE HTTP interfaces are properly exported."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Try to import directly from the bleHttp module files
print('Checking BLE HTTP module exports...')

try:
    # Check if get_app_list is in connection.py
    from phone_agent.bleHttp.connection import get_app_list
    print('✓ get_app_list is available in connection.py')
except ImportError as e:
    print(f'✗ get_app_list is not available: {e}')

try:
    # Check if type_text is in input.py
    from phone_agent.bleHttp.input import type_text
    print('✓ type_text is available in input.py')
except ImportError as e:
    print(f'✗ type_text is not available: {e}')

try:
    # Check if all interfaces are in __init__.py
    from phone_agent.bleHttp import (
        connect, get_state, get_app_list, get_screenshot,
        tap, swipe, long_press, back, home, recent_apps,
        type_text, copy, paste
    )
    print('✓ All interfaces are available in phone_agent.bleHttp')
except ImportError as e:
    print(f'✗ Some interfaces are not available: {e}')

print('\nChecking __all__ list in __init__.py...')
try:
    from phone_agent.bleHttp import __all__
    print(f'✓ __all__ list found with {len(__all__)} items')
    print('  Interfaces in __all__:')
    for item in __all__:
        print(f'    - {item}')
    
    # Check if specific interfaces are in __all__
    required_interfaces = ['get_app_list', 'type_text']
    for interface in required_interfaces:
        if interface in __all__:
            print(f'✓ {interface} is in __all__')
        else:
            print(f'✗ {interface} is not in __all__')
            
except Exception as e:
    print(f'✗ Error checking __all__: {e}')

print('\nAll checks completed!')
