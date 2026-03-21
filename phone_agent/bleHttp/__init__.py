"""BLE HTTP utilities for Android device interaction."""

from phone_agent.bleHttp.connection import (
    BLEConnection,
    DeviceInfo,
    connect,
    get_state,
    get_app_list,
)
from phone_agent.bleHttp.device import (
    back,
    home,
    long_press,
    recent_apps,
    swipe,
    tap,
    open_app,
)
from phone_agent.bleHttp.input import (
    copy,
    paste,
    type_text,
)
from phone_agent.bleHttp.screenshot import get_screenshot

__all__ = [
    # Connection
    "BLEConnection",
    "DeviceInfo",
    "connect",
    "get_state",
    "get_app_list",
    # Device control
    "tap",
    "swipe",
    "long_press",
    "back",
    "home",
    "recent_apps",
    "open_app",
    # Input
    "type_text",
    "copy",
    "paste",
    # Screenshot
    "get_screenshot",
]