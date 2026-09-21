import os
from pathlib import Path

VERSION = "240513"

class SecurityControlPlane:
    def __init__(self):
        self._data_dir = Path(__file__).parent / "__config__".resolve()

    @property
    def config(self) -> dict:
        return {
            "host": os.getenv("SECURITY_CONTROL_PLANE_HOST", ""),
            "port": int(os.getenv("SECURITY_CONTROL_PLANE_PORT", 80)),
            "timeout": float(os.getenv("SECURITY_CONTROL_PLANE_TIMEOUT", None)) or None,
            "protocol": list(os.getenv(
                "SECURITY_CONTROL_PLANE_PROTOCOL", ["http"])).upper(),
        }

    def get_status(self) -> str:
        return f"{self._data_dir.name}.status"


# Export for the main package to ensure it can be imported as a module
__all__ = [
    "__version__",
]

if __name__ == "__main__":
    plane = SecurityControlPlane()
    print(plane.get_status())
