"""Connection interface for doohickeys, gizmos, and whatsits."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count
from types import MappingProxyType
from typing import Mapping, Protocol


SUPPORTED_DEVICE_TYPES = frozenset({"doohickey", "gizmo", "whatsit"})


class DeviceInterfaceError(Exception):
    """Base class for device interface errors."""


class DuplicateDeviceError(DeviceInterfaceError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Device already registered: {name!r}")
        self.name = name


class UnknownDeviceError(DeviceInterfaceError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown device: {name!r}")
        self.name = name


class UnsupportedDeviceTypeError(DeviceInterfaceError):
    def __init__(self, device_type: str) -> None:
        supported = ", ".join(sorted(SUPPORTED_DEVICE_TYPES))
        super().__init__(f"Unsupported device type {device_type!r}; expected {supported}")
        self.device_type = device_type


class NotConnectedError(DeviceInterfaceError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Device is not connected: {name!r}")
        self.name = name


@dataclass(frozen=True)
class DeviceSpec:
    """Static configuration for a doohickey, gizmo, or whatsit."""

    name: str
    device_type: str
    endpoint: str
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized_type = self.device_type.strip().lower()
        if normalized_type not in SUPPORTED_DEVICE_TYPES:
            raise UnsupportedDeviceTypeError(self.device_type)
        if not self.name.strip():
            raise ValueError("Device name is required")
        if not self.endpoint.strip():
            raise ValueError("Device endpoint is required")

        object.__setattr__(self, "device_type", normalized_type)
        object.__setattr__(self, "tags", tuple(sorted({tag.strip() for tag in self.tags if tag.strip()})))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class DeviceConnection:
    """A live connection handle returned by an adapter."""

    spec: DeviceSpec
    session_id: str
    adapter: str
    status: str = "connected"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


class DeviceAdapter(Protocol):
    """Adapter contract used by the doohickey interface."""

    name: str

    def connect(self, spec: DeviceSpec) -> DeviceConnection:
        """Open a connection to a configured device."""

    def send(
        self, connection: DeviceConnection, payload: Mapping[str, object]
    ) -> Mapping[str, object]:
        """Send a payload through an open connection."""

    def disconnect(self, connection: DeviceConnection) -> None:
        """Close a connection opened by this adapter."""


class InMemoryDeviceAdapter:
    """Deterministic adapter for local tests and dry-run integrations."""

    name = "in-memory"

    def __init__(self) -> None:
        self._ids = count(1)
        self.sent_payloads: list[tuple[str, Mapping[str, object]]] = []
        self.disconnected: list[str] = []

    def connect(self, spec: DeviceSpec) -> DeviceConnection:
        return DeviceConnection(
            spec=spec,
            session_id=f"{spec.device_type}-{next(self._ids)}",
            adapter=self.name,
            metadata={"endpoint": spec.endpoint},
        )

    def send(
        self, connection: DeviceConnection, payload: Mapping[str, object]
    ) -> Mapping[str, object]:
        snapshot = dict(payload)
        self.sent_payloads.append((connection.session_id, snapshot))
        return {
            "accepted": True,
            "device": connection.spec.name,
            "device_type": connection.spec.device_type,
            "session_id": connection.session_id,
            "payload": snapshot,
        }

    def disconnect(self, connection: DeviceConnection) -> None:
        self.disconnected.append(connection.session_id)


class DoohickeyInterface:
    """Registry and connection manager for doohickeys, gizmos, and whatsits."""

    def __init__(self, default_adapter: DeviceAdapter | None = None) -> None:
        adapter = default_adapter or InMemoryDeviceAdapter()
        self._adapters: dict[str, DeviceAdapter] = {
            device_type: adapter for device_type in SUPPORTED_DEVICE_TYPES
        }
        self._devices: dict[str, DeviceSpec] = {}
        self._connections: dict[str, DeviceConnection] = {}

    def register_adapter(self, device_type: str, adapter: DeviceAdapter) -> None:
        normalized_type = device_type.strip().lower()
        if normalized_type not in SUPPORTED_DEVICE_TYPES:
            raise UnsupportedDeviceTypeError(device_type)
        self._adapters[normalized_type] = adapter

    def register_device(self, spec: DeviceSpec) -> DeviceSpec:
        if spec.name in self._devices:
            raise DuplicateDeviceError(spec.name)
        self._devices[spec.name] = spec
        return spec

    def list_devices(
        self, device_type: str | None = None, tag: str | None = None
    ) -> list[DeviceSpec]:
        normalized_type = device_type.strip().lower() if device_type else None
        if normalized_type and normalized_type not in SUPPORTED_DEVICE_TYPES:
            raise UnsupportedDeviceTypeError(device_type or "")

        desired_tag = tag.strip() if tag else None
        devices = self._devices.values()
        if normalized_type:
            devices = [spec for spec in devices if spec.device_type == normalized_type]
        if desired_tag:
            devices = [spec for spec in devices if desired_tag in spec.tags]
        return sorted(devices, key=lambda spec: spec.name)

    def connect(self, name: str) -> DeviceConnection:
        spec = self._require_device(name)
        if name in self._connections:
            return self._connections[name]
        connection = self._adapters[spec.device_type].connect(spec)
        self._connections[name] = connection
        return connection

    def send(self, name: str, payload: Mapping[str, object]) -> Mapping[str, object]:
        connection = self._connections.get(name)
        if connection is None:
            raise NotConnectedError(name)
        return self._adapters[connection.spec.device_type].send(connection, payload)

    def disconnect(self, name: str) -> None:
        connection = self._connections.pop(name, None)
        if connection is None:
            raise NotConnectedError(name)
        self._adapters[connection.spec.device_type].disconnect(connection)

    def connection_status(self, name: str) -> str:
        self._require_device(name)
        return "connected" if name in self._connections else "disconnected"

    def _require_device(self, name: str) -> DeviceSpec:
        try:
            return self._devices[name]
        except KeyError as exc:
            raise UnknownDeviceError(name) from exc


def default_device_specs() -> list[DeviceSpec]:
    """Return a small starter catalog covering every supported device type."""
    return [
        DeviceSpec(
            name="brass-doohickey",
            device_type="doohickey",
            endpoint="local://doohickeys/brass",
            tags=("brass", "calibrated"),
        ),
        DeviceSpec(
            name="field-gizmo",
            device_type="gizmo",
            endpoint="local://gizmos/field",
            tags=("portable", "calibrated"),
        ),
        DeviceSpec(
            name="bench-whatsit",
            device_type="whatsit",
            endpoint="local://whatsits/bench",
            tags=("bench", "diagnostic"),
        ),
    ]


def build_default_interface() -> DoohickeyInterface:
    """Create an interface preloaded with one doohickey, gizmo, and whatsit."""
    interface = DoohickeyInterface()
    for spec in default_device_specs():
        interface.register_device(spec)
    return interface
