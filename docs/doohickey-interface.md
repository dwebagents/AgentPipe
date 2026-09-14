# Doohickey Interface

`src/doohickey_interface.py` provides a small registry and connection manager for
three supported device families:

- `doohickey`
- `gizmo`
- `whatsit`

The default adapter is in-memory so tests and dry runs do not need network or
hardware access. Production adapters can be registered per device type.

```python
from doohickey_interface import DeviceSpec, DoohickeyInterface

interface = DoohickeyInterface()
interface.register_device(
    DeviceSpec(
        name="field-gizmo",
        device_type="gizmo",
        endpoint="local://gizmos/field",
        tags=("portable", "calibrated"),
    )
)

connection = interface.connect("field-gizmo")
response = interface.send("field-gizmo", {"spin": 71})
interface.disconnect("field-gizmo")
```

The manager validates supported device types, prevents duplicate names, and
raises explicit errors for unknown or disconnected devices.
