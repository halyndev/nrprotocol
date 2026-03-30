# NRP Manifest Specification

## Overview

When a node connects, it declares EVERYTHING it can do.
The AI reads the manifest and knows instantly how to interact.
Zero configuration. Zero documentation reading. Plug and play.

## Format (JSON)

```json
{
  "nrp_id": "nrp://factory-3/robot/arm-7",
  "manufacturer": "Unitree",
  "model": "G1",
  "firmware": "2.4.1",
  "observe": [
    {
      "name": "joint_positions",
      "type": "float[]",
      "unit": "rad",
      "rate": "100Hz",
      "description": "Current joint angles"
    }
  ],
  "act": [
    {
      "name": "move_joint",
      "args": {
        "joint": "int — joint index (0-22)",
        "target": "float — target angle in radians"
      },
      "description": "Move a single joint to target angle",
      "dangerous": true
    }
  ],
  "shield": [
    {
      "name": "joint_limit",
      "type": "limit",
      "value": 3.14,
      "unit": "rad",
      "description": "Maximum joint angle"
    }
  ],
  "tags": {
    "location": "assembly-line-2",
    "last_maintenance": "2026-03-01"
  }
}
```

## Observe Channels

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Channel identifier |
| type | string | Yes | Data type: `float`, `int`, `bool`, `string`, `float[]`, `image`, `json` |
| unit | string | No | SI unit or custom: `°C`, `rad`, `m/s`, `percent`, `Pa` |
| rate | string | No | Update frequency: `100Hz`, `1Hz`, `on_change`, `on_request` |
| description | string | No | Human/LLM-readable explanation |
| range | [min, max] | No | Valid value range |

## Action Specs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Command identifier |
| args | object | No | Argument name → type description |
| description | string | No | What it does |
| dangerous | bool | No | If true, requires confirmation at GUIDED level |
| priority | string | No | `normal`, `high`, `critical` |
| returns | string | No | What the action returns |

## Shield Specs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Rule identifier |
| type | string | Yes | `limit`, `zone`, `threshold`, `pattern`, `confirm` |
| value | any | No | The constraint value |
| unit | string | No | Unit of the constraint |
| description | string | No | Explanation |

## LLM Description

Implementations MUST provide a `to_llm_description()` method that generates
a human-readable summary of the manifest. Used by LLM context injection to understand
the node. It must be concise, complete, and unambiguous.

