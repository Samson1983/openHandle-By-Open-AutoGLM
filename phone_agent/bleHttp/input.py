"""Input utilities for Android device text input via BLE HTTP."""

import requests
import logging
from typing import Dict, Any

# Configure logger
logger = logging.getLogger(__name__)


def copy(base_url: str) -> Dict[str, Any]:
    """
    Copy text from the current selection.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
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
    url = f"{base_url}/input/text"
    params = {"x": x, "y": y, "content": content}
    logger.info(f"BLE HTTP: Typing text at ({x}, {y}): {content}")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    logger.info(f"BLE HTTP: Type text response: {response.json()}")
    return response.json()
