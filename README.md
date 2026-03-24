<div align="center">

# NRP — Node Reach Protocol

**6 rules. No AI can break them.**

[![PyPI](https://img.shields.io/pypi/v/nrprotocol?color=2563eb)](https://pypi.org/project/nrprotocol/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-2563eb.svg)](https://python.org)

[Website](https://nrprotocol.dev) · [The 6 Rules](#the-6-rules) · [SDK](#sdk) · [Why NRP](#why-nrp)

</div>

---

## The Problem

AI agents act autonomously — deleting files, controlling robots, managing infrastructure.  
MCP gives them tools.  
**NRP makes sure they don't break things.**

---

## The 6 Rules

Every AI action touching a physical or connected system must pass through these 6 rules.  
Remove any one and the system is unsafe. Add anything and it reduces to these 6.

| Rule | Question | Purpose |
|------|----------|---------|
| **Manifest** | *Who are you?* | Node declares identity before any action |
| **Observe** | *What do you see?* | Read state safely, no side effects |
| **Act** | *What will you do?* | Execute action, checked against shields |
| **Shield** | *What can you NOT do?* | Unbreakable constraint, enforced before execution |
| **Audit** | *What did you do?* | Tamper-evident SHA-256 record |
| **Consent** | *Did we agree?* | Mutual human + system permission |

---

## Why NRP

Protocols like MCP standardize **how** agents communicate with tools.  
NRP standardizes **whether** an agent is allowed to act at all.

```
AI Agent
   │
   ▼ NRP intercepts every action
   ├── Manifest:  agent declares identity
   ├── Observe:   safe read (no mutation)
   ├── Shield:    is this action forbidden?  ──► BLOCKED if yes
   ├── Consent:   is human approval present? ──► BLOCKED if no
   ├── Act:       execute the action
   └── Audit:     record proof of execution
```

**The Shield and Consent rules cannot be bypassed by the agent** — they run in a separate process the agent cannot access.

---

## NRP Identity

Every node in an NRP system has a URI:

```
nrp://scope/kind/name
```

| Part | Example | Meaning |
|------|---------|---------|
| scope | `factory` | Organizational boundary |
| kind | `robot`, `server`, `sensor` | Device type |
| name | `arm-7`, `web-01`, `temp-south` | Instance name |

```python
from nrp import NRPId

nid = NRPId.parse("nrp://factory/robot/arm-7")
print(nid.scope)   # factory
print(nid.kind)    # robot
print(nid.name)    # arm-7
```

---

## SDK

### Python

```bash
pip install nrprotocol
```

```python
from nrp import NRPNode, Shield, ConsentLevel

# Create a node
node = NRPNode("nrp://datacenter/server/web-01")

# Define what this node CANNOT do
node.add_shield(Shield.no_delete_production())
node.add_shield(Shield.max_autonomy(level=3))  # PHY rule

# Agent tries to act
result = node.act(
    agent="aap://myorg/assistant/deploy-bot@1.0",
    action="restart_service",
    resource="nginx",
    consent=ConsentLevel.HUMAN_APPROVED
)

print(result.audit_hash)  # sha256:f3a1...
print(result.allowed)     # True
```

### TypeScript

```typescript
import { NRPNode, Shield, ConsentLevel } from 'nrprotocol';

const node = new NRPNode('nrp://datacenter/server/web-01');
node.addShield(Shield.noDeleteProduction());

const result = await node.act({
  agent: 'aap://myorg/assistant/deploy-bot@1.0',
  action: 'restart_service',
  resource: 'nginx',
  consent: ConsentLevel.HUMAN_APPROVED,
});

console.log(result.allowed);    // true
console.log(result.auditHash);  // sha256:f3a1...
```

---

## Supported Node Types

| Type | Examples | Shield defaults |
|------|----------|-----------------|
| `robot` | Arms, drones, vehicles | Max autonomy 2, no irreversible |
| `server` | Cloud, VPS, containers | Max autonomy 3, no rm -rf |
| `sensor` | Temperature, cameras, meters | Observe-only by default |
| `actuator` | Valves, switches, motors | Consent required, max autonomy 2 |
| `agent` | AI models, automation scripts | All 6 rules, full audit |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE)

**Created by:** Elmadani SALKA · contact@nrprotocol.dev
