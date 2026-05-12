"""BLE HTTP connection management for Android devices."""

import requests
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

# Configure logger
logger = logging.getLogger(__name__)


@dataclass
class DeviceInfo:
    """Information about a connected device."""

    device_id: str
    status: str
    model: str | None = None
    android_version: str | None = None


class BLEConnection:
    """
    Manages BLE HTTP connections to Android devices.

    Example:
        >>> conn = BLEConnection("192.168.0.115:9123")
        >>> # Connect to device
        >>> conn.connect("00:11:22:33:44:55")
        >>> # Get connection state
        >>> state = conn.get_state()
        >>> # Get system info
        >>> system_info = conn.get_system_info()
        >>> # Get app list
        >>> app_list = conn.get_app_list()
    """

    def __init__(self, base_url: str):
        """
        Initialize BLE HTTP connection manager.

        Args:
            base_url: Base URL of the BLE HTTP server (e.g., "http://192.168.0.115:9123").
        """
        self.base_url = base_url.rstrip("/")
        self.connected = False
        self.system_info = None

    def connect(self, mac: Optional[str] = None) -> Dict[str, Any]:
        """
        Connect to a BLE device.

        Args:
            mac: Optional MAC address of the device to connect to.

        Returns:
            Response from the server as a dictionary.
        """
        url = f"{self.base_url}/connect"
        params = {"mac": mac} if mac else {}
        logger.info(f"BLE HTTP: Connecting to device {mac or ' (auto-detect)'}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info(f"BLE HTTP: Connect response: {response.json()}")
        self.connected = True
        return response.json()

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current connection state.

        Returns:
            Response from the server as a dictionary.
        """
        url = f"{self.base_url}/state"
        logger.info("BLE HTTP: Getting connection state")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"BLE HTTP: State response: {response.json()}")
        return response.json()

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get device system information.

        Returns:
            Response from the server as a dictionary.
        """
        if self.system_info is None:
            url = f"{self.base_url}/systeminfo"
            logger.info("BLE HTTP: Getting system information")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.system_info = response.json()
            logger.info(f"BLE HTTP: System info response: {self.system_info}")
        return self.system_info

    def get_app_list(self, system: str | None = None, search: str | None = None) -> Dict[str, Any]:
        """
        获取应用列表
        
        示例 URL: `http://192.168.0.115:9123/applist?search=微信`  (搜索应用名称或包名包含"微信"的应用)
        示例 URL: `http://192.168.0.115:9123/applist`  (默认只获取非系统应用)
        示例 URL: `http://192.168.0.115:9123/applist?system=true`  (只获取系统应用)
        示例 URL: `http://192.168.0.115:9123/applist?system=all`  (获取全部应用)
        示例 URL: `http://192.168.0.115:9123/applist?system=false&search=QQ`  (搜索非系统应用中名称或包名包含"QQ"的应用)

        Args:
            system: Filter for system apps. None for non-system apps, "true" for system apps, "all" for all apps.
            search: Search term to filter apps by name or package name.

        Returns:
            Response from the server as a dictionary.
        """
        url = f"{self.base_url}/applist"
        params = {}
        if system is not None:
            params["system"] = system
        if search is not None:
            params["search"] = search
        logger.info(f"BLE HTTP: Getting app list with system filter: {system}, search: {search}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info(f"BLE HTTP: App list response: {response.json()}")
  
        return response.json()


def connect(base_url: str, mac: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick helper to connect to a BLE device.

    Args:
        base_url: Base URL of the BLE HTTP server.
        mac: Optional MAC address of the device to connect to.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info(f"BLE HTTP: Connecting to device at {base_url} with mac {mac or 'auto'}")
    conn = BLEConnection(base_url)
    return conn.connect(mac)


def get_state(base_url: str) -> Dict[str, Any]:
    """
    Quick helper to get connection state.

    Args:
        base_url: Base URL of the BLE HTTP server.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info(f"BLE HTTP: Getting state from {base_url}")
    conn = BLEConnection(base_url)
    return conn.get_state()


def get_app_list(base_url: str, system: str | None = None, search: str | None = None) -> Dict[str, Any]:
    """
    获取应用列表
    
    示例 URL: `http://192.168.0.115:9123/applist?search=微信`  (搜索应用名称或包名包含"微信"的应用)
    示例 URL: `http://192.168.0.115:9123/applist`  (默认只获取非系统应用)
    示例 URL: `http://192.168.0.115:9123/applist?system=true`  (只获取系统应用)
    示例 URL: `http://192.168.0.115:9123/applist?system=all`  (获取全部应用)
    示例 URL: `http://192.168.0.115:9123/applist?system=false&search=QQ`  (搜索非系统应用中名称或包名包含"QQ"的应用)

    Args:
        base_url: Base URL of the BLE HTTP server.
        system: Filter for system apps. None for non-system apps, "true" for system apps, "all" for all apps.
        search: Search term to filter apps by name or package name.

    Returns:
        Response from the server as a dictionary.
    """
    logger.info(f"BLE HTTP: Getting app list from {base_url} with system filter: {system}, search: {search}")
    conn = BLEConnection(base_url)
    return conn.get_app_list(system, search)
