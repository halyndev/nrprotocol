# NRP — Node Reach Protocol
## The universal protocol for AI-to-physical-world control.
## Version 0.1.0 — Draft
## Author: Elmadani SALKA
## License: MIT

---

## Abstract

MCP (Model Context Protocol) connects LLMs to software.
NRP (Node Reach Protocol) connects LLMs to everything else.

NRP defines a universal interface for AI systems to observe,
act upon, and safely control any physical or digital node —
from servers to robots, drones to IoT sensors, vehicles to
industrial machines.

## Design Principles

1. ONE INTERFACE FOR EVERYTHING. A server and a robot are both nodes.
2. MCP IS THE FRONT DOOR. NRP extends MCP, not replaces it.
3. DRIVER = THE ONLY CUSTOM CODE. One driver per device type (~100L).
4. SAFETY IS NOT OPTIONAL. Every node declares its limits.
5. OFFLINE-FIRST. Works without internet. LLM can be local.

## Node Interface

Every NRP node implements exactly 3 capabilities:

  OBSERVE — Read state (sensors, metrics, cameras, joints)
  ACT     — Change state (commands, movements, writes)
  SHIELD  — Declare limits (max speed, zones, emergency stop)

## Driver Interface (Python)

```python
class NRPDriver(ABC):
    @property
    @abstractmethod
    def kind(self) -> str: ...

    @abstractmethod
    async def observe(self, channels: list[str] | None = None) -> dict[str, Any]: ...

    @abstractmethod
    async def act(self, command: str, args: dict[str, Any]) -> Any: ...

    @abstractmethod
    def shield_rules(self) -> list[dict[str, Any]]: ...

    async def connect(self) -> bool: return True
    async def disconnect(self) -> None: pass
    async def heartbeat(self) -> dict[str, Any]: return await self.observe(["status"])
```

## Built-in Drivers

| Driver | Kind | Target | Lines |
|--------|------|--------|-------|
| SSHDriver | ssh | Linux/Mac/Win servers | ~100 |
| ADBDriver | adb | Android phones | ~60 |
| DockerDriver | docker | Containers | ~80 |
| BrowserDriver | browser | Chrome CDP | ~100 |
| ROS2Driver | ros2 | Any ROS2 robot | ~120 |
| UnitreeDriver | unitree | Unitree G1/H1/Go2 | ~100 |
| MQTTDriver | mqtt | IoT sensors | ~80 |
| OPCUADriver | opcua | Industrial PLCs | ~100 |
| DJIDriver | dji | DJI drones | ~100 |
| URDriver | ur | Universal Robots | ~100 |
| ModbusDriver | modbus | Industrial sensors | ~60 |

## Transport

| Transport | Use case | Latency |
|-----------|----------|---------|
| gRPC + mTLS | Default | <5ms |
| WebSocket | Firewalled | <10ms |
| MQTT | IoT/low-BW | <50ms |
| DDS | ROS2 native | <2ms |
| Local | Same machine | <1ms |

## Security — 7 Layers

1. mTLS between control plane and every node
2. RBAC per user x node x command
3. Shield enforcement at node level (cannot bypass)
4. Audit trail hash-chained, append-only
5. Rate limiting per node
6. Confirmation for irreversible commands
7. Emergency stop always bypasses all queues

## Compatibility

- MCP: Control plane IS an MCP server. Claude sees robots as tools.
- ROS2: Driver wraps ROS2 topics/services. No replacement needed.
- OpenClaw: NRP is a skill. openclaw install nrp-bridge.
- Home Assistant, Kubernetes, MQTT: all via drivers.

## Architecture

```
  LLM (any)
    |
    | MCP
    v
  CONTROL PLANE (router, policy, audit, memory)
    |        |        |        |
    | NRP    | NRP    | NRP    | NRP
    v        v        v        v
  server   robot    drone    sensor
  (ssh)    (ros2)   (dji)    (mqtt)
```

