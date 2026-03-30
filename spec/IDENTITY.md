# NRP Identity Specification

## Overview

Every node in the NRP ecosystem has a unique, human-readable address.
Like URLs for the web. Like email for people.

## Format

```
nrp://scope/kind/name
```

### Components

| Component | Description | Rules |
|-----------|-------------|-------|
| `scope` | Location, org, or environment | Lowercase alphanumeric, hyphens, dots. E.g. `factory-3`, `home`, `eu-west` |
| `kind` | Device type category | Lowercase alphanumeric, hyphens. E.g. `robot`, `sensor`, `server`, `api` |
| `name` | Instance identifier | Lowercase alphanumeric, hyphens, dots. E.g. `arm-7`, `soil-north`, `prod-1` |

### Examples

```
nrp://factory-3/robot/arm-7           Industrial robot arm
nrp://farm/sensor/soil-north          Soil moisture sensor
nrp://fleet/vehicle/truck-42          Delivery truck
nrp://home/light/kitchen              Smart light
nrp://cloud/server/prod-1             Production server
nrp://cloud/api/stripe                Stripe payment API
nrp://work/email/inbox                Email inbox
nrp://city/traffic/intersection-5     Traffic light controller
```

### Glob Matching

NRP IDs support glob patterns for group operations:

```
nrp://factory-*/robot/*       All robots in all factories
nrp://home/*/kitchen*         All kitchen devices
nrp://cloud/server/*          All servers
```

### Properties

- **Stable**: Survives IP changes, network moves, device replacement
- **Human-readable**: A human can understand what a node is from its ID
- **Hierarchical**: Scope > Kind > Name enables group operations
- **Lowercase**: No case sensitivity issues
- **URL-safe**: Can be used in HTTP paths, JSON keys, filenames

### Validation Regex

```
^nrp://[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9_-]*/[a-z0-9][a-z0-9._-]*$
```

