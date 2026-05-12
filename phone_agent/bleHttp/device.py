"""Device control utilities for Android automation via BLE HTTP."""

import json
import os
import requests
import logging
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Load device configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'device_config.json')

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    DEVICE_CONFIG = json.load(f)

# Global connection manager
_connection_manager = None

from phone_agent.bleHttp.connection import BLEConnection

def get_connection_manager(base_url: str) -> BLEConnection:
    """
    Get or create a connection manager for the given base URL.
    
    Args:
        base_url: Base URL of the BLE HTTP server.
        
    Returns:
        BLEConnection instance.
    """
    global _connection_manager
    if _connection_manager is None or _connection_manager.base_url != base_url:
        _connection_manager = BLEConnection(base_url)
    return _connection_manager

def ensure_connected(base_url: str) -> None:
    """
    Ensure the device is connected before using any BLE HTTP interface.
    
    Args:
        base_url: Base URL of the BLE HTTP server.
        
    Raises:
        Exception: If connection fails.
    """
    conn = get_connection_manager(base_url)
    if not conn.connected:
        conn.connect()

def get_device_config(base_url: str, key_type: str) -> Dict[str, Any]:
    """
    Get device configuration based on system info.

    Args:
        base_url: Base URL of the BLE HTTP server.
        key_type: Type of key to get configuration for (home, back, recent_apps).

    Returns:
        Configuration dictionary for the key.
    """
    conn = get_connection_manager(base_url)
    system_info = conn.get_system_info()

    # Extract device model and Android version
    model = system_info.get('model', '').strip()
    android_version = system_info.get('version', '').strip()

    # Normalize version format (e.g., "12" -> "android_12")
    version_key = f"android_{android_version.lower()}"

    # Try to get configuration for specific device and version
    if model in DEVICE_CONFIG.get('device_configs', {}) and \
       version_key in DEVICE_CONFIG['device_configs'][model]:
        device_config = DEVICE_CONFIG['device_configs'][model][version_key]
        if key_type in device_config:
            return device_config[key_type]

    # Fall back to default configuration
    return DEVICE_CONFIG.get('default_config', {}).get(key_type, {})


def tap(base_url: str, x: int, y: int) -> Dict[str, Any]:
    """
    Tap at the specified coordinates.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x: X coordinate.
        y: Y coordinate.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/click"
    params = {"x": x, "y": y}
    logger.info(f"BLE HTTP: Tapping at ({x}, {y})")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Tap response: {response.json()}")
    return response.json()


def long_press(base_url: str, x: int, y: int, duration: int = 1000) -> Dict[str, Any]:
    """
    Long press at the specified coordinates.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x: X coordinate.
        y: Y coordinate.
        duration: Duration of press in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/press"
    params = {"x": x, "y": y, "duration": duration}
    logger.info(f"BLE HTTP: Long pressing at ({x}, {y}) for {duration}ms")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Long press response: {response.json()}")
    return response.json()


def swipe(base_url: str, x1: int, y1: int, x2: int, y2: int, duration: int = 100) -> Dict[str, Any]:
    """
    Swipe from start to end coordinates.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x1: Starting X coordinate.
        y1: Starting Y coordinate.
        x2: Ending X coordinate.
        y2: Ending Y coordinate.
        duration: Duration of swipe in milliseconds(max 300ms).

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    # Limit duration to maximum 300ms
    duration = min(duration, 300)
    url = f"{base_url}/swipe"
    params = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration": duration}
    logger.info(f"BLE HTTP: Swiping from ({x1}, {y1}) to ({x2}, {y2}) in {duration}ms")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Swipe response: {response.json()}")
    return response.json()


def swipe_with_speed(base_url: str, x1: int, y1: int, x2: int, y2: int, speed: float = 1.5) -> Dict[str, Any]:
    """
    Swipe with speed control.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x1: Starting X coordinate.
        y1: Starting Y coordinate.
        x2: Ending X coordinate.
        y2: Ending Y coordinate.
        speed: Speed factor (default: 1.5).

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/swipe1"
    params = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "s": speed}
    logger.info(f"BLE HTTP: Swiping with speed from ({x1}, {y1}) to ({x2}, {y2}) at speed {speed}")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Swipe with speed response: {response.json()}")
    return response.json()


def back(base_url: str) -> Dict[str, Any]:
    """
    Press the back button.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    config = get_device_config(base_url, "back")
    logger.info("BLE HTTP: Pressing back button")
    
    # Check if using direct endpoint or ikeyboard
    if "endpoint" in config:
        url = f"{base_url}{config['endpoint']}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
    else:
        result = ikeyboard(base_url, 
                         key1=config.get("key1", "0x87"), 
                         key2=config.get("key2", "0xB1"), 
                         duration=config.get("duration", 50))
    
    logger.info(f"BLE HTTP: Back button response: {result}")
    return result


def home(base_url: str) -> Dict[str, Any]:
    """
    Press the home button.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    config = get_device_config(base_url, "home")
    logger.info("BLE HTTP: Pressing home button")
    
    # Check if using direct endpoint or ikeyboard
    if "endpoint" in config:
        url = f"{base_url}{config['endpoint']}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
    else:
        result = ikeyboard(base_url, 
                         key1=config.get("key1", "0x87"), 
                         key2=config.get("key2", "0xB0"), 
                         duration=config.get("duration", 100))
    
    logger.info(f"BLE HTTP: Home button response: {result}")
    return result


def recent_apps(base_url: str) -> Dict[str, Any]:
    """
    Press the recent apps button.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    config = get_device_config(base_url, "recent_apps")
    logger.info("BLE HTTP: Pressing recent apps button")
    
    # Check if using direct endpoint or ikeyboard
    if "endpoint" in config:
        url = f"{base_url}{config['endpoint']}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
    else:
        result = ikeyboard(base_url, 
                         key1=config.get("key1", "0x87"), 
                         key2=config.get("key2", "0xB3"), 
                         duration=config.get("duration", 50))
    
    logger.info(f"BLE HTTP: Recent apps button response: {result}")
    return result


def open_app(base_url: str, package: str) -> Dict[str, Any]:
    """
    Open an app by package name.

    Args:
        base_url: Base URL of the BLE HTTP server.
        package: Package name of the app to open.

    Returns:
        Response from the server as a dictionary.

    Raises:
        Exception: If the app fails to open (e.g., not installed).
    """
    ensure_connected(base_url)
    url = f"{base_url}/openapp"
    params = {"package": package}
    logger.info(f"BLE HTTP: Opening app with package: {package}")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    result = response.json()
    
    # Check if the response indicates an error
    if result.get('code') != 200:
        raise Exception(f"Failed to open app: {result.get('msg', 'Unknown error')}")
    
    logger.info(f"BLE HTTP: Open app response: {result}")
    return result


def enter(base_url: str) -> Dict[str, Any]:
    """
    Press the enter key.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/enter"
    logger.info("BLE HTTP: Pressing enter key")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Enter key response: {response.json()}")
    return response.json()


def ikeyboard(base_url: str, key1: str = "0x87", key2: str = "0xB0", duration: int = 100) -> Dict[str, Any]:
    """
    ikeyboard - 自定义按钮:可实现home\back\最近任务等
    
    示例 URL: `http://192.168.2.99:9123/ikeyboard?key1=0x87&key2=0xB0&duration=100`
    
    ---------组合建-----------
    key1:
     0x87 = 触发这些安卓特殊键的功能前缀（Application 键）
    key2:
     0xB0 = Home（主页）
     0xB1 = Back（返回）
     0xB2 = Menu（菜单）
     0xB3 = Recent Apps（最近任务 / 多任务）
    ---------单键-----------
    key1:
     0x00 = 不触发特殊键的功能
    key2:
     0xB0= 回车；KEY_RETURN
     0xB2= 退格键；KEY_BACKSPACE
     0xB1= Esc键；KEY_ESC
     0xB4= 空格键；KEY_SPACE_BAR
     0xD4= KEY_DELETE

    Args:
        base_url: Base URL of the BLE HTTP server.
        key1: Prefix key (default: 0x87 for Application key).
        key2: Function key (default: 0xB0 for Home).
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/ikeyboard"
    params = {"key1": key1, "key2": key2, "duration": duration}
    logger.info(f"BLE HTTP: Sending keyboard command key1={key1}, key2={key2}, duration={duration}ms")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Keyboard command response: {response.json()}")
    return response.json()
