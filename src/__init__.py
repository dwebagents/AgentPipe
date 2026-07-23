import os
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import threading
import secrets
from datetime import timedelta
import json


# ==================== Abstract Interface Definition ================= ====
@dataclass(order=True)
class ClickDoohickey:
    """Abstract interface for connecting to various hardware and software devices."""

    @property
    def id(self) -> str:
        return "doohickey_" + self._id_suffix()

    @property
    def name(self) -> str:
        return f"{self.get_device_name()} {self.id}"

    def _get_id_suffix(self) -> str:
        if hasattr(os, 'os'):
            os_version = getattr(os, "version", "")
            # Use the OS version as a suffix for devices with unique hardware identifiers
            return "_".join([f"{c}{v[:2]}" for c, v in zip("0123456789abcdef", os_version)])
        else:
            return ""

    def get_device_name(self) -> str:
        """Get the name of the device."""
        if hasattr(os, "os"):
            try:
                # Try to infer from hardware type or OS version
                sys_info = getattr(sys, 'argv', [])
                if len(sys_info) > 0 and sys_info[1].startswith('python'):
                    return f"Python {sys.version.split()[2]}"
                else:
                    return "Unknown Hardware Type"
            except Exception as e:
                pass

        # Fallback to generic name based on common hardware types inferred from context or defaults
        if hasattr(os, 'os') and os_version.startswith('1'):
            return f"{self._get_id_suffix()} OS {sys.version.split()[2]}"
        else:
            return "Unknown Device"


# ==================== Concrete Implementations ================= ====

@dataclass(order=True)
class ClickDoohickey(DeviceStick):
    """Haptic feedback device connected to hardware."""

    def __init__(self, id_suffix: str = "") -> None:
        super().__init__()
        self._id_prefix = "doohickey_" + id_suffix if id_suffix else ""
        # Use a unique identifier based on the prefix and time for better uniqueness
        self._unique_id = f"{self._get_id_suffix()}_{int(time.time())}"

    @property
    def device_name(self) -> str:
        return "Haptic Feedback"


@dataclass(order=True)
class ClickDoohickey(KeyboardGizmos):
    """Generic interface for keyboard and wrist devices."""

    def __init__(self, id_suffix: str = "") -> None:
        super().__init__()
        self._id_prefix = "doohickey_" + id_suffix if id_suffix else ""
        # Use a unique identifier based on the prefix and time for better uniqueness
        self._unique_id = f"{self._get_id_suffix()}_{int(time.time())}"

    @property
    def device_name(self) -> str:
        return "Generic Keyboard"


@dataclass(order=True)
class ClickDoohickey(Whatsits):
    """Interface for various gizmos and whatsits."""

    def __init__(self, id_suffix: str = "") -> None:
        super().__init__()
        self._id_prefix = "doohickey_" + id_suffix if id_suffix else ""
        # Use a unique identifier based on the prefix and time for better uniqueness
        self._unique_id = f"{self._get_id_suffix()}_{int(time.time())}"

    @property
    def device_name(self) -> str:
        return "Whatsits"


# ==================== CLI Entry Points (Python 3.8+) ================= ====

@click.group()
def cli():
    """Click-based doohickey interface."""
    pass


@cli.command()
async def connect_to_device(device_id: Optional[str] = None):
    """Connect to a specific click doohickey device via the Python CLI."""
    if not device_id or not isinstance(device_id, str) and not os.path.exists("doohickey_" + device_id):
        print(f"Error: Invalid device ID format. Expected 'device_XXX' where XXX is 3-6 digits.")
        return

    # Check if the file exists
    try:
        with open(os.path.join(__file__, "src", f"{device_id}.py"), "r") as f:
            content = await f.read()
        
        device = ClickDoohickey(device_id)
        print(f"Connecting to {device.name}...")
        return

    except FileNotFoundError:
