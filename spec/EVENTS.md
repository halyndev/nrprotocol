# NRP Events Specification

## Overview

Nodes push events. The control plane routes them. The AI reacts without polling.

## Event Format

```json
{
  "source": "nrp://farm/sensor/soil-north",
  "name": "moisture_low",
  "severity": "warning",
  "data": {
    "value": 18.5,
    "threshold": 25.0,
    "unit": "percent"
  },
  "timestamp": 1710583200.123
}
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| source | string | Yes | NRP ID of the originating node |
| name | string | Yes | Event identifier (snake_case) |
| severity | string | Yes | `debug`, `info`, `warning`, `critical`, `emergency` |
| data | object | No | Event-specific payload |
| timestamp | float | Yes | Unix timestamp with milliseconds |

## Severity Levels

| Level | Meaning | Routing |
|-------|---------|---------|
| debug | Internal diagnostics | Logged only |
| info | Normal operation events | Logged, routed to subscribers |
| warning | Needs attention soon | Logged, routed, may trigger alerts |
| critical | Immediate action needed | Logged, routed, alerts human |
| emergency | Physical safety at risk | **Bypasses all queues**. Immediate. |

## Emergency Events

Emergency events MUST:
1. Bypass all queues and buffers
2. Be processed synchronously
3. Be delivered in < 100ms
4. Trigger failsafe if no response in 1 second
5. Alert the human directly (not through the AI)

## Subscription Patterns

```
"*"                         All events from all nodes
"battery_low"               Exact event name match
"nrp://farm/*"              All events from farm scope
"temperature_*"             Wildcard on event name
"nrp://factory/robot/*"     All robot events in factory
```

## Delivery

Events are delivered via:
1. **In-process**: EventBus (async handlers)
2. **HTTP**: Server-Sent Events (SSE) at `/events`
3. **Query**: REST endpoint at `/events/query?n=50&source=...`

## Standard Events

| Event | When | Typical severity |
|-------|------|-----------------|
| `node_registered` | Node connects | info |
| `node_disconnected` | Node goes offline | warning |
| `shield_blocked` | Action blocked by safety | warning |
| `battery_low` | Battery below threshold | warning |
| `temperature_exceeded` | Temp above limit | critical |
| `emergency_stop` | E-stop triggered | emergency |
| `action_failed` | Action returned error | warning |
| `heartbeat_missed` | Node stopped responding | critical |

