"""Reference control plane for Kubernetes-for-canines on an EVM chain.

The Solidity contract is the settlement layer. This Python module mirrors the
domain rules in a form that can be tested without a local Solidity toolchain.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
from typing import Iterable


MAX_REPLICAS = 128


class CanineKubernetesError(Exception):
    """Base class for control-plane errors."""


class DuplicateDeviceError(CanineKubernetesError):
    """Raised when a device is registered twice."""


class DuplicateServiceError(CanineKubernetesError):
    """Raised when a service id is reused for a different deployment."""


class InvalidDeploymentError(CanineKubernetesError):
    """Raised when a service deployment is malformed."""


class NotDeviceOwnerError(CanineKubernetesError):
    """Raised when a caller is not authorized for the target device."""


class UnknownDeviceError(CanineKubernetesError):
    """Raised when a device id is unknown."""


class UnknownServiceError(CanineKubernetesError):
    """Raised when a service id is unknown or inactive."""


def normalize_address(address: str) -> str:
    """Normalize and validate an EVM address."""
    if not isinstance(address, str) or not address.startswith("0x"):
        raise InvalidDeploymentError(f"invalid EVM address: {address!r}")
    body = address[2:]
    if len(body) != 40:
        raise InvalidDeploymentError(f"invalid EVM address: {address!r}")
    try:
        int(body, 16)
    except ValueError as exc:
        raise InvalidDeploymentError(f"invalid EVM address: {address!r}") from exc
    return "0x" + body.lower()


def stable_bytes32(*parts: object) -> str:
    """Return a Solidity-friendly bytes32 hex digest for deterministic ids."""
    encoded = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return "0x" + sha256(encoded).hexdigest()


def _clean_id(value: str, kind: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidDeploymentError(f"{kind} must be a non-empty string")
    return value.strip()


def _validate_replicas(replicas: int) -> int:
    if not isinstance(replicas, int) or replicas < 1 or replicas > MAX_REPLICAS:
        raise InvalidDeploymentError(
            f"replicas must be between 1 and {MAX_REPLICAS}, got {replicas!r}"
        )
    return replicas


@dataclass(frozen=True)
class DeviceRegistration:
    """A deployable edge device controlled by one EVM account."""

    device_id: str
    owner: str
    juicero_model: str
    touchscreen: bool
    capabilities: tuple[str, ...]

    @property
    def capabilities_hash(self) -> str:
        return stable_bytes32(*sorted(self.capabilities))

    @property
    def input_mode(self) -> str:
        return "touchscreen" if self.touchscreen else "headless-juice-button"


@dataclass(frozen=True)
class ServiceDeployment:
    """A service bound to one registered device."""

    service_id: str
    device_id: str
    owner: str
    image_digest: str
    endpoint: str
    replicas: int
    revision: int = 1
    active: bool = True

    @property
    def deployment_hash(self) -> str:
        return stable_bytes32(
            self.service_id,
            self.device_id,
            self.owner,
            self.image_digest,
            self.endpoint,
            self.replicas,
            self.revision,
            self.active,
        )

    def routes(self) -> tuple[str, ...]:
        base = self.endpoint.rstrip("/")
        return tuple(f"{base}/replicas/{index}" for index in range(self.replicas))


class CanineKubernetesControlPlane:
    """In-memory reference implementation of the on-chain registry rules."""

    def __init__(self, max_replicas: int = MAX_REPLICAS) -> None:
        self.max_replicas = max_replicas
        self._devices: dict[str, DeviceRegistration] = {}
        self._services: dict[str, ServiceDeployment] = {}

    def register_device(
        self,
        device_id: str,
        owner: str,
        *,
        juicero_model: str = "J1-C",
        touchscreen: bool = False,
        capabilities: Iterable[str] = (),
    ) -> DeviceRegistration:
        device_key = _clean_id(device_id, "device_id")
        if device_key in self._devices:
            raise DuplicateDeviceError(device_key)
        device = DeviceRegistration(
            device_id=device_key,
            owner=normalize_address(owner),
            juicero_model=_clean_id(juicero_model, "juicero_model"),
            touchscreen=bool(touchscreen),
            capabilities=tuple(
                sorted(_clean_id(cap, "capability") for cap in capabilities)
            ),
        )
        self._devices[device_key] = device
        return device

    def deploy_service(
        self,
        service_id: str,
        device_id: str,
        *,
        image_digest: str,
        endpoint: str,
        replicas: int,
        caller: str,
    ) -> ServiceDeployment:
        service_key = _clean_id(service_id, "service_id")
        if service_key in self._services:
            raise DuplicateServiceError(service_key)
        device = self._require_device(device_id)
        caller_address = normalize_address(caller)
        if caller_address != device.owner:
            raise NotDeviceOwnerError(service_key)
        deployment = ServiceDeployment(
            service_id=service_key,
            device_id=device.device_id,
            owner=device.owner,
            image_digest=self._validate_image_digest(image_digest),
            endpoint=_clean_id(endpoint, "endpoint"),
            replicas=self._validate_replica_count(replicas),
        )
        self._services[service_key] = deployment
        return deployment

    def scale_service(
        self, service_id: str, replicas: int, *, caller: str
    ) -> ServiceDeployment:
        deployment = self._require_service(service_id)
        caller_address = normalize_address(caller)
        if caller_address != deployment.owner:
            raise NotDeviceOwnerError(service_id)
        updated = replace(
            deployment,
            replicas=self._validate_replica_count(replicas),
            revision=deployment.revision + 1,
        )
        self._services[deployment.service_id] = updated
        return updated

    def retire_service(self, service_id: str, *, caller: str) -> ServiceDeployment:
        deployment = self._require_service(service_id)
        caller_address = normalize_address(caller)
        if caller_address != deployment.owner:
            raise NotDeviceOwnerError(service_id)
        retired = replace(deployment, active=False, revision=deployment.revision + 1)
        self._services[deployment.service_id] = retired
        return retired

    def routes_for(self, service_id: str) -> tuple[str, ...]:
        return self._require_service(service_id).routes()

    def dispatch_manifest(self, service_id: str) -> dict[str, object]:
        deployment = self._require_service(service_id)
        device = self._require_device(deployment.device_id)
        return {
            "service_id": deployment.service_id,
            "device_id": device.device_id,
            "image_digest": deployment.image_digest,
            "replicas": deployment.replicas,
            "routes": deployment.routes(),
            "device_input_mode": device.input_mode,
            "capabilities_hash": device.capabilities_hash,
            "deployment_hash": deployment.deployment_hash,
        }

    def _require_device(self, device_id: str) -> DeviceRegistration:
        device_key = _clean_id(device_id, "device_id")
        try:
            return self._devices[device_key]
        except KeyError as exc:
            raise UnknownDeviceError(device_key) from exc

    def _require_service(self, service_id: str) -> ServiceDeployment:
        service_key = _clean_id(service_id, "service_id")
        try:
            deployment = self._services[service_key]
        except KeyError as exc:
            raise UnknownServiceError(service_key) from exc
        if not deployment.active:
            raise UnknownServiceError(service_key)
        return deployment

    def _validate_replica_count(self, replicas: int) -> int:
        if self.max_replicas != MAX_REPLICAS:
            if (
                not isinstance(replicas, int)
                or replicas < 1
                or replicas > self.max_replicas
            ):
                raise InvalidDeploymentError(
                    "replicas must be between "
                    f"1 and {self.max_replicas}, got {replicas!r}"
                )
            return replicas
        return _validate_replicas(replicas)

    @staticmethod
    def _validate_image_digest(image_digest: str) -> str:
        digest = _clean_id(image_digest, "image_digest")
        if not (
            digest.startswith("sha256:")
            or digest.startswith("ipfs://")
            or digest.startswith("bafy")
        ):
            raise InvalidDeploymentError(
                "image_digest must be sha256:, ipfs://, or bafy-prefixed content"
            )
        return digest


__all__ = [
    "CanineKubernetesControlPlane",
    "CanineKubernetesError",
    "DeviceRegistration",
    "DuplicateDeviceError",
    "DuplicateServiceError",
    "InvalidDeploymentError",
    "MAX_REPLICAS",
    "NotDeviceOwnerError",
    "ServiceDeployment",
    "UnknownDeviceError",
    "UnknownServiceError",
    "normalize_address",
    "stable_bytes32",
]
