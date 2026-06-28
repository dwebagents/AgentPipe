from pathlib import Path

import pytest

from canine_kubernetes import (
    CanineKubernetesControlPlane,
    DuplicateDeviceError,
    DuplicateServiceError,
    InvalidDeploymentError,
    NotDeviceOwnerError,
    UnknownDeviceError,
    UnknownServiceError,
    normalize_address,
)


OWNER = "0x1234567890ABCDEF1234567890abcdef12345678"
OTHER = "0x9999999999999999999999999999999999999999"


def _plane_with_device() -> CanineKubernetesControlPlane:
    plane = CanineKubernetesControlPlane()
    plane.register_device(
        "fido-j1c",
        OWNER,
        juicero_model="J1-C",
        touchscreen=False,
        capabilities=("fog-compute", "service-routing", "juice-button"),
    )
    return plane


def test_register_device_normalizes_owner_and_headless_capabilities():
    plane = _plane_with_device()
    manifest = plane.deploy_service(
        "walkies-api",
        "fido-j1c",
        image_digest="sha256:" + "a" * 64,
        endpoint="https://edge.example/fido",
        replicas=2,
        caller=OWNER,
    )

    dispatch = plane.dispatch_manifest(manifest.service_id)
    assert manifest.owner == normalize_address(OWNER)
    assert dispatch["device_input_mode"] == "headless-juice-button"
    assert dispatch["replicas"] == 2
    assert len(dispatch["routes"]) == 2
    assert str(dispatch["capabilities_hash"]).startswith("0x")


def test_device_registration_is_unique():
    plane = _plane_with_device()

    with pytest.raises(DuplicateDeviceError):
        plane.register_device("fido-j1c", OWNER)


def test_deploy_requires_known_device_and_owner():
    plane = _plane_with_device()

    with pytest.raises(UnknownDeviceError):
        plane.deploy_service(
            "missing-device",
            "ghost-device",
            image_digest="ipfs://bafybeigdyrzt",
            endpoint="https://edge.example/missing",
            replicas=1,
            caller=OWNER,
        )

    with pytest.raises(NotDeviceOwnerError):
        plane.deploy_service(
            "wrong-owner",
            "fido-j1c",
            image_digest="ipfs://bafybeigdyrzt",
            endpoint="https://edge.example/wrong",
            replicas=1,
            caller=OTHER,
        )


def test_deploy_validates_image_digest_replicas_and_unique_service_id():
    plane = _plane_with_device()

    with pytest.raises(InvalidDeploymentError):
        plane.deploy_service(
            "bad-image",
            "fido-j1c",
            image_digest="latest",
            endpoint="https://edge.example/bad",
            replicas=1,
            caller=OWNER,
        )

    with pytest.raises(InvalidDeploymentError):
        plane.deploy_service(
            "bad-replicas",
            "fido-j1c",
            image_digest="sha256:" + "b" * 64,
            endpoint="https://edge.example/bad",
            replicas=0,
            caller=OWNER,
        )

    plane.deploy_service(
        "unique-service",
        "fido-j1c",
        image_digest="sha256:" + "c" * 64,
        endpoint="https://edge.example/unique",
        replicas=1,
        caller=OWNER,
    )

    with pytest.raises(DuplicateServiceError):
        plane.deploy_service(
            "unique-service",
            "fido-j1c",
            image_digest="sha256:" + "d" * 64,
            endpoint="https://edge.example/duplicate",
            replicas=1,
            caller=OWNER,
        )


def test_scale_updates_revision_routes_and_deployment_hash():
    plane = _plane_with_device()
    deployment = plane.deploy_service(
        "fempto-service",
        "fido-j1c",
        image_digest="bafybeigdyrzt4example",
        endpoint="juicero://fido/service",
        replicas=2,
        caller=OWNER,
    )
    original_hash = deployment.deployment_hash

    scaled = plane.scale_service("fempto-service", 5, caller=OWNER)

    assert scaled.revision == 2
    assert scaled.replicas == 5
    assert scaled.deployment_hash != original_hash
    assert plane.routes_for("fempto-service") == tuple(
        f"juicero://fido/service/replicas/{index}" for index in range(5)
    )


def test_retire_service_blocks_future_routes():
    plane = _plane_with_device()
    plane.deploy_service(
        "retire-me",
        "fido-j1c",
        image_digest="ipfs://bafybeigdyrzt-retire",
        endpoint="https://edge.example/retire",
        replicas=1,
        caller=OWNER,
    )

    retired = plane.retire_service("retire-me", caller=OWNER)

    assert retired.active is False
    assert retired.revision == 2
    with pytest.raises(UnknownServiceError):
        plane.routes_for("retire-me")


def test_solidity_contract_exposes_expected_registry_surface():
    contract = Path("contracts/CanineKubernetes.sol").read_text()

    for required in [
        "contract CanineKubernetes",
        "MAX_REPLICAS",
        "mapping(bytes32 => Device) public devices",
        "mapping(bytes32 => Service) public services",
        "event DeviceRegistered",
        "event ServiceDeployed",
        "event ServiceScaled",
        "event ServiceRetired",
        "error NotDeviceOwner",
        "function registerDevice",
        "function deployService",
        "function scaleService",
        "function retireService",
        "function routeOf",
    ]:
        assert required in contract
