"""Tests for the doohickey, gizmo, and whatsit interface."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from doohickey_interface import (
    DeviceConnection,
    DeviceSpec,
    DoohickeyInterface,
    DuplicateDeviceError,
    InMemoryDeviceAdapter,
    NotConnectedError,
    UnknownDeviceError,
    UnsupportedDeviceTypeError,
    build_default_interface,
)


class RecordingAdapter:
    name = "recording"

    def __init__(self) -> None:
        self.connected: list[str] = []
        self.disconnected: list[str] = []
        self.payloads: list[dict[str, object]] = []

    def connect(self, spec: DeviceSpec) -> DeviceConnection:
        self.connected.append(spec.name)
        return DeviceConnection(spec=spec, session_id=f"session:{spec.name}", adapter=self.name)

    def send(self, connection: DeviceConnection, payload: dict[str, object]) -> dict[str, object]:
        snapshot = dict(payload)
        self.payloads.append(snapshot)
        return {"device": connection.spec.name, "payload": snapshot}

    def disconnect(self, connection: DeviceConnection) -> None:
        self.disconnected.append(connection.spec.name)


class DoohickeyInterfaceTests(unittest.TestCase):
    def test_default_catalog_covers_all_supported_device_types(self) -> None:
        interface = build_default_interface()

        self.assertEqual(
            [spec.device_type for spec in interface.list_devices()],
            ["whatsit", "doohickey", "gizmo"],
        )
        self.assertEqual(
            [spec.name for spec in interface.list_devices(tag="calibrated")],
            ["brass-doohickey", "field-gizmo"],
        )

    def test_rejects_unknown_device_type(self) -> None:
        with self.assertRaises(UnsupportedDeviceTypeError):
            DeviceSpec(name="bad-widget", device_type="widget", endpoint="local://bad")

    def test_rejects_duplicate_device_names(self) -> None:
        interface = DoohickeyInterface()
        spec = DeviceSpec("brass-doohickey", "doohickey", "local://brass")

        interface.register_device(spec)

        with self.assertRaises(DuplicateDeviceError):
            interface.register_device(spec)

    def test_connects_sends_and_disconnects_through_registered_adapter(self) -> None:
        adapter = RecordingAdapter()
        interface = DoohickeyInterface()
        interface.register_adapter("gizmo", adapter)
        interface.register_device(DeviceSpec("field-gizmo", "gizmo", "local://field"))

        connection = interface.connect("field-gizmo")
        response = interface.send("field-gizmo", {"spin": 71})
        interface.disconnect("field-gizmo")

        self.assertEqual(connection.session_id, "session:field-gizmo")
        self.assertEqual(response, {"device": "field-gizmo", "payload": {"spin": 71}})
        self.assertEqual(adapter.connected, ["field-gizmo"])
        self.assertEqual(adapter.payloads, [{"spin": 71}])
        self.assertEqual(adapter.disconnected, ["field-gizmo"])
        self.assertEqual(interface.connection_status("field-gizmo"), "disconnected")

    def test_default_adapter_echoes_payload_for_all_device_types(self) -> None:
        adapter = InMemoryDeviceAdapter()
        interface = DoohickeyInterface(default_adapter=adapter)
        for spec in [
            DeviceSpec("d", "doohickey", "local://d"),
            DeviceSpec("g", "gizmo", "local://g"),
            DeviceSpec("w", "whatsit", "local://w"),
        ]:
            interface.register_device(spec)

        for name in ("d", "g", "w"):
            connection = interface.connect(name)
            response = interface.send(name, {"ping": name})
            self.assertEqual(response["accepted"], True)
            self.assertEqual(response["session_id"], connection.session_id)

    def test_send_requires_connection_and_known_device(self) -> None:
        interface = DoohickeyInterface()
        interface.register_device(DeviceSpec("bench-whatsit", "whatsit", "local://bench"))

        with self.assertRaises(NotConnectedError):
            interface.send("bench-whatsit", {"ping": True})
        with self.assertRaises(UnknownDeviceError):
            interface.connect("missing")


if __name__ == "__main__":
    unittest.main()
