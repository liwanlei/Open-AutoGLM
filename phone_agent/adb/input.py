"""Input utilities for Android device text input."""

import base64
import subprocess
from typing import Optional


def start_clipper_app(device_id:str):
    """
    启动 Clipper 应用界面以确保服务运行
    """
    try:
        cmd = ['adb']
        if device_id:
            cmd.extend(['-s', device_id])
        cmd.extend(['shell', 'am', 'start', '-a', 'ca.zgrs.clipper',
                    '-n', 'ca.zgrs.clipper/.Main'])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("Clipper 应用已启动")
            return True
        else:
            print(f"启动 Clipper 应用失败: {result.stderr}")
            return False

    except Exception as e:
        print(f"启动 Clipper 应用时发生错误: {e}")
        return False

def type_text(text: str, device_id: str | None = None) -> None:
    """
    Type text into the currently focused input field using ADB Keyboard.

    Args:
        text: The text to type.
        device_id: Optional ADB device ID for multi-device setups.

    Note:
        Requires ADB Keyboard to be installed on the device.
        See: https://github.com/nicnocquee/AdbKeyboard
    """
    adb_prefix = _get_adb_prefix(device_id)
    start_clipper_app(device_id)
    subprocess.run(
        adb_prefix
        + [
            "shell",
            "am",
            "broadcast",
            "-a",
            "clipper.set",
            "-e",
            "text",
            text,
        ],
        capture_output=True,
        text=True,
    )
    subprocess.run(
        adb_prefix
        + ["shell",
           "input",
           "keyevent",
           "KEYCODE_BACK"],
        capture_output=True,
        text=True)
    subprocess.run(
        adb_prefix+["shell",
                    "input",
                    "keyevent",
                    "KEYCODE_PASTE"
                    ],
    capture_output=True,
    text=True)



def clear_text(device_id: str | None = None) -> None:
    """
    Clear text in the currently focused input field.

    Args:
        device_id: Optional ADB device ID for multi-device setups.
    """
    adb_prefix = _get_adb_prefix(device_id)

    subprocess.run(
        adb_prefix + ["shell", "am", "broadcast", "-a", "ADB_CLEAR_TEXT"],
        capture_output=True,
        text=True,
    )


def detect_and_set_adb_keyboard(device_id: str | None = None) -> str:
    """
    Detect current keyboard and switch to ADB Keyboard if needed.

    Args:
        device_id: Optional ADB device ID for multi-device setups.

    Returns:
        The original keyboard IME identifier for later restoration.
    """
    adb_prefix = _get_adb_prefix(device_id)

    # Get current IME
    result = subprocess.run(
        adb_prefix + ["shell", "settings", "get", "secure", "default_input_method"],
        capture_output=True,
        text=True,
    )
    current_ime = (result.stdout + result.stderr).strip()

    # Switch to ADB Keyboard if not already set
    if "com.android.adbkeyboard/.AdbIME" not in current_ime:
        subprocess.run(
            adb_prefix + ["shell", "ime", "set", "com.android.adbkeyboard/.AdbIME"],
            capture_output=True,
            text=True,
        )

    # Warm up the keyboard
    type_text("", device_id)

    return current_ime


def restore_keyboard(ime: str, device_id: str | None = None) -> None:
    """
    Restore the original keyboard IME.

    Args:
        ime: The IME identifier to restore.
        device_id: Optional ADB device ID for multi-device setups.
    """
    adb_prefix = _get_adb_prefix(device_id)

    subprocess.run(
        adb_prefix + ["shell", "ime", "set", ime], capture_output=True, text=True
    )


def _get_adb_prefix(device_id: str | None) -> list:
    """Get ADB command prefix with optional device specifier."""
    if device_id:
        return ["adb", "-s", device_id]
    return ["adb"]
