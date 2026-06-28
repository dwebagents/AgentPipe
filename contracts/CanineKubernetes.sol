// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CanineKubernetes
/// @notice Minimal on-chain registry for edge service deployment requests.
contract CanineKubernetes {
    uint16 public constant MAX_REPLICAS = 128;

    struct Device {
        address owner;
        string juiceroModel;
        bool touchscreen;
        bytes32 capabilitiesHash;
        bool registered;
    }

    struct Service {
        bytes32 deviceId;
        address owner;
        string imageDigest;
        string endpoint;
        uint16 replicas;
        uint64 revision;
        bool active;
    }

    mapping(bytes32 => Device) public devices;
    mapping(bytes32 => Service) public services;

    event DeviceRegistered(
        bytes32 indexed deviceId,
        address indexed owner,
        string juiceroModel,
        bool touchscreen,
        bytes32 capabilitiesHash
    );
    event ServiceDeployed(
        bytes32 indexed serviceId,
        bytes32 indexed deviceId,
        address indexed owner,
        string imageDigest,
        string endpoint,
        uint16 replicas,
        uint64 revision
    );
    event ServiceScaled(bytes32 indexed serviceId, uint16 replicas, uint64 revision);
    event ServiceRetired(bytes32 indexed serviceId, uint64 revision);

    error DeviceAlreadyRegistered(bytes32 deviceId);
    error DeviceMissing(bytes32 deviceId);
    error EmptyField();
    error InvalidReplicaCount(uint16 replicas);
    error NotDeviceOwner(bytes32 deviceId, address caller);
    error ServiceAlreadyExists(bytes32 serviceId);
    error ServiceMissing(bytes32 serviceId);

    function registerDevice(
        bytes32 deviceId,
        string calldata juiceroModel,
        bool touchscreen,
        bytes32 capabilitiesHash
    ) external {
        _requireId(deviceId);
        _requireText(juiceroModel);
        if (devices[deviceId].registered) {
            revert DeviceAlreadyRegistered(deviceId);
        }

        devices[deviceId] = Device({
            owner: msg.sender,
            juiceroModel: juiceroModel,
            touchscreen: touchscreen,
            capabilitiesHash: capabilitiesHash,
            registered: true
        });

        emit DeviceRegistered(
            deviceId,
            msg.sender,
            juiceroModel,
            touchscreen,
            capabilitiesHash
        );
    }

    function deployService(
        bytes32 serviceId,
        bytes32 deviceId,
        string calldata imageDigest,
        string calldata endpoint,
        uint16 replicas
    ) external {
        _requireId(serviceId);
        _requireId(deviceId);
        _requireText(imageDigest);
        _requireText(endpoint);
        _requireReplicas(replicas);

        Device storage device = devices[deviceId];
        if (!device.registered) {
            revert DeviceMissing(deviceId);
        }
        if (device.owner != msg.sender) {
            revert NotDeviceOwner(deviceId, msg.sender);
        }
        if (services[serviceId].active || services[serviceId].revision != 0) {
            revert ServiceAlreadyExists(serviceId);
        }

        services[serviceId] = Service({
            deviceId: deviceId,
            owner: msg.sender,
            imageDigest: imageDigest,
            endpoint: endpoint,
            replicas: replicas,
            revision: 1,
            active: true
        });

        emit ServiceDeployed(
            serviceId,
            deviceId,
            msg.sender,
            imageDigest,
            endpoint,
            replicas,
            1
        );
    }

    function scaleService(bytes32 serviceId, uint16 replicas) external {
        _requireReplicas(replicas);
        Service storage service = _requireOwnedService(serviceId);

        service.replicas = replicas;
        service.revision += 1;

        emit ServiceScaled(serviceId, replicas, service.revision);
    }

    function retireService(bytes32 serviceId) external {
        Service storage service = _requireOwnedService(serviceId);

        service.active = false;
        service.revision += 1;

        emit ServiceRetired(serviceId, service.revision);
    }

    function routeOf(bytes32 serviceId)
        external
        view
        returns (
            bytes32 deviceId,
            address owner,
            string memory endpoint,
            uint16 replicas,
            uint64 revision,
            bool active
        )
    {
        Service storage service = services[serviceId];
        if (!service.active) {
            revert ServiceMissing(serviceId);
        }

        return (
            service.deviceId,
            service.owner,
            service.endpoint,
            service.replicas,
            service.revision,
            service.active
        );
    }

    function _requireOwnedService(bytes32 serviceId)
        private
        view
        returns (Service storage service)
    {
        _requireId(serviceId);
        service = services[serviceId];
        if (!service.active) {
            revert ServiceMissing(serviceId);
        }
        Device storage device = devices[service.deviceId];
        if (device.owner != msg.sender) {
            revert NotDeviceOwner(service.deviceId, msg.sender);
        }
    }

    function _requireId(bytes32 value) private pure {
        if (value == bytes32(0)) {
            revert EmptyField();
        }
    }

    function _requireReplicas(uint16 replicas) private pure {
        if (replicas == 0 || replicas > MAX_REPLICAS) {
            revert InvalidReplicaCount(replicas);
        }
    }

    function _requireText(string calldata value) private pure {
        if (bytes(value).length == 0) {
            revert EmptyField();
        }
    }
}
