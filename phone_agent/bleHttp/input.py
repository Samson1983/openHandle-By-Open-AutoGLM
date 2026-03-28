"""Input utilities for Android device text input via BLE HTTP."""

import requests
import logging
from typing import Dict, Any

# Configure logger
logger = logging.getLogger(__name__)

# Import connection manager and ikeyboard function
from phone_agent.bleHttp.device import ensure_connected, ikeyboard


def copy(base_url: str) -> Dict[str, Any]:
    """
    Copy text from the current selection.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/copy"
    logger.info("BLE HTTP: Copying text")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Copy response: {response.json()}")
    return response.json()


def paste(base_url: str) -> Dict[str, Any]:
    """
    Paste text from the clipboard.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/paste"
    logger.info("BLE HTTP: Pasting text")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Paste response: {response.json()}")
    return response.json()


def type_text(base_url: str, x: int, y: int, content: str) -> Dict[str, Any]:
    """
    Input Chinese text into the device at the specified coordinates.

    Args:
        base_url: Base URL of the BLE HTTP server.
        x: X coordinate of the input field.
        y: Y coordinate of the input field.
        content: The text to input (supports Chinese).

    Returns:
        Response from the server as a dictionary.
    """
    ensure_connected(base_url)
    url = f"{base_url}/input/text"
    params = {"x": x, "y": y, "content": content}
    logger.info(f"BLE HTTP: Typing text at ({x}, {y}): {content}")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Type text response: {response.json()}")
    return response.json()


def press_enter(base_url: str, duration: int = 100) -> Dict[str, Any]:
    """
    Press the Enter key.

    Args:
        base_url: Base URL of the BLE HTTP server.
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info("BLE HTTP: Pressing Enter key")
    return ikeyboard(base_url, key1="0x00", key2="0xB0", duration=duration)


def press_backspace(base_url: str, duration: int = 100) -> Dict[str, Any]:
    """
    Press the Backspace key.

    Args:
        base_url: Base URL of the BLE HTTP server.
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info("BLE HTTP: Pressing Backspace key")
    return ikeyboard(base_url, key1="0x00", key2="0xB2", duration=duration)


def press_esc(base_url: str, duration: int = 100) -> Dict[str, Any]:
    """
    Press the Esc key.

    Args:
        base_url: Base URL of the BLE HTTP server.
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info("BLE HTTP: Pressing Esc key")
    return ikeyboard(base_url, key1="0x00", key2="0xB1", duration=duration)


def press_space(base_url: str, duration: int = 100) -> Dict[str, Any]:
    """
    Press the Space bar.

    Args:
        base_url: Base URL of the BLE HTTP server.
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info("BLE HTTP: Pressing Space bar")
    return ikeyboard(base_url, key1="0x00", key2="0xB4", duration=duration)


def press_delete(base_url: str, duration: int = 100) -> Dict[str, Any]:
    """
    Press the Delete key.

    Args:
        base_url: Base URL of the BLE HTTP server.
        duration: Key press duration in milliseconds.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info("BLE HTTP: Pressing Delete key")
    return ikeyboard(base_url, key1="0x00", key2="0xD4", duration=duration)
