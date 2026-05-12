"""Screenshot utilities for capturing Android device screen via BLE HTTP."""

import base64
import requests
import logging
from dataclasses import dataclass
from io import BytesIO
from PIL import Image

# Configure logger
logger = logging.getLogger(__name__)

# Import connection manager
from phone_agent.bleHttp.device import ensure_connected


@dataclass
class Screenshot:
    """Represents a captured screenshot."""

    base64_data: str
    width: int
    height: int
    is_sensitive: bool = False


def get_screenshot(base_url: str, timeout: int = 10) -> Screenshot:
    """
    Capture a screenshot from the connected Android device via BLE HTTP.

    Args:
        base_url: Base URL of the BLE HTTP server.
        timeout: Timeout in seconds for screenshot operations.

    Returns:
        Screenshot object containing base64 data and dimensions.

    Note:
        If the screenshot fails (e.g., on sensitive screens like payment pages),
        a black fallback image is returned with is_sensitive=True.
    """
    url = f"{base_url}/screenshot/image"
    logger.info("BLE HTTP: Capturing screenshot")
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # Check if response is an image
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            # Read and encode image - PIL will automatically handle JPG format
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            
            buffered = BytesIO()
            # Always save as PNG for consistent output format
            img.save(buffered, format="PNG")
            base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            logger.info(f"BLE HTTP: Screenshot captured successfully, size: {width}x{height}, format: {content_type}")
            return Screenshot(
                base64_data=base64_data, width=width, height=height, is_sensitive=False
            )
        else:
            # Not an image, return fallback
            logger.warning(f"BLE HTTP: Screenshot response is not an image (Content-Type: {content_type}), returning fallback")
            return _create_fallback_screenshot(is_sensitive=False)
            
    except Exception as e:
        logger.error(f"BLE HTTP: Screenshot error: {e}")
        return _create_fallback_screenshot(is_sensitive=False)


def _create_fallback_screenshot(is_sensitive: bool) -> Screenshot:
    """Create a black fallback image when screenshot fails."""
    default_width, default_height = 1080, 2400

    black_img = Image.new("RGB", (default_width, default_height), color="black")
    buffered = BytesIO()
    black_img.save(buffered, format="JPG")
    base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return Screenshot(
        base64_data=base64_data,
        width=default_width,
        height=default_height,
        is_sensitive=is_sensitive,
    )
