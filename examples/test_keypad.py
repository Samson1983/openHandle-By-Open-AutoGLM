"""Test tool for Redmi Truo3 Android 16 keypad interfaces."""

import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RedmiTruo3KeypadTester:
    """Test utility for Redmi Truo3 Android 16 keypad interfaces."""

    def __init__(self, base_url: str = "http://192.168.2.152:9123"):
        """
        Initialize the keypad tester.

        Args:
            base_url: Base URL of the BLE HTTP server.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def press_home(self, duration: int = 100) -> bool:
        """
        Press the home button.

        Args:
            duration: Key press duration in milliseconds.

        Returns:
            True if the request was successful, False otherwise.
        """
        url = f"{self.base_url}/ikeyboard"
        params = {"key1": "0x87", "key2": "0xB0", "duration": duration}
        logger.info(f"Pressing home button with duration {duration}ms")
        return self._send_request(url, params)

    def press_back(self, duration: int = 50) -> bool:
        """
        Press the back button.

        Args:
            duration: Key press duration in milliseconds.

        Returns:
            True if the request was successful, False otherwise.
        """
        url = f"{self.base_url}/ikeyboard"
        params = {"key1": "0x87", "key2": "0xB1", "duration": duration}
        logger.info(f"Pressing back button with duration {duration}ms")
        return self._send_request(url, params)

    def press_recent_apps(self, duration: int = 50) -> bool:
        """
        Press the recent apps button.

        Args:
            duration: Key press duration in milliseconds.

        Returns:
            True if the request was successful, False otherwise.
        """
        url = f"{self.base_url}/ikeyboard"
        params = {"key1": "0x87", "key2": "0xB3", "duration": duration}
        logger.info(f"Pressing recent apps button with duration {duration}ms")
        return self._send_request(url, params)

    def _send_request(self, url: str, params: dict) -> bool:
        """
        Send HTTP request to the keypad interface.

        Args:
            url: The URL to send the request to.
            params: The parameters to include in the request.

        Returns:
            True if the request was successful, False otherwise.
        """
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"Request successful: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return False

    def test_all_buttons(self):
        """
        Test all keypad buttons sequentially.
        """
        logger.info("Testing all keypad buttons...")
        
        logger.info("\n1. Testing home button:")
        home_success = self.press_home()
        
        # Wait a bit between tests
        import time
        time.sleep(1)
        
        logger.info("\n2. Testing back button:")
        back_success = self.press_back()
        
        time.sleep(1)
        
        logger.info("\n3. Testing recent apps button:")
        recent_success = self.press_recent_apps()
        
        logger.info("\nTest results:")
        logger.info(f"Home button: {'✅ Success' if home_success else '❌ Failed'}")
        logger.info(f"Back button: {'✅ Success' if back_success else '❌ Failed'}")
        logger.info(f"Recent apps button: {'✅ Success' if recent_success else '❌ Failed'}")


if __name__ == "__main__":
    # Create tester instance
    tester = RedmiTruo3KeypadTester()
    
    # Test all buttons
    tester.test_all_buttons()
