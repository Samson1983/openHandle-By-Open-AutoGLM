"""Device control utilities for Android automation via BLE HTTP."""

import requests
import logging
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)


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
    url = f"{base_url}/press"
    params = {"x": x, "y": y, "duration": duration}
    logger.info(f"BLE HTTP: Long pressing at ({x}, {y}) for {duration}ms")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Long press response: {response.json()}")
    return response.json()


def swipe(base_url: str, x1: int, y1: int, x2: int, y2: int, duration: int = 1000) -> Dict[str, Any]:
    """
    Swipe from start to end coordinates.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x1: Starting X coordinate.
        y1: Starting Y coordinate.
        x2: Ending X coordinate.
        y2: Ending Y coordinate.
        duration: Duration of swipe in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
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
    logger.info("BLE HTTP: Pressing back button")
    result = ikeyboard(base_url, key2="0xB1")
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
    logger.info("BLE HTTP: Pressing home button")
    result = ikeyboard(base_url, key2="0xB0")
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
    logger.info("BLE HTTP: Pressing recent apps button")
    result = ikeyboard(base_url, key2="0xB3")
    logger.info(f"BLE HTTP: Recent apps button response: {result}")
    return result


def enter(base_url: str) -> Dict[str, Any]:
    """
    Press the enter key.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    url = f"{base_url}/enter"
    logger.info("BLE HTTP: Pressing enter key")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Enter key response: {response.json()}")
    return response.json()


def ikeyboard(base_url: str, key1: str = "0x87", key2: str = "0xB0", duration: int = 100) -> Dict[str, Any]:
    """
    Send custom keyboard commands (home, back, recent apps, etc.).

    Args:
        base_url: Base URL of the BLE HTTP server.
        key1: Prefix key (default: 0x87 for Application key).
        key2: Function key (default: 0xB0 for Home).
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    url = f"{base_url}/ikeyboard"
    params = {"key1": key1, "key2": key2, "duration": duration}
    logger.info(f"BLE HTTP: Sending keyboard command key1={key1}, key2={key2}, duration={duration}ms")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Keyboard command response: {response.json()}")
    return response.json()
