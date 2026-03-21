"""Device factory for selecting ADB or HDC based on device type."""

import logging
from enum import Enum
from typing import Any


class DeviceType(Enum):
    """Type of device connection tool."""

    ADB = "adb"
    HDC = "hdc"
    IOS = "ios"
    BLE_HTTP = "blehttp"


class DeviceFactory:
    """
    Factory class for getting device-specific implementations.

    This allows the system to work with both Android (ADB) and HarmonyOS (HDC) devices.
    """

    def __init__(self, device_type: DeviceType = DeviceType.ADB, blehttp_url: str = "http://192.168.0.115:9123"):
        """
        Initialize the device factory.

        Args:
            device_type: The type of device to use (ADB, HDC, or BLE_HTTP).
            blehttp_url: The BLE HTTP server URL (only used for BLE_HTTP device type).
        """
        self.device_type = device_type
        self.blehttp_url = blehttp_url
        self._module = None

    @property
    def module(self):
        """Get the appropriate device module (adb, hdc, or blehttp)."""
        if self._module is None:
            if self.device_type == DeviceType.ADB:
                from phone_agent import adb

                self._module = adb
            elif self.device_type == DeviceType.HDC:
                from phone_agent import hdc

                self._module = hdc
            elif self.device_type == DeviceType.BLE_HTTP:
                from phone_agent import bleHttp

                self._module = bleHttp
            else:
                raise ValueError(f"Unknown device type: {self.device_type}")
        return self._module

    def get_screenshot(self, device_id: str | None = None, timeout: int = 10):
        """Get screenshot from device."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.get_screenshot(self.blehttp_url, timeout)
        return self.module.get_screenshot(device_id, timeout)

    def get_current_app(self, device_id: str | None = None) -> str:
        """Get current app name."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't support get_current_app
            return "Unknown"
        return self.module.get_current_app(device_id)

    def tap(
        self, x: int, y: int, device_id: str | None = None, delay: float | None = None
    ):
        """Tap at coordinates."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.tap(self.blehttp_url, x, y)
        return self.module.tap(x, y, device_id, delay)

    def double_tap(
        self, x: int, y: int, device_id: str | None = None, delay: float | None = None
    ):
        """Double tap at coordinates."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't support double_tap, use tap twice
            self.module.tap(self.blehttp_url, x, y)
            import time
            time.sleep(0.1)
            return self.module.tap(self.blehttp_url, x, y)
        return self.module.double_tap(x, y, device_id, delay)

    def long_press(
        self,
        x: int,
        y: int,
        duration_ms: int = 3000,
        device_id: str | None = None,
        delay: float | None = None,
    ):
        """Long press at coordinates."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.long_press(self.blehttp_url, x, y, duration_ms)
        return self.module.long_press(x, y, duration_ms, device_id, delay)

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int | None = None,
        device_id: str | None = None,
        delay: float | None = None,
    ):
        """Swipe from start to end."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.swipe(self.blehttp_url, start_x, start_y, end_x, end_y, duration_ms or 1000)
        return self.module.swipe(
            start_x, start_y, end_x, end_y, duration_ms, device_id, delay
        )

    def back(self, device_id: str | None = None, delay: float | None = None):
        """Press back button."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.back(self.blehttp_url)
        return self.module.back(device_id, delay)

    def home(self, device_id: str | None = None, delay: float | None = None):
        """Press home button."""
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.home(self.blehttp_url)
        return self.module.home(device_id, delay)

    def launch_app(
        self, app_name: str, device_id: str | None = None, delay: float | None = None
    ) -> bool:
        """Launch an app."""
        if self.device_type == DeviceType.BLE_HTTP:
            import time
            logger = logging.getLogger(__name__)
            logger.info(f"BLE HTTP: Launching app '{app_name}'")
            
            # Get app package from APP_PACKAGES
            from phone_agent.config.apps import APP_PACKAGES
            if app_name in APP_PACKAGES:
                package = APP_PACKAGES[app_name]
                try:
                    self.module.open_app(self.blehttp_url, package)
                    logger.info(f"BLE HTTP: App '{app_name}' launched successfully")
                    time.sleep(1.0)  # Wait for app to load
                    return True
                except Exception as e:
                    logger.error(f"BLE HTTP: Failed to launch app '{app_name}': {e}")
                    return False
            else:
                logger.error(f"BLE HTTP: App '{app_name}' not found in APP_PACKAGES")
                return False
        return self.module.launch_app(app_name, device_id, delay)

    def type_text(self, text: str, device_id: str | None = None):
        """Type text."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP requires coordinates for text input
            # For simplicity, we'll use a default position
            return self.module.type_text(self.blehttp_url, 500, 1000, text)
        return self.module.type_text(text, device_id)

    def clear_text(self, device_id: str | None = None):
        """Clear text."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't support clear_text
            return
        return self.module.clear_text(device_id)

    def detect_and_set_adb_keyboard(self, device_id: str | None = None) -> str:
        """Detect and set keyboard."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't use ADB keyboard
            return ""
        return self.module.detect_and_set_adb_keyboard(device_id)

    def restore_keyboard(self, ime: str, device_id: str | None = None):
        """Restore keyboard."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't use ADB keyboard
            return
        return self.module.restore_keyboard(ime, device_id)

    def list_devices(self):
        """List connected devices."""
        if self.device_type == DeviceType.BLE_HTTP:
            # BLE HTTP doesn't support listing devices
            return []
        return self.module.list_devices()

    def get_app_list(self, device_id: str | None = None, system: str | None = None):
        """Get list of installed applications.
        
        Args:
            device_id: Optional device ID.
            system: Filter for system apps. None for non-system apps, "true" for system apps, "all" for all apps.
        """
        if self.device_type == DeviceType.BLE_HTTP:
            return self.module.get_app_list(self.blehttp_url, system)
        # For ADB and other device types, return empty list for now
        # In the future, we could implement this for other device types
        return []

    def get_connection_class(self):
        """Get the connection class (ADBConnection, HDCConnection, or BLEConnection)."""
        if self.device_type == DeviceType.ADB:
            from phone_agent.adb import ADBConnection

            return ADBConnection
        elif self.device_type == DeviceType.HDC:
            from phone_agent.hdc import HDCConnection

            return HDCConnection
        elif self.device_type == DeviceType.BLE_HTTP:
            from phone_agent.bleHttp import BLEConnection

            return BLEConnection
        else:
            raise ValueError(f"Unknown device type: {self.device_type}")


# Global device factory instance
_device_factory: DeviceFactory | None = None


def set_device_type(device_type: DeviceType, blehttp_url: str = "http://192.168.0.115:9123"):
    """
    Set the global device type.

    Args:
        device_type: The device type to use (ADB, HDC, or BLE_HTTP).
        blehttp_url: The BLE HTTP server URL (only used for BLE_HTTP device type).
    """
    global _device_factory
    _device_factory = DeviceFactory(device_type, blehttp_url)


def get_device_factory() -> DeviceFactory:
    """
    Get the global device factory instance.

    Returns:
        The device factory instance.
    """
    global _device_factory
    if _device_factory is None:
        _device_factory = DeviceFactory(DeviceType.ADB)  # Default to ADB
    return _device_factory
