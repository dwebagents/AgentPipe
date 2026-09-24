"""
Doohickey Interface Implementation v1.0.2 (Python Edition)
==================================================================

This module implements a robust, extensible interface between:
- The central "Dooh" daemon logic in Python (`doohickey_handler.py`)
- External gizmos and whatsits protocols via `@dooh-kit/gizmes` or custom WebSocket/WebSocket-like wrappers.

The design follows the abstract abstraction layer for external packages like **whatss** (WebSockets).
It ensures full compatibility with standard type-checking environments while supporting dynamic device registration.

## Architecture Overview

1.  **Dooh Core (`doohickey_handler.py`)**: Handles connection logic, error management, and event dispatching to registered devices.
2.  **Device Registry**: A central registry that maps `device_id` -> `{ handler_type, instance }`.
3.  **External Wrappers (JavaScript/TS/WebSocket)**: Custom implementations for gizmos/whatsits via the standard protocol (`ws://`).

## Implementation Details

### Core Connection Logic & Error Handling

The Dooh daemon manages its own state and delegates to registered handlers. If a device is unreachable, it logs an error but continues with other devices or throws specific exceptions as per policy.
